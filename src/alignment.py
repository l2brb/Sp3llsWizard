import sys, os, json, copy, math, csv, pathlib, pm4py, pandas as pd
from pathlib import Path
from itertools import product
from collections import defaultdict

# ------------------------------------------------------------------
# SET WD 
current_dir  = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def run_conformance(               # ► nuova funzione
    declare_json_path: str,
    log_path: str,
    output_csv: str
):
# ------------------------------------------------------------------
# INPUT PATHS


    DECLARE_PATH = Path(declare_json_path)   # ► prende dal parametro
    LOG_PATH     = log_path            
    OUTPUT_CSV   = output_csv          



# ------------------------------------------------------------------
# JSON Declare spec

    model_json   = json.loads(DECLARE_PATH.read_text())
    #print(json.dumps(model_json, indent=4))  


# ------------------------------------------------------------------
# Mapping
# Mapping: transition-id → label  (e vice-versa)  **usando il JSON**

    trans_map = model_json["transitionMap"]      # label → [id, id, …]
    #print(trans_map)
    # id → label
    Map = {tid: lab for lab, tids in trans_map.items() for tid in tids}
    #print(Map)  # per debug

    def id2lab(tid):
        return Map.get(tid, "?")

    # label → [ids] (inverse mapping)
    L_inv = defaultdict(list, trans_map) 
    #print(L_inv)


    # ------------------------------------------------------------------
    # AUTOMATA  (End / AtMost1 / AltPrecedence)

    class End:
        def __init__(self, alpha):
            self.X = set(alpha)
            self.after_x = False
            self.bad_tail = False
            self.msg = []
            self.pos = -1

        def step(self, t):
            self.pos += 1
            if t in self.X:
                self.after_x, self.bad_tail = True, False
            elif self.after_x and not self.bad_tail:
                labs = ",".join(id2lab(x) for x in self.X)
                ids  = ",".join(self.X)
                self.msg.append(f"[pos {self.pos}] End({labs}) violated by (id {ids})")
                self.bad_tail = True

        def result(self):
            if not self.after_x:
                labs = ",".join(id2lab(x) for x in self.X)
                ids  = ",".join(self.X)
                self.msg.append(f"[pos END] End({labs}) missing (id {ids})")
            return len(self.msg), self.msg


    class AtMost1:
        def __init__(self, alpha):
            self.X = set(alpha); self.count = 0
            self.msg, self.pos = [], -1

        def step(self, t):
            self.pos += 1
            if t in self.X:
                self.count += 1
                if self.count > 1:
                    labs = ",".join(id2lab(x) for x in self.X)
                    ids  = ",".join(self.X)
                    self.msg.append(f"[pos {self.pos}] AtMost1({labs}) repeated (id {ids})")

        def result(self):
            return len(self.msg), self.msg


    class AltPrecedence:
        def __init__(self, Target, Activator):
            self.X, self.Y = set(Target), set(Activator)
            self.waiting_target = True
            self.msg, self.pos = [], -1

        def step(self, t):
            self.pos += 1
            if self.waiting_target:
                if t in self.Y:                                  
                    labsX = ",".join(sorted(id2lab(x) for x in self.X))
                    labsY = ",".join(sorted(id2lab(y) for y in self.Y))
                    idsY  = ",".join(sorted(self.Y))
                    self.msg.append(
                        f"[pos {self.pos}] AltPrec({{{labsX}}},{{{labsY}}}): "
                        f"violated by (id {idsY})"
                    )
                elif t in self.X:
                    self.waiting_target = False
            else:                                                 
                if t in self.Y:
                    self.waiting_target = True

        def result(self):
            return len(self.msg), self.msg

    """
    # DEPRECATED
    # ------------------------------------------------------------------
    # Building constraints 

    def build_constraints(spec_json):
        constraints = []
        for c in spec_json["constraints"]:
            tmpl, param = c["template"], c["parameters"]
            if tmpl == "End":
                constraints.append(End(*param))
            elif tmpl == "Atmost1":
                constraints.append(AtMost1(*param))
            elif tmpl == "AlternatePrecedence":
                constraints.append(AltPrecedence(param[0], param[1]))
        return constraints

    CONSTRAINTS = build_constraints(model_json)"""


    # ------------------------------- utility
    def names_to_ids(names, trans_map):
        ids = []
        for n in names:
            if n in trans_map:           # label normale
                ids.extend(trans_map[n])
            else:                        # placeholder START/END ecc.
                ids.append(n)
        return ids

    # ------------------------------- build_constraints
    def build_constraints(spec_json):
        trans_map = spec_json["transitionMap"]
        n2i = lambda lst: names_to_ids(lst, trans_map)

        constraints = []
        for c in spec_json["constraints"]:
            if c["template"] == "End":
                constraints.append(End(n2i(c["parameters"][0])))
            elif c["template"] == "Atmost1":
                constraints.append(AtMost1(n2i(c["parameters"][0])))
            elif c["template"] == "AlternatePrecedence":
                p, s = c["parameters"]
                constraints.append(AltPrecedence(n2i(p), n2i(s)))
        return constraints



    CONSTRAINTS = build_constraints(model_json)
