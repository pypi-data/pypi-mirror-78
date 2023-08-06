"""
Copyright 2019 Marco Dal Molin
Licensed under the Apache License, version 2.0. See LICENSE for details.

CODED BY: Marco Dal Molin (marco.dalmolin.1991@gmail.com)
DESIGNED BY: Marco Dal Molin (marco.dalmolin.1991@gmail.com)
REVIEWED BY: None

This module contains the numerical solver for the differential equations used
by the elements.
"""

import numpy as np
import inspect
import numba as nb

class Solver(object):
    """
    Abstract base class define how the solver of the differential equation must
    be implemented.
    """

    def __init__(self, tol_F = 1e-8, tol_x = 1e-8, iter_max = 10):
        """
        The constructor of the subclass must accept the parameters of the
        solver.

        Parameters
        ----------
        tol_F : float
            Tollerance on the y axis (distance from 0) that stops the solver
        tol_x : float
            Tollerance on the x axis (distance between two roots) that stops
            the solver
        iter_max : int
            Maximum number of iteration of the solver. After this value it
            raises a runtime error
        """

        self._tol_F = tol_F
        self._tol_x = tol_x
        self._iter_max = iter_max
        self._name = 'Solver'
    
    def __repr__(self):
        str = 'Module: superflexPy\nClass: {}\n'.format(self._name)
        str += 'Parameters:\n'
        str += '\ttol_F = {}\n'.format(self._tol_F)
        str += '\ttol_x = {}\n'.format(self._tol_x)
        str += '\titer_max = {}'.format(self._iter_max)

        return str
    
    def _error_message(self):
        return 'module : superflexPy, solver : {}'.format(self._name)

    def solve(self, *args, **kwargs):
        """
        Must be overwritten by any sub-class.
        This method finds the root of the numerical approximation of the
        differential equation. It can operate over the whole time series
        """

        raise NotImplementedError('The method solve must be implemented')

class DmitriSolverPython(Solver):
    """
    This class implements the solver used in Superflex
    TODO
    """

    def __init__(self, tol_F = 1e-8, tol_x = 1e-8, iter_max = 10):
        """
        This class implements the solver used in Superflex
        TODO

        Parameters
        ----------
        tol_F : float
            Tollerance on the y axis (distance from 0) that stops the solver
        tol_x : float
            Tollerance on the x axis (distance between two roots) that stops
            the solver
        iter_max : int
            Maximum number of iteration of the solver. After this value it
            raises a runtime error
        """
        super().__init__(tol_F = tol_F,
                         tol_x = tol_x,
                         iter_max = iter_max)
        self._name = 'DmitriSolverPython'
        self.architecture = 'python'
    
    def solve(self, fun, **kwargs):
        """
        This method calculated the root of the input function. The solver 
        iterates over the provided vectors.

        Parameters
        ----------
        Parameters
        ----------
        fun : function or list(function)
            Function or list of functions to be solved. The function must
            accept the inputs in the followig order:
            - root. If None, the function must initialize the root
            - **kwargs (the initial state must be called S0)
            It must return three float values:
            - Value of the function given the root and the kwargs
            - Lower x boundary for the search
            - Upper x boundary for the search
        **kwargs : 
            Arguments of fun
        
        Returns
        -------
        numpy.ndarray
            Array of roots. It is a 2D array with dimensions (#timesteps, 
            #functions)
        """
        
        if 'S0' not in kwargs:
            raise KeyError('{}, method : solve, \'S0\' must be in **kwargs'.format(self._error_message()))

        # Divide the parameters of fun between arrays (time variant) and float
        vectors = []
        scalars = []
        
        for k in kwargs:
            if k == 'S0':
                continue
            if isinstance(kwargs[k], np.ndarray):
                vectors.append(k)
            elif isinstance(kwargs[k], float):
                scalars.append(k)
            else:
                raise TypeError() # TODO
                
        # Construct the output array
        output = []
        
        if not isinstance(fun, list):
            fun = [fun]
        
        if not isinstance(kwargs['S0'], list):
            kwargs['S0'] = [kwargs['S0']]

        for f, S0 in zip(fun, kwargs['S0']):
            output.append(self._solve(fun = f,
                                      S0 = S0,
                                      kwargs = kwargs,
                                      vectors = vectors,
                                      scalars = scalars))

        return np.array(output).reshape((-1, len(fun)))

    def _solve(self, fun, S0, kwargs, vectors, scalars):
        
        output = []
        
        fun_pars = list(inspect.signature(fun).parameters)

        # Loop in time
        for i in range(kwargs[vectors[0]].shape[0]):
            # Create the **kwargs for the timestep
            loc_kwargs = {}
            for k in kwargs:
                if (k in vectors) and (k in fun_pars):
                    loc_kwargs[k] = float(kwargs[k][i])
                elif (k in scalars) and (k in fun_pars):
                    loc_kwargs[k] = kwargs[k]
                else:
                    continue
            
            # Initialize the function
            a, b = fun(S = None, S0 = S0, **loc_kwargs)[1:]
            fa = fun(S = a, S0 = S0, **loc_kwargs)[0]
            fb = fun(S = b, S0 = S0, **loc_kwargs)[0]
            
            if fa * fb > 0:
                raise ValueError('{}, method : solve, fa and fb have the same sign: {} vs {}'.format(self._error_message(),
                                                                                                     fa,
                                                                                                     fb))
            
            # Iterate the solver
            for j in range(self._iter_max):
                
                xmin = min(a, b)
                xmax = max(a, b)
        
                dx = -(fa/(fb - fa)) * (b - a)
                root = a + dx
            
                if root < xmin:
                    root = xmin
                elif root > xmax:
                    root = xmax
            
                dx = root - a

                f_root = fun(root, S0 = S0, **loc_kwargs)[0]

                if f_root*fa < 0:
                    b = a
                    fb = fa
                else:
                    fFac = fa/(fa+f_root)
                    fb = fb * fFac
            
                a = root
                fa = f_root

                if np.abs(f_root) < self._tol_F:
                    output.append(root)
                    break
        
                if np.abs(a - b) < self._tol_x:
                    output.append(root)
                    break
                
                if j+1 == self._iter_max:
                    raise RuntimeError('{}, method : solve, not converged. iter_max : {}'.format(self._error_message(),
                                                                                                 self._iter_max))
            S0 = output[i]
        
        return np.array(output)

