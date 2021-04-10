#!/usr/bin/env python3
import json
import curses
import subprocess as sp

from time import sleep
from datetime import datetime
from collections import deque


class Core():
    def __init__(self, number, current_temp):
        self.number = number
        self.maxlen = 300
        self.temp = current_temp
        self.average = current_temp
        self.iterations = 0
        self.max_temp = current_temp
        self.min_temp = current_temp
        self.temps = deque()
        self.temps.append(current_temp)


    def __repr__(self):
        return f"Core{self.number}:\n\tcurrent: {self.temp}\n\t    min: {self.min_temp}\n\t    max: {self.max_temp}\n\t average: {self.average}"


    def report(self):
        return {"temp": self.temp,
                "min": self.min_temp,
                "max": self.max_temp,
                "avg": self.average,
                "number": self.number}


    def _compute_average(self):
        denominator = float(len(self.temps))
        numerator = float(sum(self.temps))
        self.average = numerator / denominator

    
    def update(self, current_temp):
        self.temp = current_temp
        if current_temp >= self.max_temp:
           self.max_temp = current_temp
        if current_temp <= self.min_temp:
            self.min_temp = current_temp
        if len(self.temps) > self.maxlen:
            self.temps.popleft()
        self.temps.append(current_temp)
        self._compute_average()


class CPU():
    def __init__(self):
        self.cores = list()
        poll_dump = self.poll()
        for interface, sensors in poll_dump.items():
            for device, readings in sensors.items():
                if type(readings) is dict:
                    if "Core" in device:
                        number = int(device.split()[-1])
                        for label, temp in readings.items():
                            if "_input" in label:
                                self.cores.append(Core(number, temp))
        self.last_update = datetime.now()


    def poll(self):
        temps_str = ""
        with sp.Popen('sensors -j', stdout=sp.PIPE, shell=True) as cmd:
            if cmd.stdout is not None:
                for line in cmd.stdout:
                    temps_str += line.decode()
        return json.loads(temps_str)


    def update(self):
        if (datetime.now() - self.last_update).total_seconds() > 1:
            poll_dump = self.poll()
            for interface, sensors in poll_dump.items():
                for device, readings in sensors.items():
                    if type(readings) is dict:
                        if "Core" in device:
                            number = int(device.split()[-1])
                            for label, temp in readings.items():
                                if "_input" in label:
                                    self.cores[number].update(temp)
            self.last_update = datetime.now()
         

    def print_readings(self):
        for core in self.cores:
            print(core)


    def report(self):
        core_report = list()
        for core in self.cores:
            core_report.append(core.report())
        return core_report


class Screen():
    def __init__(self):
        self.stdscr = curses.initscr()


    def __enter__(self):
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(False)
        self.stdscr.nodelay(True)
        return self.stdscr


    def __exit__(self, type, value, tb):
        self.stdscr.keypad(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


def main():
    cpu = CPU()
    with Screen() as scr:
        while True:
            try:
                cpu.update()
                data = ""
                for core in cpu.report():
                    _head = f"Core{core['number']}:\n"
                    _temp = f"\tTemp: {core['temp']}\n"
                    _tmax = f"\t Max: {core['max']}\n"
                    _tmin = f"\t Min: {core['min']}\n"
                    _tavg = f"\t Avg: {core['avg']:.1f}\n"
                    data += _head + _temp + _tmax + _tmin + _tavg
                scr.addstr(0, 0, data)
                scr.refresh()
                keypress = scr.getkey()
                if keypress == 'q':
                    break
            except curses.error:
                continue
            except KeyboardInterrupt:
                print("user keyboard interrupt")
                break



main()
