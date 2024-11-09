from lxml import etree

""" 
parse_wn_from_pnml
---------------------------
Parse the Workflow Net from a PNML file.

 Args:
- file_path: Path to the PNML file containing the Workflow Net.

Returns:
- workflow_net: Dictionary representing the parsed Workflow Net.
"""

def parse_wn_from_pnml(file_path):
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()

        workflow_net = {
            "places": [],
            "transitions": [],
            "arcs": []
        }

        # Parsing places
        for place in root.findall('.//place'):
            place_id = place.get("id")
            place_name = place.findtext('.//name/text')
            initial_marking = place.findtext('.//initialMarking/text')

            if place_id is not None and place_name is not None:
                workflow_net["places"].append({
                 "id": place_id,
                 "name": place_name,
                 "initialMarking": initial_marking
            })

        # Parsing transitions
        for transition in root.findall('.//transition'):
            transition_id = transition.get("id")
            transition_name = transition.findtext('.//name/text')

            workflow_net["transitions"].append({
                "id": transition_id,
                "name": transition_name
            })


        # Parsing arcs
        for arc in root.findall('.//arc'):
            arc_source = arc.get("source")
            arc_target = arc.get("target")

            workflow_net["arcs"].append({
                "source": arc_source,
                "target": arc_target
            })

        # Parsing final markings
        final_markings = root.find('.//finalmarkings')
        if final_markings is not None:
            for marking in final_markings.findall('.//place'):
                place_idref = marking.get("idref")
                for place in workflow_net["places"]:
                    if place["id"] == place_idref:
                        place["finalMarking"] = "1"

        return workflow_net

    except FileNotFoundError:
        #print(f"File '{file_path}' not found.")
        return None




"""# Example usage
if __name__ == "__main__":
    file_path = "/Users/luca/Documents/^main/DECpietro/petri_test/petri_pharma.pnml" 
    workflow_net = parse_wn_from_pnml(file_path)
    if workflow_net:
        print("Workflow Net parsed successfully:")
        print(workflow_net)

"""