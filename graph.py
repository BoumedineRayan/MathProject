import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# 1. Chargement et préparation des données
files = [f for f in os.listdir('.') if f.endswith('.csv') and 'benchmarks' in f]
data_list = []

for file in files:
    match = re.search(r'(\d+)x\d+', file)
    size = int(match.group(1)) if match else 0
    df = pd.read_csv(file)
    
    data_list.append({
        'size': size,
        'nw_max_iter': df['Northwest_Time'].max(),
        'bh_max_iter': df['Balas_Hammer_Time'].max(),
        'ss_nw_max_iter': df['SS_NorthWest_Time'].max(),
        'ss_bh_max_iter': df['SS_BallasHammer_Time'].max(),
        'nw_total_time': df['Total_NorthWest_Time'].max(),
        'bh_total_time': df['Total_BallasHammer_Time'].max()
    })

df_res = pd.DataFrame(data_list).sort_values('size')

# 2. Création des graphiques en échelle Log
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# Fonction utilitaire pour éviter de répéter le formatage log
def setup_log_ax(ax, title, ylabel):
    ax.set_yscale('log')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both", ls="-", alpha=0.5)

# Graph 1: Iteration Time
axs[0, 0].plot(df_res['size'], df_res['nw_max_iter'], 'o-', label='NorthWest')
axs[0, 0].plot(df_res['size'], df_res['bh_max_iter'], 's-', label='Balas Hammer')
setup_log_ax(axs[0, 0], "Max Iteration Time (Log Scale)", "Temps (s)")
axs[0, 0].legend()

# Graph 2: SS Columns
axs[0, 1].plot(df_res['size'], df_res['ss_nw_max_iter'], 'o-', color='green', label='SS NW')
axs[0, 1].plot(df_res['size'], df_res['ss_bh_max_iter'], 's-', color='red', label='SS Balas')
setup_log_ax(axs[0, 1], "Max Stepping Stone Time (Log Scale)", "Temps (s)")
axs[0, 1].legend()

# Graph 3: Total Time
axs[1, 0].plot(df_res['size'], df_res['nw_total_time'], 'o-', color='purple', label='Total NW')
axs[1, 0].plot(df_res['size'], df_res['bh_total_time'], 's-', color='orange', label='Total Balas')
setup_log_ax(axs[1, 0], "Total Time (Log Scale)", "Temps (s)")
axs[1, 0].legend()

# Graph 4: Ratio NW/BH
ratio = df_res['nw_total_time'] / df_res['bh_total_time']
axs[1, 1].plot(df_res['size'], ratio, 'D-', color='black', label='Ratio NW/BH')
axs[1, 1].axhline(y=1, color='red', linestyle='--')
setup_log_ax(axs[1, 1], "Ratio Total Time NW/BH (Log Scale)", "Ratio")
axs[1, 1].legend()

plt.tight_layout()
plt.show()