"""
Copyright 2019 Marco Dal Molin
Licensed under the Apache License, version 2.0. See LICENSE for details.

CODED BY: Marco Dal Molin (marco.dalmolin.1991@gmail.com)
DESIGNED BY: Marco Dal Molin (marco.dalmolin.1991@gmail.com)
REVIEWED BY: Marco Dal Molin (marco.dalmolin.1991@gmail.com)

This module contains the generic elements to implement the model structure.
"""

import numpy as np
import warnings
from copy import copy, deepcopy

class GenericElement(object):
    """
    Abstract base class define how the generic element of the model (e.g. a
    reservoir) must be implemented.
    """

    _prefix_parameters = ''
    _prefix_states = ''
    _solver_states = []
    _num_downstream = 1
    _num_upstream = 1

    def __init__(self, parameters, states, solver, id):
        """
        The constructor of the subclass must accept at least the parameters of
        the element, the initial state, the numerical solver and the id.

        Parameters
        ----------
        parameters : dict(str : float)
            Parameters of the element.
        states : dict(str : float)
            Initial states of the element
        solver : TODO
            Numerical solver used to solve the differential equation
        id : str
            id of the element
        """

        self._parameters = parameters
        self._states = states
        self._init_states = deepcopy(states)  # It is used to re-set the states
        self._solver = solver
        self.id = id
        self.add_prefix_parameters(id)
        self.add_prefix_states(id)

    #### METHODS TO OVERWRITE ####

    def set_input(self, input):
        """
        The method must be implemented by the subclass. It sets the input
        fluxes of the element.

        Parameters
        ----------
        input : list(numpy.ndarray)
            List of inputs of the reservoir. It is due to the subclass to set
            their order.
        """
        raise NotImplementedError('The set_input method must be implemented')
    
    def get_output(self):
        """
        This method must be implemented by the subclass. It returns the output
        fluxes from the element.

        Returns
        -------
        list(numpy.ndarray)
            List with the outputs of the reservoir. It is due to the subclass 
            to set their order.
        """
        raise NotImplementedError('The get_output method must be implemented')

    def _differential_equation(self):
        """
        This method sets the differential equation(s) to be solved by the
        solver. The method must be implemented in order to satisfy the 
        requirements of the solver.
        """
        raise NotImplementedError('The differential_equation method must be implemented')

    #### METHODS FOR THE USER ####

    def get_parameters(self, names = None):
        """
        This method returns the parameters of the element.

        Parameters
        ----------
        names : list(str)
            Names of the parameters to return. The names must be the ones
            returned by the mehod get_parameters_name. If None, all the
            parameters are returned.
        
        Returns
        -------
        dict(str : float):
            Parameters of the element.
        """

        if names is None:
            return self._parameters
        else:
            return {n : self._parameters[n] for n in names}
        
    def get_parameters_name(self):
        """
        This method returns the names of the parameters of the element.

        Returns
        -------
        list(str):
            List with the names of the parameters
        """

        return list(self._parameters.keys())
    
    def set_parameters(self, parameters):
        """
        This method sets the values of the parameters.

        Parameters
        ----------
        parameters : dict(str : float)
            Contains the parameters of the element to be set. The keys must be
            the ones returned by the method get_parameters_name. Only the
            parameters that have to be changed should be passed.
        """ 

        for k in parameters.keys():
            if k not in self._parameters.keys():
                raise KeyError('{}. The parameter {} does not exist'.format(self._error_message(), k))
            self._parameters[k] = parameters[k]
    
    def get_states(self, names = None):
        """
        This method returns the states of the element.

        Parameters
        ----------
        names : list(str)
            Names of the states to return. The names must be the ones
            returned by the mehod get_states_name. If None, all the
            states are returned.
        
        Returns
        -------
        dict(str : float):
            States of the element.
        """
        
        if names is None:
            return self._states
        else:
            return {n : self._states[n] for n in names}

    def get_states_name(self):
        """
        This method returns the names of the states of the element.

        Returns
        -------
        list(str):
            List with the names of the states
        """

        return list(self._states.keys())
                
    def set_states(self, states):
        """
        This method sets the values of the states.

        Parameters
        ----------
        states : dict(str : float)
            Contains the states of the element to be set. The keys must be
            the ones returned by the method get_states_name. Only the
            states that have to be changed should be passed
        """ 

        for k in states.keys():
            if k not in self._states.keys():
                raise KeyError('{}. The state {} does not exist'.format(self._error_message(), k))
            self._states[k] = states[k]               

    def reset_states(self):
        """
        This method sets the states to the values set at initialization
        """
        self._states = deepcopy(self._init_states)  # I have to isolate

    def set_timestep(self, dt):
        """
        This method sets the timestep used by the element.

        Parameters
        ----------
        dt : float
            Timestep
        """
        self._dt = dt

    def get_timestep(self):
        """
        This method returns the timestep used by the element.

        Returns
        -------
        float
            Timestep
        """
        return self._dt

    def define_solver(self, solver):
        """
        This method define the solver to use for the differential equation.

        Parameters
        ----------
        solver : TODO
            Numerical solver used to solve the differential equation
        """
        self._solver = solver

    #### METHODS USED BY THE FRAMEWORK ####

    def add_prefix_parameters(self, prefix):
        """
        This method add a prefix to the id of the parameters of the element.

        Parameters
        ----------
        prefix : str
            Prefix to be added. It cannot contain '_'.
        """ 
        
        if '_' in prefix:
            raise ValueError('{}. The prefix cannot contain \'_\''.format(self._error_message()))

        # Extract the prefixes in the parameters name
        splitted = list(self._parameters.keys())[0].split('_')

        if prefix not in splitted:
            # Apply the prefix 
            for k in list(self._parameters.keys()):
                value = self._parameters.pop(k)
                self._parameters['{}_{}'.format(prefix, k)] = value
            
            # Save the prefix for furure uses
            self._prefix_parameters = '{}_{}'.format(prefix, self._prefix_parameters)
    
    def add_prefix_states(self, prefix):
        """
        This method add a prefix to the id of the states of the element.

        Parameters
        ----------
        prefix : str
            Prefix to be added. It cannot contain '_'.
        """ 
        
        if '_' in prefix:
            raise ValueError('{}. The prefix cannot contain \'_\''.format(self._error_message()))

        # Extract the prefixes in the parameters name
        splitted = list(self._states.keys())[0].split('_')

        if prefix not in splitted:
            # Apply the prefix 
            for k in list(self._states.keys()):
                value = self._states.pop(k)
                self._states['{}_{}'.format(prefix, k)] = value
            
            # Save the prefix for furure uses
            self._prefix_states = '{}_{}'.format(prefix, self._prefix_states)

    @property  # This is a way to make it "read-only"
    def num_downstream(self):
        """
        Number of elements downstream of the element: always one. If more, use
        a splitter.
        """
        return self._num_downstream

    @property # This is a way to make it "read-only"
    def num_upstream(self):
        """
        Number of elements upstream of the element: always one. If more, use
        a junction.
        """
        return self._num_upstream
    
    #### PROTECTED METHODS ####

    def _error_message(self):
        return 'module : superflexPy, element : {}'.format(self.id)

    def _solve_differential_equation(self):
        if len(self._solver_states) == 0:
            raise ValueError('{}. self._solver_states must be filled'.format(self._error_message))

        self.state_array = self._solver.solve(fun = self._differential_equation,
                                              S0 = self._solver_states,
                                              dt = self._dt,
                                              **self._inputs,
                                              **{k[len(self._prefix_parameters):] : self._parameters[k] for k in self._parameters})

    #### MAGIC METHODS ####

    def __copy__(self):
        p = self._parameters # Only the reference
        s = copy(self._states) # Create new dictionary
        ele = self.__class__(parameters = p,
                             states = s,
                             solver = self._solver,
                             id = self.id)
        ele._prefix_parameters = self._prefix_parameters
        ele._prefix_states = self._prefix_states
        return ele

    def __deepcopy__(self, memo):
        p = copy(self._parameters) # Create a new dictionary
        s = copy(self._states) # Create a new dictionary
        ele = self.__class__(parameters = p,
                             states = s,
                             solver = self._solver,
                             id = self.id)
        ele._prefix_parameters = self._prefix_parameters
        ele._prefix_states = self._prefix_states
        return ele

    def __repr__(self):
        str = 'Module: superflexPy\nElement: {}\n'.format(self.id)
        str += 'Parameters:\n'
        for k in self._parameters:
            str += '\t{} : {}\n'.format(k, self._parameters[k])
        str += 'States:\n'
        for k in self._states:
            str += '\t{} : {}\n'.format(k, self._states[k])
        
        return str


