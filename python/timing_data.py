from time import perf_counter
import csv, os


class TimingTool:
    def __init__(self, fname: str = "timing_tool.csv"):
        self.fname = fname
        self.tic_dbc = 0
        self.new_epoch = True
        self.new_header = True
        self.data_dict = {}
        self.prev_heading = self.data_dict.keys()

    @property
    def tic_dbc(self):
        return self._tic_dbc

    @tic_dbc.setter
    def tic_dbc(self, value):
        # Timer only set at a new epoch, reset new epoch flag
        self._tic_dbc = value
        self.new_epoch = False

    def add_timing_data(self, func_name: str, is_start: bool, new_epoch: bool = False):
        # Create keyname to use in data dict
        pre_str = "Start" if is_start else "End"
        key_name = f"{pre_str} {func_name}"
        # Add timing data to data dict
        self.new_epoch = new_epoch
        if self.new_epoch:
            # Update previous heading and reset timer if at a new iteration
            self.prev_heading = self.data_dict.keys()
            self.data_dict = {}
            self.data_dict[key_name] = 0
            self.tic_dbc = perf_counter()
        else:
            self.data_dict[key_name] = int((perf_counter() - self.tic_dbc) * 1000)
        print(f"{key_name}: {self.data_dict[key_name]}")

    def append_to_csv(self):
        # Write to csv log
        if len(self.data_dict) > 0:
            # Sort data dict in ascending numerical
            self.data_dict = dict(
                sorted(self.data_dict.items(), key=lambda item: item[1])
            )
            self.new_header = self.new_header or (
                self.data_dict.keys() != self.prev_heading
            )
            with open(self.fname, "a", newline="", encoding="UTF8") as f:
                # Create header at first call to this function, if heading changes, or new file
                if self.new_header or (os.stat(self.fname).st_size == 0):
                    self.new_header = False
                    w = csv.writer(f)
                    w.writerow(list(self.data_dict.keys()))
                w = csv.writer(f)
                w.writerow(list(self.data_dict.values()))
        print(f"Data appended to {self.fname}\n")
