import os

import scipy.signal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import odeint


# parameters
m_GnRH_E2_P4 = 5.707
T_GnRH_P4 = 0.271
T_GnRH_E2 = 1.127
c_GnRH = 1.223
m_FSH_Inh = 1.044
T_FSH_Inh = 0.217
c_FSH = 0.559
m_LH_GnRH_P4 = 46.647
T_LH_P4 = 0.0542
T_LH_GnRH = 0.896
c_LH = 9.006
m_Foll_FSH=0.269
T_Foll_FSH = 0.787
m_Foll_Foll = 3.927
T_Foll_Foll = 0.289
m_Foll_P4 = 0.79
T_Foll_P4 = 0.125
m_Foll_LH = 1.7
T_Foll_LH = 0.881
SF_CL = 1.2
m_CL_CL = 0.0372
T_CL_CL = 0.314
m_CL_IOF = 7.534
T_CL_IOF = 1.035
k_P4_CL = 0.564
c_P4 = 0.533
k_E2_Foll = 1.009
c_E2 = 0.72
k_Inh_Foll = 0.644
c_Inh = 0.368
m_PGF_E2 = 1.291
T_PGF_E2 = 0.221
T_PGF_P4 = 0.969
c_PGF = 0.356
m_IOF_PGF_CL = 12.269
T_IOF_PGF = 1.282
T_IOF_CL = 0.639
c_IOF = 0.215


def h_pos(y, T, e):
    return (y**e) / ((y**e)+(T**e))


def h_neg(y, T, e):
    return (T**e) / ((y**e)+(T**e))


# returns dy/dt
def model(y, t):
    # GnRH FSH LH Foll CL
    # P4 E2 Inh PGF IOF
    # here are the ode equations
    # return list of the changes
    GnRH = y[0]
    FSH = y[1]
    LH = y[2]
    Foll = y[3]
    CL = y[4]
    P4 = y[5]
    E2 = y[6]
    Inh = y[7]
    PGF = y[8]
    IOF = y[9]
    dGnRHdt = m_GnRH_E2_P4 * h_neg(P4, T_GnRH_P4, 2) * h_pos(E2, T_GnRH_E2, 5) - c_GnRH * GnRH
    dFSHdt = m_FSH_Inh * h_neg(Inh, T_FSH_Inh, 5) - c_FSH * FSH
    dLHdt = m_LH_GnRH_P4 * h_neg(P4, T_LH_P4, 2) * h_pos(GnRH, T_LH_GnRH, 2) - c_LH * LH
    dFolldt = (m_Foll_FSH * h_pos(FSH, T_Foll_FSH, 2) * (1+m_Foll_Foll * h_pos(Foll, T_Foll_Foll, 2))
               - (m_Foll_P4 * h_pos(P4, T_Foll_P4, 5) + m_Foll_LH * h_pos(LH, T_Foll_LH, 2)) * Foll)
    dCLdt = (SF_CL * m_Foll_LH * h_pos(LH, T_Foll_LH, 2) * Foll + m_CL_CL * h_pos(CL, T_CL_CL, 2)
             - m_CL_IOF * h_pos(IOF, T_CL_IOF, 5) * CL)
    dP4dt = k_P4_CL * CL - c_P4 * P4
    dE2dt = k_E2_Foll * Foll - c_E2 * E2
    dInhdt = k_Inh_Foll * Foll - c_Inh * Inh
    dPGFdt = m_PGF_E2 * h_pos(E2, T_PGF_E2, 2) * h_pos(P4, T_PGF_P4, 5) - c_PGF * PGF
    dIOFdt = m_IOF_PGF_CL * h_pos(PGF, T_IOF_PGF, 5) * h_pos(CL, T_IOF_CL, 5) - c_IOF * IOF
    return [dGnRHdt, dFSHdt, dLHdt, dFolldt, dCLdt, dP4dt, dE2dt, dInhdt, dPGFdt, dIOFdt]

hormones = ["GnRH", "FSH", "LH", "Foll", "CL", "P4", "E2", "Inh", "PGF", "IOF"]
y0 = [0.0027, 0.5706, 0.0, 0.6131, 0.0098, 0.0504, 0.3650, 0.2603, 0.1418, 0.2630]
length = 60
t = np.linspace(0,length,length*10)

y, infodict = odeint(model,y0,t, full_output=True)
print(infodict['message'])

colours = ["lightseagreen", "yellow", "orange",
           "gray", "green", "blue", "red",
           "darkblue", "purple", "black"]
LH_CL_P4 = [2, 4, 5]  # LH, CL, P4
Foll_E2_Inh = [3, 6, 7]  # Foll, E2, INh
folls = [3, 1, 5]  # Foll, FSH, P4
rest = [0, 8, 9]  # GnRH, PGF, IOF
plots = [LH_CL_P4, Foll_E2_Inh, folls, rest]

lh_peaks, _ = scipy.signal.find_peaks(y[:, hormones.index("LH")], distance=10, height=0.5)
if len(lh_peaks) >= 3:
    starttime = lh_peaks[0]
    endtime = lh_peaks[2]
    ct = t - t[lh_peaks[1]]
else:
    starttime = 0
    endtime = len(t)
    ct = t

for plot in plots:
    for i in plot:
        plt.plot(ct[starttime:endtime], y[:, i][starttime:endtime], label=hormones[i], color=colours[i])
    plt.grid()
    plt.legend(loc='upper right')
    plt.xlabel('time')
    plt.ylabel('c')
    plt.show()

columns_to_plot = [2, 1, 5, 6]
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()
for i, ax in zip(columns_to_plot, axes):
    ax.plot(t, y[:, i], label=hormones[i])
    ax.set_title(hormones[i])
    ax.set_xlabel('days')
    ax.set_ylabel('Concentration (c)')
    ax.grid(True)
    #ax.legend(loc='best')
plt.tight_layout()
plt.show()

# Save the data to csv
time = [i for i in range(len(t))]
df = pd.DataFrame({
    'Time': t,
})
for hormone in hormones:
    df[hormone] = y[:,hormones.index(hormone)]

df.set_index('Time', inplace=True, drop=True)
print(df)

simulation_output_file = os.path.join(".", "bov_cycle_ODE_sim_columns.csv")
df.to_csv(simulation_output_file, sep='\t')

simulation_output_file_rows = os.path.join(".", "bov_cycle_ODE_sim_rows.csv")
df_t = df.T
df_t.to_csv(simulation_output_file_rows, sep=',')