class StructureElement(object):
    """
    Abstract base class define an element of the structure (e.g. junction, 
    splitter, linker).
    """

    def __init__(self, direction, id):
        """
        Abstract method. The initializer should be extended by the element.
        
        Parameters
        ----------
        direction : list
            Define how to mix/split the fluxes
        id : str
            id of the element
        """
        self._direction = direction
        self.id = id

    #### METHODS TO OVERWRITE ####

    def get_output(self):
        """
        This method must be implemented by the subclass. It returns the output
        fluxes from the element.

        Returns
        -------
        list:
            List with the outputs of the reservoir. The dimensionality depends
            on the element.
        """
        raise NotImplementedError() # TODO

    #### METHODS FOR THE USER ####

    def set_input(self, input):
        """
        The method sets the input fluxes of the element.

        Parameters
        ----------
        input : list
            List of inputs of the element. The dimensionality depends on the
            element.
        """
        self.input = input

    def get_direction(self):
        """
        This method returns the direction of the element. See the documentation
        of the __init__ method for details.

        Returns
        -------
        list
            Direction list
        """
        return deepcopy(self._direction)

    def set_direction(self, direction):
        """
        This method sets the direction of the element. See the documentation 
        of the __init__ method for details.

        Parameters
        ----------
        direction : list
            Define how to mix/split the fluxes
        """
        self._direction = deepcopy(direction)
        
    #### METHODS USED BY THE FRAMEWORK ####

    @property # This is a way to make it "read-only"
    def num_downstream(self):
        """
        Number of elements downstream of the element.
        """
        return self._num_downstream

    @property # This is a way to make it "read-only"
    def num_upstream(self):
        """
        Number of elements upstream of the element.
        """
        return self._num_upstream





    