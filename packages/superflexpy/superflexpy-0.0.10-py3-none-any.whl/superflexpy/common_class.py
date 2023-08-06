class CommonClass(object):

    def get_parameters(self, names = None):
        parameters = {}

        if names is None:
            for c in self._content_pointer.keys():
                position = self._content_pointer[c]
                try:
                    cont_pars = self._content[position].get_parameters()
                except AttributeError:
                    continue
                for k in cont_pars:
                    if k not in parameters:
                        parameters[k] = cont_pars[k]
        else:
            for n in names:
                position = self._find_content_from_name(n)
                if position is None:
                    for c in self._content_pointer.keys():
                        position = self._content_pointer[c]
                        try:
                            cont_pars = self._content[position].get_parameters([n])
                            break
                        except (AttributeError, KeyError): # Attribute error because the content may not have the method, Key error because the parameter may not belong to the content
                            continue
                else:
                    cont_pars = self._content[position].get_parameters([n])
                
                parameters = {**parameters, **cont_pars}
        
        return parameters

    def get_parameters_name(self):
        return list(self.get_parameters().keys())

    def _find_content_from_name(self, name):
        
        splitted_name = name.split('_')

        try:
            class_id = self.id
        except AttributeError:
            class_id = None

        if class_id is not None:
            # HRU or Catchment
            if class_id in splitted_name:
                ind = splitted_name.index(class_id)
            else:
                ind = -1 # TODO: check

            position = self._content_pointer[splitted_name[ind + 1]]
        else:
            # Model
            for c in self._content_pointer.keys():
                if c in splitted_name:
                    position = self._content_pointer[c]
                else:
                    position = None

        return position

    def set_parameters(self, parameters):

        for p in parameters.keys():
            position = self._find_content_from_name(p)

            if position is None:
                for c in self._content_pointer.keys():
                    try:
                        position = self._content_pointer[c]
                        self._content[position].set_parameters({p : parameters[p]})
                        break
                    except (KeyError, ValueError):
                        continue
            else:
                self._content[position].set_parameters({p : parameters[p]})

    def get_states(self, names = None):
        states = {}

        if names is None:
            for c in self._content_pointer.keys():
                position = self._content_pointer[c]
                try:
                    cont_st = self._content[position].get_states()
                except AttributeError:
                    continue
                for k in cont_st:
                    if k not in states:
                        states[k] = cont_st[k]
        else:
            for n in names:
                position = self._find_content_from_name(n)
                if position is None:
                    for c in self._content_pointer.keys():
                        position = self._content_pointer[c]
                        try:
                            cont_st = self._content[position].get_states([n])
                            break
                        except (AttributeError, KeyError): # Attribute error because the content may not have the method, Key error because the parameter may not belong to the content
                            continue
                else:
                    cont_st = self._content[position].get_states([n])
                
                states = {**states, **cont_st}
        
        return states

    def get_states_name(self):
        return list(self.get_states().keys())

    def set_states(self, states):

        for s in states.keys():
            position = self._find_content_from_name(s)

            if position is None:
                for c in self._content_pointer.keys():
                    try:
                        position = self._content_pointer[c]
                        self._content[position].set_states({s : states[s]})
                        break
                    except (KeyError, ValueError):
                        continue
            else:
                self._content[position].set_states({s : states[s]})

    def reset_states(self, id = None):

        if id is None:
            for c in self._content_pointer.keys():
                position = self._content_pointer[c]
                try:
                    self._content[position].reset_states()
                except AttributeError:
                    continue
        else:
            if isinstance(id, str):
                id = [id]
            for i in id:
                position = self._find_content_from_name(i)

                # TODO: With states we do not have the case position = None
                self._content[position].reset_states()

    def get_timestep(self):
        return self._dt

    def set_timestep(self, dt):
        self._dt = dt

        for c in self._content_pointer.keys():
            position = self._content_pointer[c]

            try:
                self._content[position].set_timestep(dt)
            except AttributeError:
                continue

    def define_solver(self, solver):
        for c in self._content_pointer.keys():
            position = self._content_pointer[c]

            try:
                self._content[position].define_solver(solver)
            except AttributeError:
                continue