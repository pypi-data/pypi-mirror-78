from copy import copy, deepcopy
from common_class import CommonClass

class HRU(CommonClass):

    def __init__(self, layers, id, copy_pars = True):
        
        if copy_pars:
            # Deep-copy the elements
            self._layers = []
            for l in layers:
                self._layers.append([])
                for el in l:
                    self._layers[-1].append(deepcopy(el))
        else:
            self._layers = layers

        self.id = id
        
        self._check_layers()
        self.add_prefix_parameters(id)
        self.add_prefix_states(id)
        self._construct_dictionary()

    #### METHODS FOR THE USER ####

    def set_input(self, input):
        self.input = input

    def get_output(self, solve = True):
    
        # Set the first layer (it must have 1 element)
        self._layers[0][0].set_input(self.input)

        for i in range(1, len(self._layers)):
            # Collect the outputs
            outputs = []
            for el in self._layers[i-1]:
                if el.num_downstream == 1:
                    outputs.append(el.get_output(solve))
                else:
                    loc_out = el.get_output(solve)
                    for o in loc_out:
                        outputs.append(o)

            # Fill the inputs
            ind = 0
            for el in self._layers[i]:
                if el.num_upstream == 1:
                    el.set_input(outputs[ind])
                    ind += 1
                else:
                    loc_in = []
                    for _ in range(el.num_upstream):
                        loc_in.append(outputs[ind])
                        ind += 1
                    el.set_input(loc_in)

        # Return the output of the last element
        return self._layers[-1][0].get_output(solve)
    
    def append_layer(self, layer):
        self.insert_layer(layer, position = len(self._layers))

    def insert_layer(self, layer, position):
        l = []
        for el in layer:
            l.append(deepcopy(el))

        self._layers.insert(position, l)
        self._construct_dictionary()
        self._check_layers()

    def parse_structure(self, structure):
            raise NotImplementedError('Functionality in the TODO list')

    def get_internal(self, id, attribute):

        return self._find_attribute_from_name(id, attribute)   
        
    def call_internal(self, id, function, **kwargs):
    
        method = self._find_attribute_from_name(id, function)
        return method(**kwargs)

    #### METHODS USED BY THE FRAMEWORK ####

    def add_prefix_parameters(self, id):
        for l in self._layers:
            for el in l:
                try:
                    el.add_prefix_parameters(id)
                except AttributeError:
                    continue

    def add_prefix_states(self, id):
        # add the Prefix to the elements
        for l in self._layers:
            for el in l:
                try:
                    el.add_prefix_states(id)
                except AttributeError:
                    continue
    
    #### PROTECTED METHODS ####
    
    def _construct_dictionary(self):
        
        self._content_pointer = {}

        for i in range(len(self._layers)):
            for j in range(len(self._layers[i])):
                if self._layers[i][j].id in self._content_pointer:
                    raise KeyError('')  #TODO
                self._content_pointer[self._layers[i][j].id] = (i, j)

        self._content = {}
        for k in self._content_pointer.keys():
            l, el  = self._content_pointer[k]
            self._content[(l, el)] = self._layers[l][el]

    def _find_attribute_from_name(self, id, function):
        # Search the element
        (l, el) = self._find_content_from_name(id)
        element = self._layers[l][el]

        # Call the function on the element
        try:
            method = getattr(element, function)
        except AttributeError:
            raise AttributeError('') # TODO

        return method

    def _check_layers(self):
        
        # Check layer 0
        if len(self._layers[0]) != 1:
            raise ValueError() # TODO

        if self._layers[0][0].num_upstream != 1:
            raise ValueError() # TODO

        # Check the other layers
        for i in range(1, len(self._layers)):
            num_upstream = 0
            num_downstream = 0
            for el in self._layers[i-1]:
                num_downstream += el.num_downstream
            for el in self._layers[i]:
                num_upstream += el.num_upstream
            
            if num_downstream != num_upstream:
                raise ValueError() # TODO
        
        # Check last layer
        if len(self._layers[-1]) != 1:
            raise ValueError() # TODO

        if self._layers[-1][0].num_downstream!= 1:
            raise ValueError() # TODO

    #### MAGIC METHODS ####
    
    def __copy__(self):
        layers = []
        for l in self._layers:
            layers.append([])
            for el in l:
                layers[-1].append(copy(el))
        return self.__class__(layers = layers,
                              id = self.id,
                              copy_pars = False) # False because the copy is customized here

    def __deepcopy__(self, memo):
        return self.__class__(layers = self._layers,
                              id = self.id,
                              copy_pars = True) # init already implements deepcopy
    
    def __repr__(self):
        str = 'Module: superflexPy\nHRU: {}\n'.format(self.id)
        str += 'Layers:\n'
        id_layer = []
        for l in self._layers:
            id_layer.append([])
            for el in l:
                id_layer[-1].append(el.id)
        
        str += '\t{}\n'.format(id_layer)
        
        for l in self._layers:
            for el in l:
                str += '********************\n'
                str += el.__repr__()
                str += '\n'
        
        return str

if __name__ == '__main__':
    from reservoirs import FastReservoir as FR
    from solver import DmitriSolverPython as Solver

    solver = Solver()

    f1 = FR(parameters = {'k' : 0.1,
                          'alpha' : 2.0},
            states = {'S0' : 10.0},
            solver = solver,
            id = 'FR1')
    f2 = FR(parameters = {'k' : 0.1,
                          'alpha' : 2.0},
            states = {'S0' : 10.0},
            solver = solver,
            id = 'FR2')

    h = HRU(layers = [[f1], [f2]], id = 'HRU')

    print(h.get_parameters_name())
    h.set_parameters({'HRU_FR1_k' : 0.2})
    print(h.get_parameters())
    print(h.get_parameters(['HRU_FR1_k']))
    print(h.get_states_name())
    h.set_states({'HRU_FR1_S0' : 20.0})
    print(h.get_states())
    print(h.get_states(['HRU_FR1_S0']))
    h.reset_states(id = 'FR1')
    h.reset_states()
    h.set_timestep(1.0)
    print(h.get_internal('FR1', 'id'))
    print(h.call_internal(id = 'HRU_FR1', function = 'get_parameters'))
