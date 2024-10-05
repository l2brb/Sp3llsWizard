import petri_parser_automata
import petri_to_automata

def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/test/PLG/test_xor/xor_pm4py.pnml"
    petri_net = petri_parser_automata.parse_pn_from_pnml(pnml_file_path)


    if petri_net:
        print("WORKFLOW NET PARSED SUCCESFULLY.")
        print(petri_net)

        petri_net_class = petri_to_automata.PetriNet(petri_net['places'], petri_net['transitions'], petri_net['arcs'])
        fsa = petri_to_automata.convert_petri_net_to_fsa(petri_net_class)
        print("FSM GENERATED SUCCESFULLY.")
        print("Stati dell'automa:", fsa.states)
        print("Transizioni dell'automa:", fsa.transitions)


if __name__ == "__main__":
    main()
