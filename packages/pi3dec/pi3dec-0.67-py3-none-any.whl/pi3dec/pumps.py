import time
import os
import pandas as pd
from pi3dec import pm

PUMP_DATA_FILENAME = "log_pumps.csv"
PUMP_CALIBRATION_FILENAME = "calibration_pumps.csv"


class Pumps:
    def __init__(self, pe):
        self.pe = pe  # pi3dec.Experiment object
        self.dev = pe.dev  # device
        self.logfile = os.path.join(pe.name, PUMP_DATA_FILENAME)
        self.calibration_file = os.path.join(pe.name, PUMP_CALIBRATION_FILENAME)
        self._default_pump_coefficients = {1: 215000, 2: 215000, 3: 215000}
        self.calibrated_pump_coefficients = {1: None, 2: None, 3: None}
        self.read_calibration_data()

    def pump_peace(self, tube, volume):
        self.pe.Valves.close_all_valves()  # redundant valve close for safety
        self.log_pump_operation(tube=tube, pump1Volume=volume, comment="started pumping")
        self.pe.Valves.open_valve(tube)
        time.sleep(0.5)
        steps = int(volume * self.pump_coefficients[1])
        self.dev.request(pm.dev_msg.PumpRequest(pump1Volume=steps))
        time.sleep(0.5)  # release all pressure in the tubes before closing the valve
        self.pe.Valves.close_valve(tube)
        self.log_pump_operation(tube=tube, pump1Volume=volume, comment="completed pumping")

    def pump_death(self, tube, volume):
        self.pe.Valves.close_all_valves()  # redundant valve close for safety
        self.log_pump_operation(tube=tube, pump2Volume=volume, comment="started pumping")
        self.pe.Valves.open_valve(tube)
        time.sleep(0.5)
        steps = int(volume * self.pump_coefficients[2])
        self.dev.request(pm.dev_msg.PumpRequest(pump2Volume=steps))
        time.sleep(0.5)  # release all pressure in the tubes before closing the valve
        self.pe.Valves.close_valve(tube)
        self.log_pump_operation(tube=tube, pump2Volume=volume, comment="completed pumping")

    def pump_vacuum(self, tube, volume):
        self.pe.Valves.close_all_valves()  # redundant valve close for safety
        self.log_pump_operation(tube=tube, pump3Volume=volume, comment="started pumping")
        self.pe.Valves.open_valve(tube)
        time.sleep(0.5)
        steps = int(volume * self.pump_coefficients[3])
        self.dev.request(pm.dev_msg.PumpRequest(pump3Volume=steps))
        time.sleep(0.5)  # release all pressure in the tubes before closing the valve
        self.pe.Valves.close_valve(tube)
        self.log_pump_operation(tube=tube, pump3Volume=volume, comment="completed pumping")

    def log_pump_operation(self, tube, pump1Volume=0, pump2Volume=0, pump3Volume=0,comment=""):
        if not os.path.exists(self.logfile):
            with open(self.logfile, "w+") as f:
                f.write("time,tube,pump1Volume,pump2Volume,pump3Volume,comment\n")
        current_time = time.ctime()
        with open(self.logfile, "a") as f:
            f.write("{time}, {tube:1d}, {v1:.3f}, {v2:.3f}, {v3:.3f}, {comment}\n".format(time=current_time,
                                                                                tube=tube,
                                                                                v1=pump1Volume,
                                                                                v2=pump2Volume,
                                                                                v3=pump3Volume,
                                                                                comment=comment))

    def calibrate(self, tube=None, requested_volume=None, real_volume=None):
        """
        Calibrate the pumps by weighting the volume pumped in a vial using a scale.
        Place the vial on the scale, making sure that the silicone tubes will not affect the measurement.
        """
        pump_input_string = """Please select which pump to calibrate:
        1 - peace
        2 - death
        3 - vacuum
        input 1,2 or 3"""
        pump = int(input(pump_input_string))
        if tube is None:
            tube = int(input("Please select which tube to pump into: \n (0,1,2,3,4,5 or 6)"))
            assert tube in [0, 1, 2, 3, 4, 5, 6]

        if requested_volume is None:
            requested_volume = float(input("Please input volume to pump in ml: \n(max 20)"))
            assert 0 < requested_volume < 20

        if real_volume is None:
            print("Sending {vol}ml request to pump {p}".format(vol=requested_volume, p=pump))
            if pump == 1:
                self.pump_peace(tube=tube, volume=requested_volume)
            if pump == 2:
                self.pump_death(tube=tube, volume=requested_volume)
            if pump == 3:
                self.pump_vacuum(tube=tube, volume=requested_volume)

            real_volume = float(input("What was the real volume [ml]?"))
            self.pump_coefficients[pump] = int(self.pump_coefficients[pump] * requested_volume / real_volume)
            self.calibrated_pump_coefficients[pump] = self.pump_coefficients[pump]
            self.write_calibration_data()

    def write_calibration_data(self):
        pd.DataFrame(self.calibrated_pump_coefficients, index=[0]).to_csv(self.calibration_file, index=False)
        print("Wrote calibration data\n{coefs} to file\n{file}".format(coefs=self.calibrated_pump_coefficients,
                                                                       file=self.calibration_file))

    def read_calibration_data(self,pump_calibration_filepath=None):
        """
        read calibration of current experiment, or from another file
        """
        if pump_calibration_filepath is None:
            pump_calibration_filepath = self.calibration_file

        if not os.path.exists(pump_calibration_filepath):
            print("Pump calibration file not found.")
            print("Please calibrate pumps before running experiment!")
            self.pump_coefficients = self._default_pump_coefficients
        else:
            coefficients = pd.read_csv(pump_calibration_filepath).T[0]
            keys = coefficients.keys().astype(int)
            values = [int(i) if i > 0 else None for i in coefficients.values]
            self.calibrated_pump_coefficients = dict(zip(keys, values))

            print("Calibrated pump coefficients read from "+pump_calibration_filepath)
            print(self.calibrated_pump_coefficients)

            self.pump_coefficients = self.calibrated_pump_coefficients
            if None in self.calibrated_pump_coefficients.values():
                print("Please calibrate all pumps! Using some default values.")
                for k in self.pump_coefficients.keys():
                    if self.pump_coefficients[k] is None:
                        self.pump_coefficients[k] = self._default_pump_coefficients[k]