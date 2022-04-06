from time import perf_counter
import csv, os


class TimingTool:
    fname = "timing_tool.csv"
    tic_dbc = 0
    new_epoch = True
    new_header = True
    data_dict = {}
    prev_heading = data_dict.keys()

    @classmethod
    def __init__(cls, fname: str = ""):
        if len(fname) == 0:
            return
        else:
            cls.fname = fname

    @classmethod
    def add_timing_data(cls, func_name: str, is_start: bool, new_epoch: bool = False):
        # Create keyname to use in data dict
        pre_str = "Start" if is_start else "End"
        key_name = f"{pre_str} {func_name}"
        # Add timing data to data dict
        cls.new_epoch = new_epoch
        if cls.new_epoch:
            # Update previous heading and reset timer if at a new iteration
            cls.prev_heading = cls.data_dict.keys()
            cls.data_dict = {}
            cls.data_dict[key_name] = 0
            cls.tic_dbc = perf_counter()
            cls.new_epoch = False
        else:
            cls.data_dict[key_name] = int((perf_counter() - cls.tic_dbc) * 1000)
        print(f"{key_name}: {cls.data_dict[key_name]}")

    @classmethod
    def append_to_csv(cls):
        # Write to csv log
        if len(cls.data_dict) > 0:
            # Sort data dict in ascending numerical
            cls.data_dict = dict(
                sorted(cls.data_dict.items(), key=lambda item: item[1])
            )
            cls.new_header = cls.new_header or (
                cls.data_dict.keys() != cls.prev_heading
            )
            with open(cls.fname, "a", newline="", encoding="UTF8") as f:
                # Create header at first call to this function, if heading changes, or new file
                if cls.new_header or (os.stat(cls.fname).st_size == 0):
                    cls.new_header = False
                    w = csv.writer(f)
                    w.writerow(list(cls.data_dict.keys()))
                w = csv.writer(f)
                w.writerow(list(cls.data_dict.values()))
        print(f"Data appended to {cls.fname}\n")
