import sys, os, json, copy, math, csv, pathlib, pm4py, pandas as pd
from pathlib import Path
from itertools import product
from collections import defaultdict

# -------------------- PREAMBOLO PATH ------------------------------
current_dir  = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import petri_parser

# ------------------------------------------------------------------
# INPUT WN
# ------------------------------------------------------------------
pnml_file_path = "/home/l2brb/main/DECpietro/evaluation/diagnostics/real-world/bpic155f/BPIC15_5f_alpha.pnml"
workflow_net   = petri_parser.parse_wn_from_pnml(pnml_file_path)

# ------------------------------------------------------------------
# Mapping WN: transition-id → label  +  helper id2lab
# ------------------------------------------------------------------
Map = {}
for tr in workflow_net["transitions"]:
    label = "τ" if tr["is_tau"] else tr["name"]
    Map[tr["id"]] = label
print(Map)

def id2lab(tid):
    return Map.get(tid, "?")

# ------------------------------------------------------------------
# L-1 globale (inverse mapping)
# ------------------------------------------------------------------
L_inv = defaultdict(list)
for t_id, lab in Map.items():
    L_inv[lab].append(t_id)

# ------------------------------------------------------------------
# JSON Declare spec

declare_path = Path("/home/l2brb/main/DECpietro/evaluation/diagnostics/real-world/bpic155f/BPIC15_5f_constraints.json")
model_json   = json.loads(declare_path.read_text())



# ------------------------------------------------------------------
# AUTOMI  (End / AtMost1 / AltPrecedence)

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
            self.msg.append(f"[pos {self.pos}] End({labs}) violated (id {ids})")
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
            if t in self.Y:                                   # violazione
                labsX = ",".join(sorted(id2lab(x) for x in self.X))
                labsY = ",".join(sorted(id2lab(y) for y in self.Y))
                idsY  = ",".join(sorted(self.Y))
                self.msg.append(
                    f"[pos {self.pos}] AltPrec({{{labsX}}},{{{labsY}}}): "
                    f"violated in (id {idsY})"
                )
            elif t in self.X:
                self.waiting_target = False
        else:                                                 # aspetto Y
            if t in self.Y:
                self.waiting_target = True

    def result(self):
        return len(self.msg), self.msg

# ------------------------------------------------------------------
# Build constraints 

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
# Allineamento per singola traccia
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

LOG_PATH   = "/home/l2brb/main/DECpietro/evaluation/performance/realworld/logs/BPIC155f/BPIC15_5f.xes"
OUTPUT_CSV = "/home/l2brb/main/DECpietro/conformance/incrementale/alignment_results.csv"

log_obj = pm4py.read_xes(LOG_PATH)
df      = pm4py.convert_to_dataframe(log_obj).sort_values(
              ["case:concept:name", "time:timestamp"])

# opzionale mapping label-log → label-modello
LOG_LABEL_MAP = {}

def norm_label(lbl): return LOG_LABEL_MAP.get(lbl, lbl)

def extract_labels_df(sub_df, attr="concept:name"):
    return [lab for lab in map(norm_label, sub_df[attr]) if lab in L_inv]

# ------------------------------------------------------------------
# LOOP TRACCE  +  outCSV

results, sum_cost, max_cost = [], 0, 0
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["trace_idx","cost","realization_ids","realization_labels","violations"])


    for idx, (_, sub) in enumerate(df.groupby("case:concept:name")):
        labels = extract_labels_df(sub)
        cost, real, detail = align_trace(labels)

        writer.writerow([idx,
                         cost if math.isfinite(cost) else "inf",
                         ";".join(real),
                         ";".join(id2lab(r) for r in real), 
                         " | ".join(detail)])

        results.append(cost)
        sum_cost += (cost if math.isfinite(cost) else 0)
        max_cost  = max(max_cost, cost)

# ------------------------------------------------------------------
# METRICS

n = len(results)
finite = [c for c in results if math.isfinite(c)]
avg_cost = sum(finite)/len(finite) if finite else 0
perc_ok  = results.count(0)/n*100 if n else 0

print("------------------------------------------------------------------")
print(f"Log file        : {pathlib.Path(LOG_PATH).name}")
print(f"Trace analysed  : {n}")
print(f"Mean violation  : {avg_cost:.2f}")
print(f"OK percentage   : {perc_ok:.1f}%")
print(f"Max violation   : {max_cost}")
print(f"Results in      : {os.path.abspath(OUTPUT_CSV)}")
