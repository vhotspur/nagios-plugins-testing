

class NagiosPluginBase:
    STATUS_NAMES = [ 'OK', 'WARNING', 'CRITICAL', 'UNKNOWN' ]

    def __init__(self, name):
        self.name_ = name
        self.status_ = 0
        self.message_ = "empty message"
        self.perf_data_ = {}

    def collect(self):
        raise NotImplementedError("Re-implement in subclass!")

    def add_perf_data(self, name, value):
        self.perf_data_[name] = value

    def set_message(self, msg):
        self.message_ = msg

    def run(self):
        self.collect()
        status_name = NagiosPluginBase.STATUS_NAMES[self.status_]
        print("{} {} - {}{}".format(self.name_, status_name, self.message_, self.format_perf_data_()))

    def format_perf_data_(self):
        res = []
        for key, value in self.perf_data_.items():
            res.append("{}={}".format(key, value))
        if len(res) == 0:
            return ""
        else:
            return "|{}".format(",".join(res))
