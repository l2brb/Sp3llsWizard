import csv
import pandas as pd

"""
translate_to_DECLARE
---------------------------
Translate the Workflow Net to DECLARE constraints.

Args:
- workflow_net: Dictionary representing the Workflow Net.

Returns:
- constraints: List of DECLARE constraints.
"""

# EXISTANCE CONTRAINTS 

# Init
def get_init_constraint(workflow_net):
    init_constraint = ""
    initial_place_id = None
    for place in workflow_net["places"]:
        if "initialMarking" in place and place["initialMarking"] == "1":
            initial_place_id = place["id"]
            #print(initial_place_id)
            break

    if initial_place_id:
        for arc in workflow_net["arcs"]:
            if arc["source"] == initial_place_id:
                next_transition_id = arc["target"]
                #print(next_transition_id)
                next_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == next_transition_id][0]
                #print(next_transition_name)
                init_constraint += f"{next_transition_name}"
                #print(type(init_constraint))

    return {"Init": init_constraint}


# End
def get_end_constraint(workflow_net):
    end_constraint = ""
    final_place_id = None
    for place in workflow_net["places"]:
        if "finalMarking" in place and place["finalMarking"] == "1":
            final_place_id = place["id"]
            #print(final_place_id)
            break

    if final_place_id:
        for arc in workflow_net["arcs"]:
            if arc["target"] == final_place_id:
                prev_transition_id = arc["source"]
                #print(prev_transition_id)
                prev_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == prev_transition_id][0]
                end_constraint += f"{prev_transition_name}"

    return {"End": end_constraint}


# RELATION CONSTRAINTS

    
# Alternate Precedence
def get_alternate_precedence(workflow_net):
    constraints = {}
    for place in workflow_net["places"]:
        if place.get("initialMarking") != "1" and place.get("finalMarking") != "1":
            a = set(arc["source"] for arc in workflow_net["arcs"] if arc["source"] == place["id"])
            #print(a)
            for source in a:
                for arc in workflow_net["arcs"]:
                    for transition in workflow_net["transitions"]:
                        if arc["source"] == source and arc["target"] == transition["id"]:
                            constraints[source] = arc["target"]
    #print(constraints.keys())
    altprecedence_constraint = {}
    for key in constraints.keys():
        for arc in workflow_net["arcs"]:
            if arc["target"] == key:
                altprecedence_constraint[arc["source"]] = constraints[key]
    #print(altprecedence_constraint)

    altprecedence_constraint_name = {}
    for el in altprecedence_constraint:
        for t in workflow_net["transitions"]:
            if t["id"] == el:
                print(el , t["name"])
                altprecedence_constraint_name[t["name"]] = altprecedence_constraint[t["name"]]


    return {"AltPrecedence": altprecedence_constraint}    

def translation(value):
    for t in workflow_net["transitions"]:
            if t["id"] == value:
                return t["name"]
    return None

# Alternate Response
def get_alternate_response(workflow_net):
    constraints = {}
    for place in workflow_net["places"]:
        if place.get("initialMarking") != "1" and place.get("finalMarking") != "1":
            b = set(arc["target"] for arc in workflow_net["arcs"] if arc["target"] == place["id"])
            #print(b)
            for target in b:
                for arc in workflow_net["arcs"]:
                    for transition in workflow_net["transitions"]:
                        if arc["target"] == target and arc["source"] == transition["id"]:
                            constraints[arc["source"]] = target
    #print(constraints.values())
    #print(constraints)    
    altresponse_constraint = {}
    for key, val in constraints.items():
        for arc in workflow_net["arcs"]:
            if arc["source"] == val:
                altresponse_constraint[key] = arc["target"]
    #print(altresponse_constraint)  


    return {"AltResponse": altresponse_constraint}
        

# Main Function
def translate_to_DEC(workflow_net):
    constraints = get_init_constraint(workflow_net)
    constraints = constraints | get_end_constraint(workflow_net)
    constraints = constraints | get_alternate_precedence(workflow_net)
    constraints = constraints | get_alternate_response(workflow_net)
  
 
    return constraints


