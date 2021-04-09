#!/usr/bin/env python3
import json

import subprocess as sp

from time import sleep
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
        temps_str = ""
        with sp.Popen('sensors -j', stdout=sp.PIPE, shell=True) as cmd:
            if cmd.stdout is not None:
                for line in cmd.stdout:
                    temps_str += line.decode()
        poll_dump = json.loads(temps_str)
        for interface, sensors in poll_dump.items():
            for device, readings in sensors.items():
                if type(readings) is dict:
                    if "Core" in device:
                        number = int(device.split()[-1])
                        for label, temp in readings.items():
                            if "_input" in label:
                                self.cores.append(Core(number, temp))


    def poll(self):
        temps_str = ""
        with sp.Popen('sensors -j', stdout=sp.PIPE, shell=True) as cmd:
            if cmd.stdout is not None:
                for line in cmd.stdout:
                    temps_str += line.decode()
        poll_dump = json.loads(temps_str)
        for interface, sensors in poll_dump.items():
            for device, readings in sensors.items():
                if type(readings) is dict:
                    if "Core" in device:
                        number = int(device.split()[-1])
                        for label, temp in readings.items():
                            if "_input" in label:
                                self.cores[number].update(temp)
         

    def print_readings(self):
        for core in self.cores:
            print(core)



def main():
    cpu = CPU()
    while True:
        try:
            cpu.poll()
            cpu.print_readings()
            sleep(1)
        except KeyboardInterrupt:
            print("user keyboard interrupt")
            exit(0)
        except Execption as e:
            print(e)
            exit(1)


main()
