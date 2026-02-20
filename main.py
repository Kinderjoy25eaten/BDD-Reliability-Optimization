import time
import random
import matplotlib.pyplot as plt

class BDDEngine:
    def __init__(self):
        self.unique_table = {}  # (var, high, low) -> node_id
        self.computed_table = {} # (op, id1, id2) -> result_id
        self.next_id = 2
        self.recursive_calls = 0
        self.TRUE = 1
        self.FALSE = 0

    def get_node(self, var, high, low):
        if high == low: return high
        key = (var, high, low)
        if key not in self.unique_table:
            self.unique_table[key] = self.next_id
            self.next_id += 1
        return self.unique_table[key]

    def and_op(self, f, g):
        self.recursive_calls += 1
        if f == self.FALSE or g == self.FALSE: return self.FALSE
        if f == self.TRUE: return g
        if g == self.TRUE: return f
        
        key = ('AND', min(f, g), max(f, g))
        if key in self.computed_table: return self.computed_table[key]

        # Simplified node lookup for the simulation
        f_info = [k for k, v in self.unique_table.items() if v == f][0]
        g_info = [k for k, v in self.unique_table.items() if v == g][0]
        
        v_f, f_h, f_l = f_info
        v_g, g_h, g_l = g_info
        top_var = min(v_f, v_g)
        
        fh, fl = (f_h, f_l) if v_f == top_var else (f, f)
        gh, gl = (g_h, g_l) if v_g == top_var else (g, g)

        res_h = self.and_op(fh, gh)
        res_l = self.and_op(fl, gl)
        res = self.get_node(top_var, res_h, res_l)
        self.computed_table[key] = res
        return res

def run_simulation(phase_counts, seed=4):
    random.seed(seed)
    all_phase_configs = []
    for _ in range(max(phase_counts)):
        num_comp = random.randint(1, 7)
        all_phase_configs.append(random.sample(range(7), num_comp))

    results = {'naive': {'scale': [], 'time': [], 'calls': []},
               'opt': {'scale': [], 'time': [], 'calls': []}}

    for count in phase_counts:
        # 1. Naive Model
        engine_n = BDDEngine()
        start_n = time.time()
        mission_n = engine_n.TRUE
        for p in range(count):
            phase_logic = engine_n.TRUE
            for c_idx in all_phase_configs[p]:
                var_node = engine_n.get_node(p * 7 + c_idx + 10, engine_n.TRUE, engine_n.FALSE)
                phase_logic = engine_n.and_op(phase_logic, var_node)
            mission_n = engine_n.and_op(mission_n, phase_logic)
        results['naive']['scale'].append(len(engine_n.unique_table))
        results['naive']['time'].append(time.time() - start_n)
        results['naive']['calls'].append(engine_n.recursive_calls)

        # 2. Optimized Model (Backward PDO / Superscript Rule)
        engine_o = BDDEngine()
        start_o = time.time()
        mission_o = engine_o.TRUE
        for p in range(count):
            phase_logic = engine_o.TRUE
            for c_idx in all_phase_configs[p]:
                var_node = engine_o.get_node(c_idx + 10, engine_o.TRUE, engine_o.FALSE)
                phase_logic = engine_o.and_op(phase_logic, var_node)
            mission_o = engine_o.and_op(mission_o, phase_logic)
        results['opt']['scale'].append(len(engine_o.unique_table))
        results['opt']['time'].append(time.time() - start_o)
        results['opt']['calls'].append(engine_o.recursive_calls)
    return results

phase_counts = [2, 10, 20, 50, 100]
data = run_simulation(phase_counts)

fig, axs = plt.subplots(1, 3, figsize=(18, 5))
metrics = [('scale', 'Model Scale (Nodes)'), ('time', 'Construction Time (s)'), ('calls', 'Recursive Calls')]
for i, (key, label) in enumerate(metrics):
    axs[i].plot(phase_counts, data['naive'][key], 'r-o', label='Naive (No Merging)')
    axs[i].plot(phase_counts, data['opt'][key], 'b-s', label='Optimized (Backward/Merged)')
    axs[i].set_title(label)
    axs[i].set_xlabel('Number of Phases')
    axs[i].legend()
    axs[i].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
