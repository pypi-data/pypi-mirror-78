from common_class import CommonClass

class Model(CommonClass):

    def __init__(self, catchments, network):
        self._content = catchments
        self._downstream = network

        self._build_network()

    #### METHODS FOR THE USER ####

    def get_output(self, solve = True):
    
        # Keep track of the solved catchemts
        solved = {k : False for k in self._upstream.keys()}
        output = {}

        # Solve first the headwater
        for cat in self._headwater:
            output[cat] = self._content[self._content_pointer[cat]].get_output(solve)
            solved[cat] = True

        if len(self._content) != len(self._headwater):
            completed = False
        else:
            completed = True

        while not completed:
            for cat in self._upstream.keys():
                if not solved[cat]:
                    # Check if all the upstrams have been solves
                    solvable = True
                    for cat_up in self._upstream[cat]:
                        if not solved[cat_up]:
                            solvable = False
                    if solvable:
                        # Solve the current cathcment
                        loc_out = self._content[self._content_pointer[cat]].get_output(solve)

                        # Multiply for the area
                        for i in range(len(loc_out)):
                            loc_out[i] *= self._content[self._content_pointer[cat]].area

                        for cat_up in self._upstream[cat]:
                            routed_out = self._content[self._content_pointer[cat_up]].external_routing(output[cat_up]) # TODO: double check
                            if len(loc_out) != len(routed_out):
                                raise RuntimeError() # TODO
                            for i in range(len(loc_out)):
                                loc_out[i] += routed_out[i] * self._total_area[cat_up]
                        
                        for i in range(len(loc_out)):
                            loc_out[i] /= self._total_area[cat]

                        output[cat] = loc_out
                        solved[cat] = True
                        
                        if self._downstream[cat] is None:
                            completed = True
        
        return output
    
    def get_internal(self, id, attribute):

        cat_num, ele = self._find_attribute_from_name(id)

        if ele:
            return self._content[cat_num].get_internal(id, attribute)
        else:
            try:
                method = getattr(self._content[cat_num], attribute)
                return method
            except AttributeError:
                raise AttributeError('') # TODO

    def call_internal(self, id, function, **kwargs):
        
        cat_num, ele = self._find_attribute_from_name(id)

        if ele:
            return self._content[cat_num].call_internal(id, function, **kwargs)
        else:
            try:
                method = getattr(self._content[cat_num], function)
                return method(**kwargs)
            except AttributeError:
                raise AttributeError('') # TODO

    #### PROTECTED METHODS ####

    def _build_network(self):

        # Find the upstream catchments
        self._upstream = {k : [] for k in self._downstream.keys()}
        for cat in self._downstream.keys():
            if self._downstream[cat] is not None:
                self._upstream[self._downstream[cat]].append(cat)
        
        for cat in self._upstream.keys():
            if len(self._upstream[cat]) == 0:
                self._upstream[cat] = None

        # Find the headwater
        self._headwater = [k for k in self._upstream.keys() if self._upstream[k] is None]

        # Build the map from id to index
        self._content_pointer = {cat.id : i for i, cat in enumerate(self._content)}

        # Calculate the total area
        self._total_area = {}
        solved = {k : False for k in self._upstream.keys()}

        # First the headwaters
        for cat in self._headwater:
            self._total_area[cat] = self._content[self._content_pointer[cat]].area
            solved[cat] = True

        if len(self._content) != len(self._headwater):
            completed = False
        else:
            completed = True

        while not completed:
            for cat in self._upstream.keys():
                if not solved[cat]:
                    # Check if all the upstrams have been solves
                    solvable = True
                    for cat_up in self._upstream[cat]:
                        if not solved[cat_up]:
                            solvable = False
                    if solvable:
                        # Solve the current cathcment
                        area = self._content[self._content_pointer[cat]].area

                        for cat_up in self._upstream[cat]:
                            area += self._total_area[cat_up]
                        
                        self._total_area[cat] = area
                        solved[cat] = True
                        
                        if self._downstream[cat] is None:
                            completed = True

    def _find_attribute_from_name(self, id):

        splitted = id.split('_')

        cat_num = self._find_content_from_name(id)

        if len(splitted) >= 2:
            return (cat_num, True)  # We are looking for a HRU or an element
        else:
            return (cat_num, False)

    #### MAGIC METHODS ####

    def __copy__(self):
        raise AttributeError() # TODO
    
    def __deepcopy__(self, memo):
        raise AttributeError() # TODO
    
    def __repr__(self):
        str = 'Module: superflexPy\nModel class\n'
        str += 'Cathcments:\n'
        str += '\t{}\n'.format(list(self._content_pointer.keys()))
        str += 'Network:\n'
        str += '\t{}\n'.format(self._downstream)
        
        for cat in self._content:
            str += '********************\n'
            str += '********************\n'
            str += '********************\n'
            str += cat.__repr__()
            str += '\n'
            str += '\n'

        return str

if __name__ == '__main__':
    from reservoirs import FastReservoir as FR
    from solver import DmitriSolverPython as Solver
    from hru import HRU
    from catchment import Catchment

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

    m = Model(catchments = [c],
              network = {'C1' : None})

    print(m.get_parameters_name())
    m.set_parameters({'HRU1_FR1_k' : 0.2})
    print(m.get_parameters())
    print(m.get_parameters(['HRU1_FR1_k']))
    print(m.get_states_name())
    m.set_states({'C1_HRU1_FR1_S0' : 20.0})
    print(m.get_states())
    print(m.get_states(['C1_HRU1_FR1_S0']))
    m.reset_states(id = 'C1_HRU1_FR1')
    m.reset_states()
    m.set_timestep(1.0)
    print(m.get_internal('C1_HRU1_FR1', 'id'))
    print(m.call_internal(id = 'C1_HRU1_FR1', function = 'get_parameters'))
    print(m.get_internal('C1_HRU1', 'id'))
    print(m.call_internal(id = 'C1_HRU1', function = 'get_parameters'))
    print(m.get_internal('C1', 'id'))
    print(m.call_internal(id = 'C1', function = 'get_parameters'))