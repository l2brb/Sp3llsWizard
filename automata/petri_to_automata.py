#### CONVERSION (tentative) ####



class PetriNet:
    def __init__(self, places, transitions, arcs):
        self.places = {place['id']: 0 for place in places}
        self.transitions = transitions
        self.arcs = arcs
        self.marking = self.generate_initial_marking(places)  
        self.final_marking = self.generate_final_marking(places) 

    def generate_initial_marking(self, places):
        """Generate InitialMarking based on the places exploration"""
        initial_marking = {}
        for place in places:
            initial_marking[place['id']] = int(place.get('initialMarking', 0) or 0)
        return initial_marking

    def generate_final_marking(self, places):
        """Generate FinalMarking based on the places exploration"""
        final_marking = {}
        for place in places:
            final_marking[place['id']] = int(place.get('finalMarking', 0) or 0)
        return final_marking

    def is_enabled(self, transition):
        """Transition verification"""
        input_places = [arc['source'] for arc in self.arcs if arc['target'] == transition['id']]
        for place in input_places:
            if self.marking[place] == 0:  # Verifico se c'è un token nel place
                return False
        return True

    def fire_transition(self, transition):
        """Firing and update"""
        new_marking = self.marking.copy()

        # Tolgo i token dagli input places
        input_places = [arc['source'] for arc in self.arcs if arc['target'] == transition['id']]
        for place in input_places:
            new_marking[place] -= 1

        # Aggiungo i token agli output places
        output_places = [arc['target'] for arc in self.arcs if arc['source'] == transition['id']]
        for place in output_places:
            new_marking[place] += 1

        return new_marking





class FiniteStateAutomaton:
    def __init__(self):
        self.states = []   
        self.transitions = {} 

    def add_state(self, state):
        state_tuple = tuple(state.items())
        if state_tuple not in self.states:
            self.states.append(state_tuple)

    def add_transition(self, from_state, to_state, transition_name):
        from_state_tuple = tuple(from_state.items())
        to_state_tuple = tuple(to_state.items())
        if from_state_tuple not in self.transitions:
            self.transitions[from_state_tuple] = []
        self.transitions[from_state_tuple].append((to_state_tuple, transition_name))

def convert_petri_net_to_fsa(petri_net):
    fsa = FiniteStateAutomaton()
    states_to_explore = [petri_net.marking] 
    explored_states = set()

    while states_to_explore:
        current_marking = states_to_explore.pop(0)
        if current_marking == petri_net.final_marking:
            fsa.add_state(current_marking)
            continue

        if tuple(current_marking.items()) in explored_states:
            continue

        fsa.add_state(current_marking)
        explored_states.add(tuple(current_marking.items()))


        for transition in petri_net.transitions:
            if petri_net.is_enabled(transition):
                new_marking = petri_net.fire_transition(transition)

                fsa.add_state(new_marking)
                fsa.add_transition(current_marking, new_marking, transition['name'])

                if tuple(new_marking.items()) not in explored_states:
                    states_to_explore.append(new_marking)

    return fsa