# ------------------------------------------------------------------
    # Cost function

    def declare_cost(realization):
        constraints = copy.deepcopy(CONSTRAINTS)
        for t in realization:
            for c in constraints:
                c.step(t)
        total, details = 0, []
        for c in constraints:
            v, msg = c.result()
            total += v
            details.extend(msg)
        return total, details

# ------------------------------------------------------------------
# Alignment function per trance

    def align_trace(trace_labels):
        unknown = [lab for lab in trace_labels if lab not in L_inv]
        if unknown:
            return math.inf, tuple(), [f"unknown label {set(unknown)}"]

        local_inv = {lab: L_inv[lab] for lab in set(trace_labels)}
        choices   = [local_inv[lab] for lab in trace_labels]

        best_cost, sols, dets = math.inf, [], []
        for combo in product(*choices):
            cost, detail = declare_cost(combo)
            if cost < best_cost:
                best_cost, sols, dets = cost, [combo], [detail]
            elif cost == best_cost:
                sols.append(combo); dets.append(detail)

        idx = sols.index(min(sols)) 
        return best_cost, sols[idx], dets[idx]

# ------------------------------------------------------------------
# Log

    log_obj = pm4py.read_xes(LOG_PATH)
    df      = pm4py.convert_to_dataframe(log_obj).sort_values(["case:concept:name", "time:timestamp"])

    # opzionale mapping label-log → label-modello
    LOG_LABEL_MAP = {}

    def norm_label(lbl): return LOG_LABEL_MAP.get(lbl, lbl)

    def extract_labels_df(sub_df, attr="concept:name"):
        return [lab for lab in map(norm_label, sub_df[attr]) if lab in L_inv]


# ------------------------------------------------------------------
    # LOOP TRACCE  +  outCSV

    results, sum_cost, max_cost, min_cost = [], 0, 0, 0
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "case_id",
            "trace_len",
            "cost",
            "realization_ids",
            "realization_labels",
            "violations"
            ])


        for case_name, sub in df.groupby("case:concept:name"):
            labels = extract_labels_df(sub)
            cost, real, detail = align_trace(labels)

            writer.writerow([case_name,
                            len(labels),  
                            cost if math.isfinite(cost) else "inf",
                            ";".join(real),
                            ";".join(id2lab(r) for r in real), 
                            " | ".join(detail)])

            results.append(cost)
            sum_cost += (cost if math.isfinite(cost) else 0)
            max_cost  = max(max_cost, cost)
            min_cost = min(min_cost, cost) if results else cost


# ------------------------------------------------------------------
    # METRICS

    n = len(results)
    finite = [c for c in results if math.isfinite(c)]
    avg_cost = sum(finite)/len(finite) if finite else 0
    perc_ok  = results.count(0)/n*100 if n else 0

    # print("------------------------------------------------------------------")
    # print(f"Log file        : {pathlib.Path(LOG_PATH).name}")
    # print(f"Processed traces  : {n}")
    # print(f"Mean violation cost  : {avg_cost:.2f}")
    # print(f"Max violation cost   : {max_cost}")
    # print(f"Min violation cost   : {min_cost}")
    # print(f"OK percentage   : {perc_ok:.1f}%")
    # print(f"Results in      : {os.path.abspath(OUTPUT_CSV)}")
