import dataclasses
import json
import glob
import time
import xml.etree.ElementTree as ET

from collections import deque, defaultdict, Counter
from copy import deepcopy
from functools import reduce
from itertools import combinations, permutations, chain, product

from pathlib import Path
from typing import Dict, FrozenSet, Generator, List, Optional, Set, Tuple, NamedTuple, Iterable

import automata
import networkx
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

import pm4py
from dataclasses import dataclass


# Set this to True just for running the experiments, else keep it False while developing/testing
MAX_PERFORMANCE = True
if MAX_PERFORMANCE:
    automata.base.automaton.global_config.should_validate_automata = False
    automata.base.automaton.global_config.allow_mutable_automata = True

OMEGA_LABEL = 'O'
NFA_INVISIBLE_LABEL = ''

# ======================== DEFINIZIONI DI CLASSI ========================

@dataclasses.dataclass
class PetriNet:
    __slots__ = ('places', 'transitions')

    class TransitionData(NamedTuple):
        id: str
        label: Optional[str]
        pre_set: Set[str]
        post_set: Set[str]

    # We use sets to represent markings, hence we assume the net to be *safe*
    places: Set[str]
    # transition_id -> (label, in_places, out_places)
    transitions: Dict[str, TransitionData]

    def __init__(self, places: Set[str], transitions: Dict[str, TransitionData]):
        self.places = places
        self.transitions = transitions

        assert places.isdisjoint(transitions.keys()), "A transition and a place have the same id"
        assert all(transition.pre_set.issubset(places) for transition in transitions.values()), \
            "Graph is not bipartite or refers to non-existing nodes"
        assert all(transition.post_set.issubset(places) for transition in transitions.values()), \
            "Graph is not bipartite or refers to non-existing nodes"

    def transition_to_label(self, transition_id: str) -> Optional[str]:
        return self.transitions[transition_id].label

    def next_markings(self, marking: FrozenSet[str]) -> Generator[Tuple[str, FrozenSet[str]], None, None]:
        for transition in self.transitions.values():
            if transition.pre_set.issubset(marking):
                # Assume that post_set is a single place for simplicity; adjust as needed
                yield transition.id, marking.difference(transition.pre_set).union(transition.post_set)


@dataclasses.dataclass
class WFNet:
    net: PetriNet
    im: FrozenSet[str]
    fm: FrozenSet[str]

@dataclasses.dataclass
class AlignmentMove:
    move_on_log: Optional[str]
    # Transition ID (or None if log move)
    move_on_model: Optional[str]
    # Transition Label (or None if invisible move).
    model_label: Optional[str]

    @property
    def is_log_move(self) -> bool:
        return self.move_on_model is None

    @property
    def is_model_move(self) -> bool:
        return self.move_on_log is None

    @property
    def is_sync_move(self) -> bool:
        return self.move_on_log is not None and self.move_on_model is not None

    @property
    def is_invisible_move(self) -> bool:
        return self.move_on_model is not None and self.model_label is None

Alignment = List[AlignmentMove]

@dataclasses.dataclass
class AlignedLog:
    variants: List[Tuple[Alignment, int]]

@dataclasses.dataclass
class Dataset:
    name: str
    description: str
    wf_net: WFNet
    aligned_log: AlignedLog

@dataclasses.dataclass
class Template:
    name: str
    parameter_count: int
    activation_templates: Dict[str, Set[str]]
    target_activities: Set[str]
    placeholder_equivalences: List[Set[str]]
    dfa: DFA
    vacuity_condition: DFA
    type_priority: int
    subsumption_hierarchy: int

    def __post_init__(self):
        # We must serialize the placeholders to
        self._invariant_labels = get_invariant_labels(self.dfa)
        self._invariant_labels_vacuity_condition = get_invariant_labels(self.vacuity_condition)
        self._placeholders = [symbol for symbol in self.dfa.input_symbols if symbol != OMEGA_LABEL]
        self._placeholders.sort()
        self._placeholder_offsets = {
            placeholder: i
            for i, equivalence_class in enumerate(self.placeholder_equivalences)
            for placeholder in equivalence_class if placeholder != OMEGA_LABEL
        }
        self._relevant_labels = [symbol for symbol in self.dfa.input_symbols if symbol not in self._invariant_labels]

        # We require the vacuity condition to contain only relevant labels
        assert not get_invariant_labels(self.vacuity_condition)

        # Fixup for the Absence constraint
        if not self._relevant_labels:
            self._relevant_labels = list(self.dfa.input_symbols)

    def __call__(self, *args, **kwargs):
        parameter_map = {k: v for k, v in zip(self._placeholders, args)}
        assert len(parameter_map) == self.parameter_count, \
            f"Rule requires {self.parameter_count} DISTINCT parameters"

        if self._is_repeated_constraint(*args):
            return None

        activations = inject_activation_parameters(self.activation_templates, parameter_map)
        target_activities = set(parameter_map[label] for label in self.target_activities)
        argument_str = ', '.join(args)

        constraint_traits = ConstraintTraits(
            name=f"{self.name}({argument_str})",
            type_priority=self.type_priority,
            subsumption_hierarchy=self.subsumption_hierarchy,
            activations=activations,
            tgt_activities=target_activities,
            is_omega_invariant=OMEGA_LABEL in self._invariant_labels,
            max_label_distance=kwargs["max_label_distance"],
        )

        constraint_dfa = inject_dfa_parameters(self.dfa, parameter_map)
        constraint_vacuity_condition = inject_dfa_parameters(self.vacuity_condition, parameter_map)
        relevant_labels = frozenset(parameter_map[label] for label in self._relevant_labels)

        return Constraint(
            constraint_traits,
            constraint_dfa,
            constraint_vacuity_condition,
            relevant_labels,
        )

    def _is_repeated_constraint(self, *args):
        # placeholder_equivalences groups placeholders that are "equivalent",
        #   i.e. swapping their assigned parameters returns a DFA of the same language
        # If that is the case, then we only need to instantiate these parameters once
        # This code establishes that the parameters must be assigned in increasing lexographic order
        # If the assignment violates it, then it's a repetition
        last_assigned_arg = {}
        for placeholder, arg in zip(self._placeholders, args):
            equivalence_group = self._placeholder_offsets[placeholder]
            if equivalence_group in last_assigned_arg and arg < last_assigned_arg[equivalence_group]:
                # If we are trying to assign a label to an equivalence group that decreases, we have repetition
                return True
            else:
                last_assigned_arg[equivalence_group] = arg

        return False


