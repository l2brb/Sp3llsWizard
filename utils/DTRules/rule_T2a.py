import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

# RULE T2a - XOR SPLIT
# Task t1 is replaced by two conditional tasks t2 and t3. 
# This transformation rule corresponds to the specialization of a task (e.g. handle order) into two more specialized tasks (e.g. handle small order and handle large order).

# Random activity name generator
def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"

# T2a
def xor_split_transition_t2a(petri_net, t3_name=None):  
    
    # Add new transition t3 and connect to p1 and p2

    if t3_name is None:
        t3_name = generate_random_activity_name()
    
    t3 = PetriNet.Transition(t3_name, label=t3_name)
    petri_net.transitions.add(t3)
    
    p1 = next((p for p in petri_net.places if p.name == 'p1'), None)
    p2 = next((p for p in petri_net.places if p.name == 'p2'), None)
    
    if p1 and p2:
        utils.add_arc_from_to(p1, t3, petri_net)
        utils.add_arc_from_to(t3, p2, petri_net)
    
    return petri_net