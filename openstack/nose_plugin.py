"""
Openstack run_tests.py style output for nosetests
"""

import heapq
import logging
import time

import colorama
import termcolor
from nose import plugins


log = logging.getLogger("openstack.nose")


class Colorizer(object):
    def __init__(self, stream):
        self.stream = stream
        colorama.init()

    def write(self, text, color):
        self.stream.write(termcolor.colored(text, color))

    def writeln(self, text, color):
        self.stream.writeln(termcolor.colored(text, color))


class NullColorizer(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, text, color):
        self.stream.write(text)

    def writeln(self, text, color):
        self.stream.writeln(text)


class Openstack(plugins.Plugin):
    """Nova style output generator"""

    name = "openstack"
    times = {}

    def _get_color(self, elapsed):
        if elapsed > self.red:
            return 'red'
        elif elapsed > self.yellow:
            return 'yellow'
        else:
            return 'green'

    def _get_name(self, test):
        address = test.address()
        parts = address[2].split('.')
        if len(parts) == 2:
            return tuple(parts)
        else:
            return None, parts[0]

    def _writeResult(self, test, long_result, color, short_result):
        name = self._get_name(test)
        elapsed = self.times[name][1] - self.times[name][0]
        item = (elapsed, name)
        if len(self._slow_tests) >= self.num_slow:
            heapq.heappushpop(self._slow_tests, item)
        else:
            heapq.heappush(self._slow_tests, item)

        if self.show_all:
            self.colorizer.write(long_result, color)
            if self.show_elapsed:
                color = self._get_color(elapsed)
                self.colorizer.write("  %.2f" % elapsed, color)
            self.stream.writeln()
        else:
            self.stream.write(short_result)
            self.stream.flush()

    def addError(self, test, err):
        name = self._get_name(test)
        self.times[name].append(time.time())
        self._writeResult(test, 'ERROR', 'red', 'E')

    def addFailure(self, test, err):
        name = self._get_name(test)
        self.times[name].append(time.time())
        self._writeResult(test, 'FAIL', 'red', 'F')

    def addSuccess(self, test):
        name = self._get_name(test)
        self.times[name].append(time.time())
        self._writeResult(test, 'OK', 'green', '.')

    def configure(self, options, conf):
        plugins.Plugin.configure(self, options, conf)
        self.conf = conf
        self.red = float(options.openstack_red)
        self.yellow = float(options.openstack_yellow)
        self.show_elapsed = options.openstack_show_elapsed
        self.num_slow = int(options.openstack_num_slow)
        self.color = options.openstack_color
        self.colorizer = None
        self._cls = None
        self._slow_tests = []
        self.show_all = True

    def options(self, parser, env):
        plugins.Plugin.options(self, parser, env)
        parser.add_option("--openstack-red",
                          default=env.get("NOSE_OPENSTACK_RED", 1.0),
                          dest="openstack_red",
                          help="Colorize run times greater than value red. "
                               "[NOSE_OPENSTACK_RED] or 1.0")
        parser.add_option("--openstack-yellow",
                          default=env.get("NOSE_OPENSTACK_YELLOW", 0.25),
                          dest="openstack_yellow",
                          help="Colorize run times greater than value "
                               "yellow. [NOSE_OPENSTACK_RED] or 0.25")
        parser.add_option("--openstack-show-elapsed", action="store_true",
                          default=env.get("NOSE_OPENSTACK_SHOW_ELAPSED"),
                          dest="openstack_show_elapsed",
                          help="Show the elaped runtime of tests. "
                               "[NOSE_OPENSTACK_SHOW_ELAPSED]")
        parser.add_option("--openstack-color", action="store_true",
                          default=env.get("NOSE_OPENSTACK_COLOR"),
                          dest="openstack_color",
                          help="Colorize output. [NOSE_OPENSTACK_COLOR]")
        parser.add_option("--openstack-num-slow",
                          dest="openstack_num_slow",
                          default=env.get("NOSE_OPENSTACK_NUM_SLOW", 5),
                          help="Number top slowest tests to report. "
                               "[NOSE_OPENSTACK_NUM_SLOW]")

    def report(self, stream):
        slow_tests = [item for item in self._slow_tests
                      if self._get_color(item[0]) != 'green']
        if slow_tests:
            slow_total_time = sum(item[0] for item in slow_tests)
            stream.writeln("Slowest %i tests took %.2f secs:"
                                % (len(slow_tests), slow_total_time))
            for time, test in sorted(slow_tests, reverse=True):
                name = '.'.join(test)
                self.colorizer.writeln("    %.2f    %s" % (time, name),
                                       self._get_color(time))

    def setOutputStream(self, stream):
        self.stream = stream
        if self.color:
            self.colorizer = Colorizer(self.stream)
        else:
            self.colorizer = NullColorizer(self.stream)
        self.stream.writeln()

    def startTest(self, test):
        cls, name = self._get_name(test)
        if cls != self._cls:
            self.stream.writeln(str(cls))
            self._cls = cls
        self.stream.write((' ' * 4 + str(name)).ljust(65))
        self.stream.flush()
        self.times[(cls, name)] = [time.time()]