@dataclasses.dataclass
class ConstraintTraits:
    name: str
    # These are used to order the constraints later
    type_priority: int
    subsumption_hierarchy: int
    activations: List[str]
    tgt_activities: Set[str]
    is_omega_invariant: bool
    max_label_distance: int


@dataclasses.dataclass
class Constraint:
    traits: ConstraintTraits
    dfa: DFA
    vacuity_condition: DFA
    # We could compute this for each newly created constraint,
    #   but that would increase the total runtime, so we take it from the template
    relevant_labels: FrozenSet[str]


@dataclasses.dataclass
class Repository:
    name: str
    max_k: int
    templates: List[Template]

# ======================== IMPORTATORE PNML PERSONALIZZATO ========================

@dataclass
class PnmlImporter:
    namespace: Dict[str, str] = dataclass(init=False)

    def __post_init__(self):
        # Definiamo lo spazio dei nomi PNML standard
        self.namespace = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}

    def apply(self, pnml_file: str) -> Tuple['PetriNet', Set[str], Set[str]]:
        """
        Analizza un file PNML e restituisce la rete di Petri, la marcatura iniziale e finale.

        :param pnml_file: Path al file PNML.
        :return: Tuple contenente PetriNet, marcatura iniziale (im) e marcatura finale (fm).
        """
        tree = ET.parse(pnml_file)
        root = tree.getroot()

        # Estrai le place
        places = set()
        for place in root.findall('.//pnml:place', self.namespace):
            place_id = place.get('id')
            if place_id:
                places.add(place_id)

        # Estrai le transizioni
        transitions = {}
        for transition in root.findall('.//pnml:transition', self.namespace):
            transition_id = transition.get('id')
            # Estrai l'etichetta della transizione, se presente
            label_elem = transition.find('.//pnml:name/pnml:text', self.namespace)
            label = label_elem.text.strip() if label_elem is not None else None
            transitions[transition_id] = PetriNet.TransitionData(
                id=transition_id,
                label=label,
                pre_set=set(),
                post_set=set()
            )

        # Estrai gli archi e popola pre_set e post_set delle transizioni
        for arc in root.findall('.//pnml:arc', self.namespace):
            source = arc.get('source')
            target = arc.get('target')
            if source in places and target in transitions:
                # Arco da place a transizione: pre_set
                transitions[target].pre_set.add(source)
            elif source in transitions and target in places:
                # Arco da transizione a place: post_set
                transitions[source].post_set.add(target)
            else:
                # Altri casi possono essere ignorati o gestiti a seconda delle necessità
                pass

        # Crea l'oggetto PetriNet
        petri_net = PetriNet(
            places=places,
            transitions=transitions
        )

        # Estrai la marcatura iniziale (im)
        im = set()
        for init_marking in root.findall('.//pnml:initialMarking/pnml:text', self.namespace):
            place_id = init_marking.text.strip()
            if place_id in places:
                im.add(place_id)

        # Estrai la marcatura finale (fm)
        fm = set()
        for final_marking in root.findall('.//pnml:finalMarking/pnml:text', self.namespace):
            place_id = final_marking.text.strip()
            if place_id in places:
                fm.add(place_id)

        return petri_net, im, fm

# ======================== FUNZIONI PER RIMUOVERE TRANSAZIONI SILENTI ========================