class DmitriSolverNumba(Solver):

    def __init__(self, tol_F = 1e-8, tol_x = 1e-8, iter_max = 10):
        """
        This class implements the numba optimization of the solver used in
        Superflex

        TODO

        Parameters
        ----------
        tol_F : float
            Tollerance on the y axis (distance from 0) that stops the solver
        tol_x : float
            Tollerance on the x axis (distance between two roots) that stops
            the solver
        iter_max : int
            Maximum number of iteration of the solver. After this value it
            raises a runtime error
        """
        super().__init__(tol_F = tol_F,
                         tol_x = tol_x,
                         iter_max = iter_max)
        self._name = 'DmitriSolverPython'
        self.architecture = 'numba'

    def solve(self, fun, **kwargs):
        """
        This method calculate the root of the input function. The solver 
        iterates over the provided vectors.

        Parameters
        ----------
        fun : function or list(function)
            Function or list of functions to be solved. The function must be
            "numba decorated" and accept the inputs in the followig order:
            - root: if None, the function must initialize the root. The root 
                    must be called S and be of type float64.
            - S0: initial state of type float64
            - ind: index of the array to look for (type int32)
            - **kwargs: inputs and parameters. All of type float64[:]
            It must return three float values:
            - Value of the function given the root and the kwargs
            - Lower x boundary for the search
            - Upper x boundary for the search
        **kwargs : 
            Arguments of fun
        
        Returns
        -------
        numpy.ndarray
            Array of roots. It is a 2D array with dimensions (#timesteps, 
            #functions)
        """

        if 'S0' not in kwargs:
            raise KeyError('{}, method : solve, \'S0\' must be in **kwargs'.format(self._error_message()))
        
        if not isinstance(fun, list):
            fun = [fun]
        
        if not isinstance(kwargs['S0'], list):
            kwargs['S0'] = [kwargs['S0']]

        # Construct the output array
        output = []

        for f, S0 in zip(fun, kwargs['S0']):
            # Get the arguments of the function -> this line will give error if the
            # function  is not numba because of the "py_func"
            arg_names = list(inspect.signature(f.py_func).parameters)
            # arg_names = list(inspect.signature(f).parameters)

            # Collect the args for the function
            args = []
            for name in arg_names:
                if name in ['S0', 'S', 'ind']:
                    continue
                if isinstance(kwargs[name], float):
                    args.append(np.array([kwargs[name]]))
                elif isinstance(kwargs[name], np.ndarray):
                        args.append(kwargs[name])
                else:
                    raise KeyError()

            # Find the length
            num_timestep = 0
            floats = []
            for i, a in enumerate(args):
                if a.shape[0] != 1:
                    if num_timestep == 0:
                        num_timestep = a.shape[0]
                    elif a.shape[0] != num_timestep:
                        raise ValueError()
                else:
                    floats.append(i)
            
            if num_timestep == 0:
                num_timestep = 1
            
            # Extend the float
            if num_timestep != 1:
                for i in floats:
                    args[i] = args[i] * np.ones(num_timestep)  #np.broadcast_to(args[i], (num_timestep))

            args = tuple(args)

            output.append(self._solve(f, S0, self._tol_F, self._tol_x, 
                                      self._iter_max, *args))
        
        return np.array(output).reshape((-1, len(fun)))

    @staticmethod
    @nb.jit(nopython = True)
    def _solve(fun, S0, tol_F, tol_x, iter_max, *args):

        num_ts = args[0].shape[0]
        output = np.zeros(num_ts)

        # Loop in time
        for i in range(num_ts):
            a, b = fun(None, S0, i, *args)[1:]
            fa = fun(a, S0, i, *args)[0]
            fb = fun(b, S0, i, *args)[0]
        
            # TODO: we avoid to raise value error if fa and fb have the same 
            # sign because I don't know if it works with numba

            # Iterate the solver
            for j in range(iter_max):
                
                if a>b:
                    xmin = b
                    xmax = a
                else:
                    xmin = a
                    xmax = b

                dx = -(fa/(fb - fa)) * (b - a)
                root = a + dx
            
                if root < xmin:
                    root = xmin
                elif root > xmax:
                    root = xmax
            
                dx = root - a

                f_root = fun(root, S0, i, *args)[0]

                if f_root*fa < 0:
                    b = a
                    fb = fa
                else:
                    fFac = fa/(fa+f_root)
                    fb = fb * fFac
            
                a = root
                fa = f_root

                if np.abs(f_root) < tol_F:
                    output[i] = root
                    break
        
                if np.abs(a - b) < tol_x:
                    output[i] = root
                    break
                
                if j+1 == iter_max:
                    output[i] = np.nan # TODO: I should raise an error here
                    
            S0 = output[i]
        
        return output

