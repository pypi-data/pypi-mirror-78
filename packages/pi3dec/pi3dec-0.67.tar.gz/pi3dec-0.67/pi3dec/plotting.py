import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

def exp_fit(timewindow, ODwindow):
    """
    fits an exponential growth curve to the OD vs time data.
    N=N0*exp(r*t)

    time: array of time values in hours
    OD: array of OD values
    returns: N0, r
    """

    ODwindow[ODwindow < 0] = 0
    ODwindow = np.log(ODwindow)
    r, b = np.polyfit(timewindow, ODwindow, 1)
    N0 = np.exp(b)
    return N0, r


def shrink_time_window(timewindow, ODwindow):
    timewindow = timewindow[ODwindow > 0]
    ODwindow = ODwindow[ODwindow > 0]
    log_diff = np.diff(np.log(ODwindow))
    if any(abs(log_diff) > 0.2):
        indeces = np.where(abs(log_diff) > 0.2)[0]
        if len(indeces) == 1:  # only 1 big jump in OD
            index = indeces.ravel()[0]
        else:
            #             print("big jumps",timewindow[0])
            #             index = np.where(log_diff==log_diff.max())[0][0]
            return [], []
        if index > len(ODwindow) / 2:
            timewindow = timewindow[:index + 1]
            ODwindow = ODwindow[:index + 1]
        else:
            timewindow = timewindow[index + 1:]
            ODwindow = ODwindow[index + 1:]
    return timewindow, ODwindow

def interpolate_nans(growth_rates):
    nans = np.isnan(growth_rates)
    x = lambda z: z.nonzero()[0]
    growth_rates_2 = growth_rates.copy()
    growth_rates_2[nans] = np.interp(x(nans), x(~nans), growth_rates[~nans])
    return growth_rates_2

def calculate_growth_rates(time, od, window_size=40):
    assert len(time) == len(od)
    time_in_hours = [t.total_seconds() / 3600 for t in time - time[0]]
    growth_rates = np.array([np.nan] * len(time))
    N0s = np.array([np.nan] * len(time))
    for i in range(window_size // 2, len(time) - window_size // 2):
        timewindow = time_in_hours[i - window_size // 2:i + window_size // 2]
        ODwindow = od[i - window_size // 2:i + window_size // 2]
        timewindow = np.array(timewindow)
        ODwindow = np.array(ODwindow)
        timewindow, ODwindow = shrink_time_window(timewindow, ODwindow)

        if len(timewindow) > 5:
            N0, r = exp_fit(timewindow, ODwindow)
            if r < 0:
                r = np.nan
            growth_rates[i] = r
            N0s[i] = N0
    growth_rates = np.convolve(interpolate_nans(growth_rates), [1 / 120] * 120, mode='same')

    return growth_rates, N0s



def plot_tube(pe, tube, log_OD=None, log_pumps=None, plot_growth_rate=True, window_size=30, close=True, dpi=150):
    if log_OD is None:
        log_OD = pd.read_csv(pe.OD_measurement.od_file, parse_dates=["time"], index_col="time")
    if log_pumps is None:
        log_pumps = pd.read_csv(os.path.join(pe.name, "log_pumps.csv"), parse_dates=["time"], index_col="time")

    df = log_OD.iloc[:, tube].dropna()
    time, od = df.index, df.values.astype(float)
    time0 = time[0]
    time_last = time[-1]

    time_in_hours = [t.total_seconds() / 3600 for t in time - time0]

    fig, ax = plt.subplots(figsize=[12, 4], dpi=dpi)

    ax2 = ax.twinx()
    colors = ["xkcd:dull yellow", "xkcd:electric green", "xkcd:puke brown"]
    labels = ["medium", "medium + drug", "vacuum"]
    alpha = [0.5, 0.3, 0.1]
    for j in range(3):
        pdata = log_pumps[(log_pumps.iloc[:, j + 1] > 0) & (log_pumps.tube == tube)].iloc[:, [j + 1, 4]]
        completed_indeces = np.where(pdata.comment.str.contains("completed"))[0]

        for i in completed_indeces:
            if "started" in pdata.iloc[i - 1].comment:
                start_time = (pdata.index[i - 1] - time0).total_seconds() / 3600
                end_time = (pdata.index[i] - time0).total_seconds() / 3600
                vol = pdata.iloc[i, 0]
                assert vol == pdata.iloc[i - 1, 0]
                plt.plot([start_time, end_time], [vol, vol], "s-", color=colors[j], markersize=4, linewidth=4,
                         alpha=alpha[j], label=labels[j])

    ax2.set_ylim(0, 11)
    ax2.set_ylabel("Pumped Volume [mL]")
    ax2.spines["right"].set_position(("axes", 1))
    handles2, labels2 = ax2.get_legend_handles_labels()
    by_label2 = dict(zip(labels2, handles2))

    ax.plot(time_in_hours, od, "k.", label="OD", markersize=3)
    ax.set_ylabel("Optical Density")
    ax.set_yscale("log")
    ax.set_ylim(0.0086, 1.01)
    ax.set_yticks([0.01, 0.1, 0.5, 1])
    ax.set_yticklabels([0.01, 0.1, 0.5, 1])

    handles, labels = ax.get_legend_handles_labels()

    if plot_growth_rate:
        growth_rates, N0s = calculate_growth_rates(time, od, window_size=window_size)
        ax3 = ax.twinx()
        ax3.spines["left"].set_position(("axes", -0.1))
        ax3.yaxis.set_label_position("left")
        ax3.yaxis.set_ticks_position("left")

        ax3.plot(time_in_hours, growth_rates, "r.", alpha=0.03, label="growth rate", markersize=3)
        if len(growth_rates)>120:
            growth_rates_mean = np.convolve(growth_rates, [1 / 120] * 120, mode='same')
            ax3.plot(time_in_hours, growth_rates_mean, 'r--')
        ax3.set_ylabel("Growth rate [1/h]")
        ax3.set_ylim(-0.05, 1.6)
        handles3, labels3 = ax3.get_legend_handles_labels()
        handles = handles + handles3
        labels = labels + labels3

    by_label = dict(zip(labels, handles))
    legend = plt.legend(by_label.values(), by_label.keys(), loc=3)
    legend2 = plt.legend(by_label2.values(), by_label2.keys(), loc=6, title="Pumps")  # loc - localisation
    plt.gca().add_artist(legend)
    ax.grid()
    #         ax4.grid()
    plt.suptitle("Tube  %d" % tube)
    plt.title("%s  -  %s" % (str(time0), str(time_last)), fontsize=6)
    ax.set_xlabel("Time [hours]")
    plt.savefig(os.path.join(pe.name, "plot.%d.png" % tube))
    #         plt.xlim(11.6,14)
    plt.show()
    if close:
        plt.close()