def remove_silent_transitions(net: PetriNet, im: Set[str], fm: Set[str], max_number_of_nodes: int = 1_000_000) -> DFA:
    """
    Rimuove le transizioni silenti da una rete di Petri convertendola in un DFA.

    :param net: La rete di Petri.
    :param im: Marcatura iniziale.
    :param fm: Marcatura finale.
    :param max_number_of_nodes: Numero massimo di nodi per limitare la complessità.
    :return: Un DFA senza transizioni silenti.
    """
    wf_net = WFNet(net=net, im=frozenset(im), fm=frozenset(fm))
    return get_behavioral_automaton(wf_net, max_number_of_nodes)

def get_behavioral_automaton(wf_net: WFNet, max_number_of_nodes: int = 1_000_000) -> DFA:
    """
    Ottiene l'automa comportamentale (DFA) dalla rete di Petri.

    :param wf_net: La rete di Petri con marcature iniziali e finali.
    :param max_number_of_nodes: Numero massimo di nodi per limitare la complessità.
    :return: Un DFA deterministico.
    """
    nfa = get_reachability_graph(wf_net, max_number_of_nodes)
    dfa = DFA.from_nfa(nfa)
    return dfa

def get_reachability_graph(wf_net: WFNet, max_number_of_nodes: int = 1_000_000) -> NFA:
    """
    Costruisce l'NFA dal reachability graph della rete di Petri.

    :param wf_net: La rete di Petri con marcature iniziali e finali.
    :param max_number_of_nodes: Numero massimo di nodi per limitare la complessità.
    :return: Un NFA rappresentante il reachability graph.
    """
    net, im, fm = wf_net.net, wf_net.im, wf_net.fm
    markings_to_explore = deque()
    seen_markings = set()
    explored_markings = set()
    # {src_marking => {enabled_transition => tgt_marking}}
    nfa = {}
    nfa_start_node = im
    nfa_final_nodes = set()

    markings_to_explore.append(im)
    seen_markings.add(im)

    while markings_to_explore:
        to_explore = markings_to_explore.popleft()
        if to_explore in explored_markings:
            continue

        explored_markings.add(to_explore)
        if to_explore not in nfa:
            nfa[to_explore] = {}

        for transition_id, tgt_marking in net.next_markings(to_explore):
            nfa[to_explore][transition_id] = tgt_marking

            if tgt_marking == fm:
                nfa_final_nodes.add(tgt_marking)

            if tgt_marking not in seen_markings:
                markings_to_explore.append(tgt_marking)
                seen_markings.add(tgt_marking)

            if len(seen_markings) > max_number_of_nodes:
                raise RuntimeError(f"Net is too complex. Exceeded the maximum number "
                                   f"of nodes [{max_number_of_nodes}]. "
                                   f"Try to simplify it or increase the limit")

    # Sanity check
    assert explored_markings == seen_markings

    # Build the NFA's transition function, map to states to int, map None label to ''
    #   We could have done it all in the previous loop but like this we decouple the logic
    state_to_id = {marking: i for i, marking in enumerate(seen_markings)}
    transitions = {state_id: {} for state_id in state_to_id.values()}
    for src_state, state_lookup in nfa.items():
        src_state_id = state_to_id[src_state]

        for transition, tgt_state in state_lookup.items():
            net_transition_label = net.transition_to_label(transition)
            transition_str = NFA_INVISIBLE_LABEL if net_transition_label is None else net_transition_label
            tgt_state_id = state_to_id[tgt_state]

            if transition_str not in transitions[src_state_id]:
                transitions[src_state_id][transition_str] = set()

            transitions[src_state_id][transition_str].add(tgt_state_id)

    start_state = state_to_id[nfa_start_node]
    end_states = {state_to_id[end_state] for end_state in nfa_final_nodes}

    return NFA(
        states={state_id for state_id in state_to_id.values()},
        input_symbols={
            label for state_lookup in transitions.values() for label in state_lookup.keys()
            if label != NFA_INVISIBLE_LABEL
        },
        transitions=transitions,
        initial_state=start_state,
        final_states=end_states,
    )

# ======================== IMPORTATORE DI DOTTORATO ========================

# Il resto delle classi e delle funzioni rimane invariato
# Assicurati che tutte le classi siano definite prima di essere utilizzate

# ======================== MAIN FUNCTION ========================

def main():
    # Definisci il percorso al file PNML
    net, im, fm, = pm4py.read_pnml("/home/l2brb/main/DECpietro/evaluation/bisimulation/reachability_graph/REVISED EASIER.pnml", True)
    print (net, im, fm)

    # Verifica l'importazione
    print("Place IDs:", net.places)
    print("Transitions:")
    for t in net.transitions:
        print(f"  Transition ID: {t.id}, Label: {t.label}, Pre-set: {t.pre_set}, Post-set: {t.post_set}")
    print("Marcatura Iniziale (im):", im)
    print("Marcatura Finale (fm):", fm)

    # Rimuovi le transizioni silenti ottenendo un DFA
    dfa_without_silent = remove_silent_transitions(net, im, fm)

    # Ora puoi utilizzare 'dfa_without_silent' per ulteriori elaborazioni
    print("DFA senza transizioni silenti:")
    print(dfa_without_silent)

    # Continua con il resto delle trasformazioni o analisi
    # ...

if __name__ == '__main__':
    main()