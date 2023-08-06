import os
import time
import pandas as pd
import schedule
import numpy as np


def read_last_OD_values(pe):
    def strtoint(s):
        try:
            return float(s)
        except:
            return None
    df = pd.read_csv(pe.OD_measurement.od_file, index_col=0)
    lastvalues = [0, 0, 0, 0, 0, 0, 0]
    for t in range(7):
        try:
            ODvalues=list(strtoint(s) for s in df.iloc[:, t])
            ODvalues=[od for od in ODvalues if od]
            lastvalues[t]=ODvalues[-1]
        except:
            pass
    return np.array(lastvalues)


def make_dilution(pe, tube, death_volume=0, peace_volume=0, extra_vacuum=5):
    pe.mix(30)   # Mixer speed > 30 while pumping may lead to power failure!
    if death_volume>0:
        pe.Pumps.pump_death(tube, death_volume)
    if peace_volume>0:
        pe.Pumps.pump_peace(tube, peace_volume)
    pe.Pumps.pump_vacuum(tube, death_volume+peace_volume)
    pe.mix(0)
    pe.Pumps.pump_vacuum(tube, extra_vacuum)
    pe.mix(30)


def _write_parameters_drug_doses(pe, drug_doses):
    assert len(drug_doses) == 7
    with open(os.path.join(pe.name, "parameters_drug_dose.csv"), "w+") as f:
        f.write(",".join([str(int(d)) for d in drug_doses]))


def _read_parameters_drug_doses(pe):
    try:
        df = pd.read_csv(os.path.join(pe.name, "parameters_drug_dose.csv"), header=None)
        drug_doses = np.array(df.values.ravel()).astype(int)
        drug_doses = drug_doses
    except FileNotFoundError:
        drug_doses = [0, 0, 0, 0, 0, 0, 0]
        _write_parameters_drug_doses(pe, drug_doses)
    return drug_doses


def _write_parameters_OD_thresholds(pe, OD_thresholds):
    OD_thresholds = np.array(OD_thresholds).astype(float)
    assert len(OD_thresholds) == 7
    with open(os.path.join(pe.name, "parameters_OD_thresholds.csv"), "w+") as f:
        f.write(",".join([str(round(thr, 2)) for thr in OD_thresholds]))


def _read_parameters_OD_thresholds(pe):
    try:
        OD_thresholds = pd.read_csv(os.path.join(pe.name, "parameters_OD_thresholds.csv"), header=None).values[0]
        OD_thresholds = np.array(OD_thresholds.ravel()).astype(float)
        OD_thresholds = OD_thresholds
    except FileNotFoundError:
        OD_thresholds = [np.inf] * 7
        _write_parameters_OD_thresholds(pe, OD_thresholds)
    return OD_thresholds


def dilute_if_necessary(pe, total_dilution_volume=10,delta_t_min=900):
    OD_thresholds = pe.parameters_OD_thresholds
    drug_doses = pe.parameters_drug_doses

    death_volumes = total_dilution_volume * drug_doses/100
    peace_volumes = total_dilution_volume - death_volumes
    for tube in range(7):
        if OD_thresholds[tube] > 0.15 and tube in pe.active_tubes:
            if pe.last_OD_values[tube] > OD_thresholds[tube]:
                if time_since_last_pump(pe,tube)>delta_t_min:
                    make_dilution(pe, tube,
                              death_volume=death_volumes[tube],
                              peace_volume=peace_volumes[tube],
                              extra_vacuum=5)

def time_since_last_pump(pe,t):
    df = pd.read_csv(os.path.join(pe.name, "log_pumps.csv"))
    timenow=pd.Timestamp(time.ctime())
    timedeltas=timenow-df.groupby("tube")["time"].max().apply(pd.Timestamp)
    timedeltas=timedeltas.apply(lambda x: x.total_seconds())
    return timedeltas[t]

def pause_mixers_and_measure_OD(pe):
    pe.mix(pe.mixer_speed)
    time.sleep(2)
    pe.mix(0)
    time.sleep(3)
    for t in range(7):
        pe.last_OD_values[t] = pe.OD_measurement.measure_OD(t)
    pe.mix(pe.mixer_speed)


def start_experiment(pe):
    print("Starting Experiment loop")
    if len(pe.active_tubes) == 0:
        print("####### NO ACTIVE TUBES! #######")
    pe.print_status()

    pe.mix(pe.mixer_speed)
    schedule.clear()
    schedule.every().minute.at(":00").do(pause_mixers_and_measure_OD, pe)
    schedule.every().minute.at(":15").do(dilute_if_necessary, pe)

    stop_file = os.path.join(pe.name, "stop.experiment")
    while not os.path.exists(stop_file):
        schedule.run_pending()
        time.sleep(1)
    os.remove(stop_file)
    print("Experiment stopped")
