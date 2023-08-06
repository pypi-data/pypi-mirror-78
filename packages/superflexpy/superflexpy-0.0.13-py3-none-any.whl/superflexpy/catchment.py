from copy import copy, deepcopy
from common_class import CommonClass

class Catchment(CommonClass):

    def __init__(self, hrus, weights_in, weights_out, area, id, shared_parameters=True):
        """
        Area is the area of the subcatchment. If the catchment contains others,
        the value is the net value (total - subcatchments)
        """

        self.id = id

        self._content = []
        for h in hrus:
            if shared_parameters:
                self._content.append(copy(h))
            else:
                self._content.append(deepcopy(h))
                self.add_prefix_parameters(id)

        self.area = area
        self._content_pointer = {hru.id : i 
                                 for i, hru in enumerate(self._content)}
        self._weights_in = deepcopy(weights_in)
        self._weights_out = deepcopy(weights_out)
        self.add_prefix_states(id)

    #### METHODS FOR THE USER ####

    def set_input(self, input):
        self.input = input
    
    def get_output(self, solve = True):  # TODO: test

        # Set the inputs
        if isinstance(self._weights_in[0], float):
            for h, w in zip(self._content, self._weights_in):
                h.set_input([i * w for i in self.input])
        else:
            for h, w in zip(self._content, self._weights_in):
                loc_input = []
                for j in len(self.input):
                    if w[j] is None:
                        continue
                    loc_input.append(self.input[j] * w[j])
                h.set_input(loc_input)

        # Calculate output
        if isinstance(self._weights_out[0], float):
            for i, (h, w) in enumerate(zip(self._content, self._weights_out)):
                loc_out = h.get_output(solve)

                if i == 0:
                    output = [o*w for o in loc_out]
                else:
                    for j in range(len(output)):
                        output[j] += loc_out[j]
        else:
            for i, (h, w) in enumerate(zip(self._content, self._weights_out)):
                loc_out = h.get_output(solve)
                out_count = 0

                if i == 0:
                    output = []
                    for j in range(len(w)):
                        if w[j] is None:
                            output.append(0)
                        else:
                            output.append(loc_out[out_count])
                            out_count += 1
                else:
                    for j in range(len(w)):
                        if w[j] is None:
                            continue
                        else:
                            output[j] += loc_out[out_count]
                            out_count += 1

        return self._internal_routing(output)
    
    def get_internal(self, id, attribute):

        hru_num, ele = self._find_attribute_from_name(id)

        if ele:
            return self._content[hru_num].get_internal(id, attribute)
        else:
            try:
                method = getattr(self._content[hru_num], attribute)
                return method
            except AttributeError:
                raise AttributeError('') # TODO

    def call_internal(self, id, function, **kwargs):
        
        hru_num, ele = self._find_attribute_from_name(id)

        if ele:
            return self._content[hru_num].call_internal(id, function, **kwargs)
        else:
            try:
                method = getattr(self._content[hru_num], function)
                return method(**kwargs)
            except AttributeError:
                raise AttributeError('') # TODO

    #### METHODS USED BY THE FRAMEWORK ####

    def add_prefix_parameters(self, id):
        for h in self._content:
            h.add_prefix_parameters(id)

    def add_prefix_states(self, id):
        for h in self._content:
            h.add_prefix_states(id)
    
    def external_routing(self, flux):
        """
        External routing is the one that affect the flux moving from the
        outflow of this catchment to the outflow of the one downstream.
        This function must be used by the Model.
        """

        # No routing
        return flux

    #### PROTECTED METHODS ####
    
    def _find_attribute_from_name(self, id):

        splitted = id.split('_')

        hru_num = self._find_content_from_name(id)

        if len(splitted) == 3:
            return (hru_num, True)  # We are looking for an element
        else:
            return (hru_num, False)

    def _internal_routing(self, flux):
        """
        Internal routing is the one that affects the flux coming to the HRUs
        and reaching the outflow of the catchment. This function is internally
        used by the Catchment.
        """

        # No routing
        return flux    

    #### MAGIC METHODS ####
    
    def __copy__(self):
        raise AttributeError('')  # TODO

    def __deepcopy__(self, memo):
        raise AttributeError('')  # TODO

    def __repr__(self):
        str = 'Module: superflexPy\nCatchment: {}\n'.format(self.id)
        str += 'HRUs:\n'
        str += '\t{}\n'.format([h.id for h in self._content])
        str += 'Weights in:\n'
        str += '\t{}\n'.format(self._weights_in)
        str += 'Weights out:\n'
        str += '\t{}\n'.format(self._weights_out)
        
        for h in self._content:
            str += '********************\n'
            str += '********************\n'
            str += h.__repr__()
            str += '\n'

        return str

if __name__ == '__main__':
    from reservoirs import FastReservoir as FR
    from solver import DmitriSolverPython as Solver
    from hru import HRU

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

    h1 = HRU(layers = [[f1], [f2]], id = 'HRU1')
    h2 = HRU(layers = [[f1]], id = 'HRU2')

    c = Catchment(hrus = [h1, h2],
                  weights_in = [0.4, 0.6],
                  weights_out = [0.4, 0.6],
                  area = 1.0,
                  id = 'C1')

    print(c.get_parameters_name())
    c.set_parameters({'HRU1_FR1_k' : 0.2})
    print(c.get_parameters())
    print(c.get_parameters(['HRU1_FR1_k']))
    print(c.get_states_name())
    c.set_states({'C1_HRU1_FR1_S0' : 20.0})
    print(c.get_states())
    print(c.get_states(['C1_HRU1_FR1_S0']))
    c.reset_states(id = 'HRU1_FR1')
    c.reset_states()
    c.set_timestep(1.0)
    print(c.get_internal('C1_HRU1_FR1', 'id'))
    print(c.call_internal(id = 'C1_HRU1_FR1', function = 'get_parameters'))
    print(c.get_internal('C1_HRU1', 'id'))
    print(c.call_internal(id = 'C1_HRU1', function = 'get_parameters'))