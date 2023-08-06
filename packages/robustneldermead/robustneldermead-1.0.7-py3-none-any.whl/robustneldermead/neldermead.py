# Contains the custom Nelder-Mead algorithm
import numpy as np
import sys
eps = sys.float_info.epsilon # For Amoeba xtol and tfol
import time
import pdb
import copy
from numba import njit, jit, prange
from pdb import set_trace as stop
import optimparameters.parameters as optimparameters
import numba


class NelderMead:
    """A class to interact with the Nelder Mead optimizer.
    
    """
    
    def __init__(self, target_function, init_pars, names=None, minvs=None, maxvs=None, varies=None, max_f_evals=None, xtol=1E-4, ftol=1E-4, n_iterations=None, no_improve_break=3, penalty=1E6, alpha=1, gamma=2, sigma=0.5, delta=0.5, args_to_pass=(), kwargs_to_pass={}, subspaces=None):
        """Initiate a Nelder Mead solver.
        
        Args:
            target_function (function): The function to optimize. Must be called as ``target_function(pars, *args_to_pass, **kwargs_to_pass)``, with return values: ``(F, CONS)``, where F is the value to minimize and CONS = g(x) is the constraint. If g(x) < 0, the target function is penalized, along with parameters being out of bounds.
            init_pars (Parameters or np.ndarray): The initial parameters.
            names (list or np.ndarray, optional): The names of the parameters. Internally defaults to par1, par2, ...
            minvs (list or np.ndarray, optional): The lower bounds. Defaults to -inf.
            maxvs (list or np.ndarray, optional): The upper bounds. Defaults to inf.
            varies (list or np.ndarray, optional): Whether or not to vary (and effectively solve for) this parameter. Defaults to True.
            max_f_evals (int, optional): The maximum total number of function calls, including all full simplex + subspace calls. Defaults to 5000 x number of varied parameters.
            xtol (float, optional): If the relative range of all parameters are below this threshold (i.e, span a range smaller than this), then the solver breaks. Defaults to 1E-4.
            ftol (float, optional): If the relative range of function values is below this threshold, then the solver breaks and is considered converged.. Defaults to 1E-4.
            n_iterations (int, optional): The number of iterations to run. One iteration = 1 full simplex call + Subspace calls for consecutive pairs of parameters, including last parameter, first parameter. Defaults to = number of varied parameters.
            no_improve_break (int, optional): The consective number of times the solver needs to converge (reach ftol) before breaking. Defaults to 3.
            penalty (float, optional): The penalty term added to the target function return value if either parameters are out of bounds or if the constraint is < 0.. Defaults to 1E6.
            alpha (float, optional): NM hyper-parameter (see src code). Defaults to 1.
            gamma (float, optional): NM hyper-parameter (see src code). Defaults to 2.
            sigma (float, optional): NM hyper-parameter (see src code). Defaults to 0.5.
            delta (float, optional): NM hyper-parameter (see src code). Defaults to 0.5.
            args_to_pass (tuple, optional): The additional arguments to pass to the target function. Defaults to (), empty tuple.
            kwargs_to_pass (dict, optional): The additional keyword arguments to pass to the target function. Defaults to {}, empty dict.
        """

        # The target function
        self.target_function = target_function
        
        # The tolerance on x and f
        self.xtol, self.ftol = xtol, ftol
            
        # The number of consecutive convergences to actually converge
        self.no_improve_break = no_improve_break
            
        # The arguments to pass to the target function
        self.args_to_pass = args_to_pass
        self.kwargs_to_pass = kwargs_to_pass
        
        # The panalty term
        self.penalty = penalty
        
        # Nelder-Mead scale factors
        self.alpha, self.gamma, self.sigma, self.delta = alpha, gamma, sigma, delta
        
        # Init simplex
        self.init_params(init_pars, names=names, minvs=minvs, maxvs=maxvs, varies=varies)
        
        if n_iterations is not None:
            self.n_iterations = n_iterations
        else:
            self.n_iterations = self.n_pars_vary
            
        if max_f_evals is not None:
            self.max_f_evals = max_f_evals
        else:
            self.max_f_evals = self.n_pars_vary * 5000
        
        # test_pars is constantly updated and passed to the target function wrapper
        # If only using numpy, test_pars will be unpacked before calling the actual target function.
        self.test_pars = copy.deepcopy(self.init_pars)
        
        # Copy the original parameters to the current min
        self.xmin = copy.deepcopy(self.init_pars)
        
        # f calls
        self.fcalls = 0
        
        # The current fmin = inf
        self.fmin = np.inf
        
        # Init the subspaces
        self.init_subspaces(subspaces=subspaces)
        
        # Convergence status
        self.converged = False
        
    def init_subspaces(self, subspaces=None):
        """ Initializes the subspaces.
        
        Args:
            subspaces (iterable): An iterable of indices or parameter names. Indices are relative to the entire parameter space.
        """
        
        # Aliases
        vpi = self.init_pars_vary_indices
        names = self.init_pars_numpy['name']
        
        # Default subspaces are each consecutive pair of parameters
        if subspaces is None:
            
            if len(vpi) >= 3:
                
                # All consecutive pairs
                self.subspace_vary_inds = [[i, i+1] for i in range(self.n_pars_vary - 1)]
                self.subspace_inds = [[vpi[i], vpi[i+1]] for i in range(self.n_pars_vary - 1)]
                self.subspace_names = [[names[vpi[i]], names[vpi[i+1]]] for i in range(self.n_pars_vary - 1)]
                
                # Last pair
                self.subspace_inds.append([0, vpi[self.n_pars_vary - 1]])
                self.subspace_vary_inds.append([0, self.n_pars_vary - 1])
                self.subspace_names.append([names[vpi[0]], names[vpi[-1]]])
                self.n_subspaces = len(self.subspace_names)

            else:
                self.subspace_inds = None
                self.subspace_vary_inds = None
                self.subspace_names = None
                self.n_subspaces = 0
                
        else:
            
            # Parameter names
            if type(subspaces[0][0]) is str:
                
                # First filter the subspaces to ensure they only include varied parameters
                for subspace in subspaces:
                    for p in subspace:
                        if not self.init_pars[p].vary:
                            subspace.remove(p)
                
                self.subspace_names = subspaces
                self.subspace_inds = []
                self.subspace_vary_inds = []
                for subspace in subspaces:
                    self.subspace_vary_inds.append([list(self.init_pars_numpy_vary['name']).index(p) for p in subspace])
                    self.subspace_inds.append([self.init_pars_numpy['name'].index(p) for p in subspace])
                    
            # Indices relative to entire parameter space
            else:
                
                # First filter the subspaces to ensure they only include varied parameters
                for subspace in subspaces:
                    for i in subspace:
                        p = names[i]
                        if not self.init_pars[p].vary:
                            subspace.remove(i)
                            
                self.subspace_inds = subspaces
                self.subspace_names = []
                self.subspace_vary_inds = []
                for isubspace, subspace in enumerate(subspaces):
                    self.subspace_names.append([names[i] for i in self.subspace_inds])
                    self.subspace_vary_inds.append([list(self.init_pars_numpy_vary['name']).index() for name in self.subspace_names])
                    
            self.n_subspaces = len(self.subspace_names)
            
    def init_params(self, init_pars, names=None, minvs=None, maxvs=None, varies=None):
        """Initialize the parameters

        Args:
            init_pars ([type]): [description]
            names ([type], optional): [description]. Defaults to None.
            minvs ([type], optional): [description]. Defaults to None.
            maxvs ([type], optional): [description]. Defaults to None.
            varies ([type], optional): [description]. Defaults to None.

        Raises:
            ValueError: [description]
        """
        # The number of parameters
        self.n_pars = len(init_pars)
        
        # The initial parameters
        if type(init_pars) is optimparameters.Parameters:
            self.uses_parameters = True
            self.init_pars = init_pars
        else:
            self.uses_parameters = False
            names = ['par' + str(i+1) for i in range(self.n_pars)]
            self.init_pars = optimparameters.Parameters.from_numpy(name=names, value=init_pars, minv=minvs, maxv=maxvs, vary=varies)

        self.init_pars_numpy = self.init_pars.unpack() # A dictionary
        self.init_pars_vary_indices = np.where(self.init_pars_numpy['vary'])[0]
        self.init_pars_numpy_vary = {}
        for key in self.init_pars_numpy:
            self.init_pars_numpy_vary[key] = self.init_pars_numpy[key][self.init_pars_vary_indices]
        
        # Number of varied parameters
        self.n_pars_vary = len(self.init_pars_vary_indices)
        
        if self.n_pars_vary == 0:
            raise ValueError("No Parameters to vary")
        
        # Initialize a simplex
        self.current_full_simplex = np.zeros(shape=(self.n_pars_vary, self.n_pars_vary + 1), dtype=float)
        
        # Fill each column with the initial parameters
        self.current_full_simplex[:, :] = np.tile(self.init_pars_numpy_vary['value'].reshape(self.n_pars_vary, 1), (1, self.n_pars_vary + 1))
        
        # For each column, offset a uniqe parameter according to p=1.5*p
        self.current_full_simplex[:, :-1] += np.diag(0.5 * self.init_pars_numpy_vary['value'])


    def init_space(self, subspace_index=None):
        
        if subspace_index is not None:
            n = len(self.subspace_names[subspace_index])
            inds = self.subspace_inds[subspace_index]
            self.current_simplex = np.zeros((n, n+1))
            pbest = self.xmin['value'][inds]
            pinit = self.init_pars_numpy['value'][inds]
            self.current_simplex[:, 0] = np.copy(pbest)
            self.current_simplex[:, 1] = np.copy(pinit)
            for i in range(2, n + 1):
                self.current_simplex[:, i] = np.copy(pbest)
                j = i -2
                self.current_simplex[j, i] = pinit[j]
        else:
            self.current_simplex = np.copy(self.current_full_simplex)
            
        self.test_pars = copy.deepcopy(self.xmin)

    def solve_space(self, subspace_index=None):
        
        # Generate a simplex for this subspace
        self.init_space(subspace_index=subspace_index)
        
        simplex = self.current_simplex
        
        # Define these as they are used often
        nx, nxp1 = simplex.shape

        # Initiate storage arrays
        fvals = np.empty(nxp1, dtype=float)
        xr = np.empty(nx, dtype=float)
        xbar = np.empty(nx, dtype=float)
        xc = np.empty(nx, dtype=float)
        xe = np.empty(nx, dtype=float)
        xcc = np.empty(nx, dtype=float)
        
        # Generate the fvals for the initial simplex
        for i in range(nxp1):
            fvals[i] = self.foo_wrapper(simplex[:, i], subspace_index=subspace_index)

        # Sort the fvals and then simplex
        ind = np.argsort(fvals)
        simplex = simplex[:, ind]
        fvals = fvals[ind]
        fmin = fvals[0]
        
        # Best fit parameter is now the first column
        xmin = simplex[:, 0]
        
        # Keeps track of the number of times the solver thinks it has converged in a row.
        n_converged = 0
        
        # Force convergence with break
        while True:

            # Sort the vertices according from best to worst
            # Define the worst and best vertex, and f(best vertex)
            xnp1 = simplex[:, -1]
            fnp1 = fvals[-1]
            x1 = simplex[:, 0]
            f1 = fvals[0]
            xn = simplex[:, -2]
            fn = fvals[-2]
                
            # Checks whether or not to shrink if all other checks "fail"
            shrink = False

            # break after max number function calls is reached.
            if self.fcalls >= self.max_f_evals:
                self.converged = False
                break
                
            # Break if f tolerance has been met
            if self.compute_ftol(fmin, fnp1) > self.ftol:
                n_converged = 0
            else:
                n_converged += 1
            if n_converged >= self.no_improve_break:
                self.converged = True
                break

            # Idea of NM: Given a sorted simplex; N + 1 Vectors of N parameters,
            # We want to iteratively replace the worst point with a better point.
            
            # The "average" vector, ignoring the worst point
            # We first anchor points off this average Vector
            xbar[:] = np.average(simplex[:, :-1], axis=1)
            
            # The reflection point
            xr[:] = xbar + self.alpha * (xbar - xnp1)
            
            # Update the current testing parameter with xr
            fr = self.foo_wrapper(xr, subspace_index=subspace_index)

            if fr < f1:
                xe[:] = xbar + self.gamma * (xbar - xnp1)
                fe = self.foo_wrapper(xe, subspace_index=subspace_index)
                if fe < fr:
                    simplex[:, -1] = np.copy(xe)
                    fvals[-1] = fe
                else:
                    simplex[:, -1] = np.copy(xr)
                    fvals[-1] = fr
            elif fr < fn:
                simplex[:, -1] = xr
                fvals[-1] = fr
            else:
                if fr < fnp1:
                    xc[:] = xbar + self.sigma * (xbar - xnp1)
                    fc = self.foo_wrapper(xc, subspace_index=subspace_index)
                    if fc <= fr:
                        simplex[:, -1] = np.copy(xc)
                        fvals[-1] = fc
                    else:
                        shrink = True
                else:
                    xcc[:] = xbar + self.sigma * (xnp1 - xbar)
                    fcc = self.foo_wrapper(xcc, subspace_index=subspace_index)
                    if fcc < fvals[-1]:
                        simplex[:, -1] = np.copy(xcc)
                        fvals[-1] = fcc
                    else:
                        shrink = True
            if shrink:
                for j in range(1, nxp1):
                    simplex[:, j] = x1 + self.delta * (simplex[:, j] - x1)
                    fvals[j] = self.foo_wrapper(simplex[:, j], subspace_index=subspace_index)

            ind = np.argsort(fvals)
            fvals = fvals[ind]
            simplex = simplex[:, ind]
            fmin = fvals[0]
            xmin = simplex[:, 0]
            
        # Update current simplex
        self.current_simplex = np.copy(simplex)
        
        # Update full simplex
        if subspace_index is not None:
            self.current_full_simplex[:, self.subspace_vary_inds[subspace_index][0:-1]] = np.tile(xmin.reshape(xmin.size, 1), (len(self.subspace_vary_inds[subspace_index]) - 1))
        else:
            self.current_full_simplex = np.copy(self.current_simplex)
        
        if subspace_index is None:
            self.current_full_simplex = np.copy(simplex)
            for i, p in enumerate(self.init_pars_numpy_vary['name']):
                self.xmin[p].setv(value=xmin[i])
        else:
            for i, p in enumerate(self.subspace_names[subspace_index]):
                self.xmin[p].setv(value=xmin[i])
            
        # Redefine the numpy variable
        self.xmin_numpy = self.xmin.unpack()
        
        # Update the current function minimum
        self.fmin = fmin
        
        
    def solve(self):
        
        iteration = 1
        dx = np.inf
        
        for iteration in range(self.n_iterations):

            # Perform Ameoba call for all parameters
            self.solve_space(None)
            
            dx = self.compute_xtol(self.current_simplex)
            if dx > self.xtol:
                break
            
            # If there's <= 2 params, a three-simplex is the smallest simplex used and only used once.
            if self.n_pars_vary <= 2:
                break
            
            # Perform Ameoba call for subspaces
            for subspace_index in range(self.n_subspaces):
                self.solve_space(subspace_index)

            # Update the iteration
            iteration += 1
            
            # Compute the max absolute range of the simplex
            dx = self.compute_xtol(self.current_simplex)
        
        # Compute uncertainties
        if self.converged:
            try:
                xmin_err = self.compute_uncertainties(self.current_simplex)
            except:
                xmin_err = np.full(self.n_pars_vary, fill_value=np.nan)
        else:
            xmin_err = np.full(self.n_pars_vary, fill_value=np.nan)
        
        # Output variable
        out = {}
        out['converged'] = self.converged
        out['fmin'] = self.fmin
        out['fcalls'] = self.fcalls
            
        # Recreate new parameter obejcts
        if self.uses_parameters:
            out['xmin'] = self.xmin
            k = 0
            for pname in out['xmin'].keys():
                if out['xmin'][pname].vary:
                    out['xmin'][pname].setv(uncertainty=xmin_err[k])
                    k += 1
            out['fmin'] = self.fmin
            out['fcalls'] = self.fcalls
        else:
            out['xmin'] = self.xmin.unpack(keys=['value'])['value']
            out['xmin_err'] = xmin_err
            
        return out
    
    def compute_uncertainties(self, sim):
        
        # fit quadratic coefficients
        sim = sim.T
        n = len(sim) - 1
        fsim = np.zeros(n+1)
        for i in range(n+1):
            fsim[i] = self.foo_wrapper(sim[i])

        ymin = fsim[0]

        sim = np.copy(sim)
        fsim = np.copy(fsim)

        centroid = np.mean(sim, axis=0)
        fcentroid = self.foo_wrapper(centroid)

        # enlarge distance of simplex vertices from centroid until all have at
        # least an absolute function value distance of 0.1
        for i in range(n + 1):
            while np.abs(fsim[i] - fcentroid) < 0.01:
                sim[i] += sim[i] - centroid
                fsim[i] = self.foo_wrapper(sim[i])

        # the vertices and the midpoints x_ij
        x = 0.5 * (
            sim[np.mgrid[0:n + 1, 0:n + 1]][1] +
            sim[np.mgrid[0:n + 1, 0:n + 1]][0]
        )

        y = np.nan * np.ones(shape=(n + 1, n + 1))
        for i in range(n + 1):
            y[i, i] = fsim[i]
            for j in range(i + 1, n + 1):
                y[i, j] = y[j, i] = self.foo_wrapper(x[i, j])

        y0i = y[np.mgrid[0:n + 1, 0:n + 1]][0][1:, 1:, 0]

        y0j = y[np.mgrid[0:n + 1, 0:n + 1]][0][0, 1:, 1:]

        b = 2 * (y[1:, 1:] + y[0, 0] - y0i - y0j)

        q = (sim - sim[0])[1:].T

        varco = ymin * np.dot(q, np.dot(np.linalg.inv(b), q.T))
        errors = np.sqrt(np.diag(varco))
        
        return errors
    
        
    @staticmethod
    def compute_xtol(simplex):
        a = np.nanmin(simplex, axis=1)
        b = np.nanmax(simplex, axis=1)
        c = (np.abs(b) + np.abs(a)) / 2
        c = np.atleast_1d(c)
        ind = np.where(c < eps)[0]
        if ind.size > 0:
            c[ind] = 1
        r = np.abs(b - a) / c
        return np.nanmax(r)

    @staticmethod
    @njit(numba.types.float64(numba.types.float64, numba.types.float64))
    def compute_ftol(a, b):
        return np.abs(a - b)
            
    def foo_wrapper(self, x, subspace_index=None):
        
        if subspace_index is None:
            for i, p in enumerate(self.init_pars_numpy_vary['name']):
                self.test_pars[p].setv(value=x[i])
        else:
            for i, p in enumerate(self.subspace_names[subspace_index]):
                self.test_pars[p].setv(value=x[i])
        
        # Call the target function
        if self.uses_parameters:
            res = self.target_function(self.test_pars, *self.args_to_pass, **self.kwargs_to_pass)
            if type(res) is tuple:
                f, c = res
            else:
                f, c = res, 1
        else:
            res = self.target_function(self.test_pars.unpack(keys=['value'])['value'], *self.args_to_pass, **self.kwargs_to_pass)
            if type(res) is tuple:
                f, c = res
            else:
                f, c = res, 1
        
        # Penalize the target function if pars are out of bounds or constraint is less than zero
        vals = self.test_pars.unpack(keys='value')['value']
        f += self.penalty * np.where((vals < self.init_pars_numpy['minv']) | (vals > self.init_pars_numpy['maxv']))[0].size
        f += self.penalty * (c < 0)
        
        # Update fcalls
        self.fcalls += 1
        
        # Only return a single value for the function.
        return f