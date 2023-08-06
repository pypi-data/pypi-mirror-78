"""
Copyright 2019 Marco Dal Molin
Licensed under the Apache License, version 2.0. See LICENSE for details.

CODED BY: Marco Dal Molin (marco.dalmolin.1991@gmail.com)
DESIGNED BY: Marco Dal Molin (marco.dalmolin.1991@gmail.com)
REVIEWED BY: None

This module contains some element that compose the HRU structure.
"""

# from .generic_elements import GenericElement
from generic_elements import GenericElement
import numba as nb

class FastReservoir(GenericElement):
    """
    The FastReservoir (FR) is governed by the differential equation

    \frac{dS}{dt} = P - Q
    Q = kS^\alpha

    """

    def __init__(self, parameters, states, solver, id):
        """
        This class implement the FastReservoir (FR).

        Parameters
        ----------
        parameters : dict(str : float)
            Contains the parameters of the model. The keys must be:
            'k' : multiplier of the state
            'alpha' : exponent of the state
        states : dict (str : float)
            Contains the initial state of the reservoir. The key must be:
            'S0' : initial state of the reservoir
        solver : TODO
            Numerical solver used to solve the differential equation
        id : str
            id of the element
        """
        
        super().__init__(parameters = parameters,
                         states = states,
                         solver = solver,
                         id = id)

        if solver.architecture == 'numba':
            self._differential_equation = self._differential_equation_numba
        elif solver.architecture == 'python':
            self._differential_equation = self._differential_equation_python

    #### METHODS FOR THE USER ####

    def set_input(self, input):
        """
        This method sets the input of the FR.

        Parameters
        ----------
        input : list(numpy.ndarray)
            List of inputs to the reservoir. Values must be provided in the
            following order:
            0 : precipitation (P)
        """

        self._inputs = {'P' : input[0]}

    def get_output(self, solve = True):
        """
        This method returns the output of the FR.

        Returns
        -------
        list(numpy.ndarray):
            List with the outputs of the reservoir in the following order:
            0 : streamflow (Q)
        """

        if solve:
            self._solver_states = [self._states[self._prefix_states + 'S0']]
            self._solve_differential_equation()

            # Update the state
            self.set_states({self._prefix_states + 'S0' : self.state_array[-1, 0]})

        k = self._parameters[self._prefix_parameters + 'k']
        alpha = self._parameters[self._prefix_parameters + 'alpha']
        return [k * self.state_array[:,0] ** alpha]

    #### PROTECTED METHODS ####

    @staticmethod
    def _differential_equation_python(S, S0, P, k, alpha, dt):
        if S is None:
            S = 0
        return ((S - S0)/dt - P + k*S**alpha, 0.0, S0+P)

    @staticmethod
    @nb.jit('UniTuple(f8, 3)(optional(f8), f8, i4, f8[:], f8[:], f8[:], f8[:])',
            nopython = True)
    def _differential_equation_numba(S, S0, ind, P, k, alpha, dt):
        if S is None:
            S = 0
        dt = dt[ind]
        P = P[ind]
        k = k[ind]
        alpha = alpha[ind]
        return ((S - S0)/dt - P + k*S**alpha, 0.0, S0+P)