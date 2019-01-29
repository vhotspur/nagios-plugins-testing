#!/usr/bin/env python3

import re
from d3s.nagios import NagiosPluginBase


class CheckHealth(NagiosPluginBase):
    """
    Collects basic information about running Linux system.

    There are not critical/warning limits as its main purpose is to collect
    basic system information for later processing via perf data section.
    """

    MEM_INFO_RE = re.compile('^([^:]*):[ \t]*([0-9]*) kB$')
    LOAD_AVG_RE = re.compile('''
        ^([0-9.]+) # 1 min
        \\s+
        ([0-9.]+) # 5 min
        \\s+
        ([0-9.]+) # 15 min
        \\s+
        ([0-9]+)/([0-9]+) # runnable/total tasks in the system
        \\s+.*$ # ignore rest of line
        ''', re.VERBOSE)
    UPTIME_RE = re.compile('^.*up[ \t]+([^,]*),.*$')

    def __init__(self):
        NagiosPluginBase.__init__(self, 'HEALTH')

    def collect(self):
        # Read memory information
        for entry in self.grep_lines(CheckHealth.MEM_INFO_RE, self.read_file('/proc/meminfo')):
            key = entry.group(1)
            value = entry.group(2)
            if key == 'MemTotal':
                self.add_perf_data('mem_total_kb', value)
            elif key == 'MemAvailable':
                self.add_perf_data('mem_avail_kb', value)

        # Get load average
        entry = next(self.grep_lines(CheckHealth.LOAD_AVG_RE, self.read_file('/proc/loadavg')))
        self.add_perf_data('load_1min', entry.group(1))
        self.add_perf_data('load_5min', entry.group(2))
        self.add_perf_data('load_15min', entry.group(3))
        self.add_perf_data('tasks_runnable', entry.group(4))
        self.add_perf_data('tasks_total', entry.group(5))

        # Read uptime information
        entry = next(self.grep_lines(CheckHealth.UPTIME_RE, self.read_command_output(['uptime'])))
        self.add_perf_data('uptime', entry.group(1))

        # Format final message
        self.set_message_from_perf("up {uptime}, {load_5min} load, {tasks_runnable} ready tasks")

if __name__ == '__main__':
    import sys
    print(sys.argv)
    CheckHealth().run()