if __name__ == '__main__':
    solv = DmitriSolverPython()
    
    def FR_1(S, S0, P, k, alpha, dt):
        if S is None:
            S = 0
        out = (S-S0)/dt - P + k*S**alpha

        return (out, 0, S0+P)

    def FR_2(S, S0, P, k, dt):
        if S is None:
            S = 0
        out = (S-S0)/dt - P + k*S

        return (out, 0, S0+P)

    @nb.jit('UniTuple(f8, 3)(optional(f8), f8, i4, f8[:], f8[:], f8[:])',
            nopython = True)
    def FR_1_numba(S, S0, ind, P, k, dt):
        if S is None:
            S = 0

        P = P[ind]
        k = k[ind]
        dt = dt[ind]

        return((S-S0)/dt - P + k*S, 0.0, S0 + P)
    
    from datetime import datetime as dt
    nt = 100000
    precipitation = np.random.randn(nt)
    start = dt.now()
    S = solv.solve(fun = FR_2,
                   S0 = 10,
                   P = precipitation,
                   k = 1e-2,
                   alpha = 2.0,
                   dt = 1.0)
    end = dt.now()
    print('Python')
    print(end - start)
    print(S.shape)

    S = solv.solve(fun = [FR_1, FR_2],
                   S0 = [10, 15],
                   P = np.array([5, 0, 500]),
                   k = 1e-2,
                   alpha = 2.0,
                   dt = 1.0)

    print(S.shape)
    print(S)

    solv = DmitriSolverNumba()

    precipitation = np.random.randn(nt)
    start = dt.now()
    S = solv.solve(fun = FR_1_numba,
                   S0 = 10.0,
                   P = precipitation,
                   k = 1e-2,
                   alpha = 2.0,
                   dt = 1.0)
    end = dt.now()
    print('Numba')
    print(end - start)
    print(S.shape)

    precipitation = np.random.randn(nt)
    start = dt.now()
    S = solv.solve(fun = FR_1_numba,
                   S0 = 10.0,
                   P = precipitation,
                   k = 1e-2,
                   alpha = 2.0,
                   dt = 1.0)
    end = dt.now()
    print('Numba2')
    print(end - start)
    print(S.shape)
