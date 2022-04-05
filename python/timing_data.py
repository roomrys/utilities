from time import perf_counter
import csv, os

global data_dbc
global tic_dbc
data_dbc = {}


def add_timing_data(func_name: str, is_start: bool, new_epoch: bool = False):
    pre_str = "Start" if is_start else "End"
    key_name = f"{pre_str} {func_name}"
    if new_epoch:
        global tic_dbc
        data_dbc[key_name] = 0
        tic_dbc = perf_counter()
    else:
        data_dbc[key_name] = int((perf_counter() - tic_dbc) * 1000)
    print(f"{key_name}: {data_dbc[key_name]}")


def append_to_csv():
    # Write to csv log
    fname = "node_dbc_timing.csv"
    if len(data_dbc) > 0:
        d_keys = list(data_dbc.keys())
        d_values = list(data_dbc.values())
        d_values.sort()
        d_keys.sort(key=dict(zip(d_keys, d_values)).get)
        with open(fname, "a", newline="", encoding="UTF8") as f:
            if os.stat(fname).st_size == 0:
                w = csv.writer(f)
                w.writerow(d_keys)
            w = csv.writer(f)
            w.writerow(d_values)
    print(f"Data appended to {fname}\n")
