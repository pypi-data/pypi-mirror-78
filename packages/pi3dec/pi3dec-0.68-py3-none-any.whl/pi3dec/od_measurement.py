import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt
class ODmeasurement:
    def __init__(self, pe, fit_calibration_functions=True):
        self.pe = pe
        self.dev = pe.dev
        self.calibration_file_front = os.path.join(self.pe.name, "calibration_data_od_front.csv")
        self.calibration_file_side = os.path.join(self.pe.name, "calibration_data_od_side.csv")
        self.calibration_file_front_off = os.path.join(self.pe.name, "calibration_data_od_front_off.csv")
        self.calibration_file_side_off = os.path.join(self.pe.name, "calibration_data_od_side_off.csv")
        self.od_file = os.path.join(self.pe.name, "log_OD.csv")

        self.calibration_functions = None
        if os.path.exists(self.calibration_file_front):
            df = pd.read_csv(self.calibration_file_front, index_col=0)
            if any(np.isnan(df.values.ravel())):
                print("OD calibration data incomplete.")
            else:
                if fit_calibration_functions:
                    self.fit_calibration_curves()
        else:
            print("OD calibration data not found.")

    def collect_calibration_data(self, calibration_OD_values=None, starting_index=0):
        if calibration_OD_values is None:
            od_list = input("Please input 7 od values used for calibration:")
            od_list = [float(od) for od in od_list.replace(" ", ",").split(",") if od]
            calibration_OD_values=od_list
        CurrentFront = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6], index=calibration_OD_values)
        CurrentSide = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6], index=calibration_OD_values)
        CurrentFrontOFF = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6], index=calibration_OD_values)
        CurrentSideOFF = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6], index=calibration_OD_values)
        if starting_index >0:
            CurrentFront = pd.read_csv(self.calibration_file_front, index_col=0)
            CurrentSide = pd.read_csv(self.calibration_file_side, index_col=0)
            CurrentFrontOFF = pd.read_csv(self.calibration_file_front_off, index_col=0)
            CurrentSideOFF = pd.read_csv(self.calibration_file_side_off, index_col=0)
            for df in [CurrentFront, CurrentSide, CurrentFrontOFF, CurrentSideOFF]:
                df.columns = df.columns.astype(int)
        for i in range(starting_index, 7):
            instructions = "Please arrange tubes as follows:\n"
            for t in range(7):
                instructions += "OD {OD} in tube {t}\n".format(OD=calibration_OD_values[(t - i) % 7], t=t)
            instructions += "ENTER to continue, input x to exit:"
            next_step = input(instructions)
            if next_step.lower() == "x":
                break
            else:
                self.pe.mix(self.pe.mixer_speed)
                time.sleep(5)
                self.pe.mix(0)
                time.sleep(3)
                for t in range(7):
                    IFS, ISS, IFSoff, ISSoff = self.pe.Photodiodes.measure_current(t)
                    CurrentFront.loc[calibration_OD_values[(t - i) % 7], t] = IFS
                    CurrentFrontOFF.loc[calibration_OD_values[(t - i) % 7], t] = IFSoff
                    CurrentSide.loc[calibration_OD_values[(t - i) % 7], t] = ISS
                    CurrentSideOFF.loc[calibration_OD_values[(t - i) % 7], t] = ISSoff

                    CurrentFront.to_csv(self.calibration_file_front)
                    CurrentSide.to_csv(self.calibration_file_side)
                    CurrentFrontOFF.to_csv(self.calibration_file_front_off)
                    CurrentSideOFF.to_csv(self.calibration_file_side_off)
                    try:
                        from IPython.display import clear_output
                        clear_output()
                    except:
                        pass

                    print(color.RED+color.BOLD+"Front Current:"+color.END)
                    print(color.RED+color.BOLD+str(CurrentFront)+color.END)
                    print(color.BLUE+color.BOLD+"Side Current:"+color.END)
                    print(color.BLUE+color.BOLD+str(CurrentSide)+color.END)
                    print(color.YELLOW+color.BOLD+"Front Current, laser OFF:"+color.END)
                    print(color.YELLOW+color.BOLD+str(CurrentFrontOFF)+color.END)
                    print(color.DARKCYAN+color.BOLD+"Side Current, laser OFF:"+color.END)
                    print(color.DARKCYAN+color.BOLD+str(CurrentSideOFF)+color.END)
            print("\t\tBatch completed.\n\n")
            if i==7:
                print("\t\tDone collecting calibration data!")

    def fit_calibration_curves(self):
        df = pd.read_csv(self.calibration_file_front, index_col=0)
        df.columns = df.columns.astype(int)
        OD = np.array(df.index).ravel()
        calibration_functions = []
        for tube in range(7):
            current = df.loc[:, tube]
            function = fit_one_calibration_curve(current, OD)
            calibration_functions += [function]
        self.calibration_functions = calibration_functions

    def plot_calibration_curves(self):
        plot_calibration_curves(self.pe)

    def calculate_OD_from_calibration_function(self, FrontCurrent, tube):
        f = self.calibration_functions[tube]
        calculated_od = f(FrontCurrent)
        return calculated_od

    def measure_OD(self, tube,log=True,cycles=5, n_measurements=20, laserOnDelay=10, laserOffDelay=10,
                        filter_errors=True, verbose=False):
        if callable(self.calibration_functions[tube]):
            IFS, ISS, IFSoff, ISSoff = self.pe.Photodiodes.measure_current(tube, cycles=cycles,
                                                       n_measurements=n_measurements, laserOnDelay=laserOnDelay,
                                                       laserOffDelay=laserOffDelay, filter_errors=filter_errors,
                                                       verbose=verbose)
            measured_od = self.calculate_OD_from_calibration_function(IFS, tube)
            if log:
                self.log_od(tube, measured_od)
            return measured_od
        else:
            print("Please calibrate OD sensors")

    def log_od(self, tube, od_value):
        if not os.path.exists(self.od_file):
            with open(self.od_file, "w+") as f:
                f.write("time,0,1,2,3,4,5,6\n")
        string = [""] * 7
        string[tube] = str(round(od_value, 3))
        string=",".join([time.ctime()] + string)+"\n"
        with open(self.od_file, "a") as f:
            f.write(string)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def fit_one_calibration_curve(current, OD):
    x = np.log(current)
    y = np.log(OD + 1)

    coefficients = np.polyfit(x, y, 3)
    poly = np.poly1d(coefficients)

    def current_to_OD(current):
        x = np.log(current)
        y = poly(x)
        OD = np.exp(y) - 1
        return OD

    return current_to_OD

def plot_calibration_curves(pe):
    calibration_file=pe.OD_measurement.calibration_file_front
    calibration_df=pd.read_csv(calibration_file,index_col=0)
    for t in range(7):
        calibration_OD_values=calibration_df.iloc[:,t].index
        calibration_currents=calibration_df.iloc[:,t].values
        maxcurrent=calibration_df.max().max()
        currents=np.linspace(10,maxcurrent*1.1,200)
        f = pe.OD_measurement.calibration_functions[t]
        plt.plot(currents,f(currents),"--",label="calibration curve")
        plt.plot(calibration_currents,calibration_OD_values,"ro",label="calibration data")
        plt.xlabel("Photodiode Current (uA)")
        plt.ylabel("Optical Density")
        plt.title("Tube %d" %t)
        plt.legend()
        plt.grid()
        plt.show()