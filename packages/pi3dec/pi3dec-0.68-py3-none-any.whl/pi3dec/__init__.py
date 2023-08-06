from pi3dec.valves import Valves
from pi3dec.photodiodes import Photodiodes
from pi3dec.od_measurement import ODmeasurement
from pi3dec.pumps import Pumps
from pi3dec import pm
from pi3dec.experiment import start_experiment, _write_parameters_OD_thresholds, _write_parameters_drug_doses, \
    _read_parameters_OD_thresholds, _read_parameters_drug_doses, read_last_OD_values
from pi3dec.plotting import plot_tube
import pandas as pd
import numpy as np
import os
import time
import threading

print("imported pi3dec - package to control the 3d printed raspberry pi powered evolution contraption")

class Experiment:
    def __init__(self, name="NewExperiment", connect=True, device_serial="auto", fit_calibration_functions=True,
                 total_dilution_volume=10, mixer_speed=30, active_tubes=()):
        """
        :param name: Experiment name with no spaces, e.g. starting date
        :param device_serial: board serial number or "auto" to auto-connect
        """
        assert " " not in name
        self.name = name
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        if connect:
            self.dev = self.connect_device(device_serial=device_serial)
            self.Valves = Valves(self)
            self.Photodiodes = Photodiodes(self)
            self.Pumps = Pumps(self)
        else:
            self.dev = None
            self.hub = None
            print("Not connected to device")
        self.OD_measurement = ODmeasurement(self, fit_calibration_functions=fit_calibration_functions)
        self.active_tubes = active_tubes
        self.mixer_speed = mixer_speed
        self.total_dilution_volume = total_dilution_volume
        self.experiment_thread = None

        # try:
        #     self.parameters_OD_thresholds = _read_parameters_OD_thresholds(self)
        # except FileNotFoundError:
        #     self.parameters_OD_thresholds = [0, 0, 0, 0, 0, 0, 0]
        #
        # try:
        #     self.parameters_drug_doses = _read_parameters_drug_doses(self)
        # except FileNotFoundError:
        #     self.parameters_drug_doses = [0, 0, 0, 0, 0, 0, 0]

    def mix(self, speed=30, period=3000):
        if 0 < speed < 30:
            speed = 30
        if speed > 100:
            speed = 100

        if speed > 0:
            state = 1
        else:
            state = 0

        pulseWidth = int(period * speed / 100)
        period = int(period)
        self.dev.request(pm.dev_msg.SetMixerStateRequest(state=state, period=period, pulseWidth=pulseWidth))

        # log
        try:
            with open(os.path.join(self.name, "log_mixer.csv"), "a") as f:
                f.write(time.ctime() + ",%d\n" % speed)
        except FileNotFoundError:
            with open(os.path.join(self.name, "log_mixer.csv"), "w+") as f:
                f.write("time, speed \n")
                f.write(time.ctime() + ",%d\n" % speed)

    def connect_device(self, device_serial="auto"):
        # hub = pm.PMHub.local()
        self.hub = pm.PMHub("tcp://localhost:5555")
        if device_serial == "auto":
            dev = self.hub.get_devices()[0]
        else:
            dev = [d for d in self.hub.get_devices() if d.device_serial == device_serial][0]
        print("Connected to device with serial ", dev.device_serial)
        return dev

    def test_device(self):
        print("Testing OD measurement...")
        for t in range(7):
            self.Photodiodes.measure_current(t, 1, 10)
        print("Testing mixers...")
        for speed in [30, 50, 100]:
            self.mix(speed)
            time.sleep(1)
        self.mix(0)
        print("Testing valves...")
        for t in range(7):
            self.Valves.open_valve(t)
            self.Valves.close_valve(t)
        print("Testing pumps...")
        self.Pumps.pump_peace(6, 0.1)
        self.Pumps.pump_death(6, 0.1)
        self.Pumps.pump_vacuum(6, 0.1)

    def start_experiment(self):
        if self.is_running():
            print("Experiment thread is already running! Use pe.stop_experiment() to stop.")
        else:
            self.experiment_thread = threading.Thread(target=start_experiment, args=(self,))
            self.experiment_thread.daemon = True
            self.experiment_thread.start()

    def is_running(self):
        try:
            return self.experiment_thread.is_alive()
        except AttributeError:
            return False

    def print_status(self):
        if not self.is_running():
            print("### Experiment NOT running! ###\n")
        else:
            print("Running...")
        print_status(self)

    def plot(self, tubes=None, window_size=30, close=True, dpi=150):
        if tubes is None:
            tubes = self.active_tubes
        if len(tubes) == 0:
            tubes = range(7)
        log_OD = pd.read_csv(self.OD_measurement.od_file, parse_dates=["time"], index_col="time")
        log_pumps = pd.read_csv(os.path.join(self.name, "log_pumps.csv"), parse_dates=["time"], index_col="time")
        for tube in tubes:
            plot_tube(self, tube, log_OD=log_OD, log_pumps=log_pumps, window_size=window_size, close=close, dpi=dpi)

    def stop_experiment(self):
        with open(os.path.join(self.name, "stop.experiment"), "w+"):
            pass

    @property
    def parameters_OD_thresholds(self):
        return _read_parameters_OD_thresholds(self)
    @parameters_OD_thresholds.setter
    def parameters_OD_thresholds(self,thresholds):
        _write_parameters_OD_thresholds(self, thresholds)


    @property
    def parameters_drug_doses(self):
        return _read_parameters_drug_doses(self)
    @parameters_drug_doses.setter
    def parameters_drug_doses(self, drug_doses):
        _write_parameters_drug_doses(self, drug_doses)


def print_status(pe):
    print("Tube:\t\t" + "\t".join(str(t) for t in range(7)))
    print("Status:\t\t" + "\t".join(["ACTIVE" if t in pe.active_tubes else "-" for t in range(7)]))
    print("OD threshold:\t" + "\t".join([str(thr) for thr in pe.parameters_OD_thresholds]))
    print("Drug dose (%):\t" + "\t".join([str(thr) for thr in pe.parameters_drug_doses]))

    try:
        pe.last_OD_values = read_last_OD_values(pe)
    except FileNotFoundError:
        pe.last_OD_values = [0]*7

