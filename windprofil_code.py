# Windprofile

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Speicherpfad

BASE_DIR = Path(__file__).resolve().parent
plots_path = BASE_DIR / "Plots"
windprofile_path = plots_path / "Windprofile (Gebiet, Referenzhöhe)"
windprofile_path.mkdir(exist_ok=True)

# Faktoren im Potenzansatz (Oberflächenrauhigkeit) vgl. VDI 3782/1

m_land = {"I": 0.37, "II": 0.32, "III/1": 0.26, "III/2": 0.18, "IV": 0.14, "V": 0.12}
m_stadt = {"I": 0.52, "II": 0.48, "III/1": 0.31, "III/2": 0.31, "IV": 0.31, "V": 0.20}

# Ausbreitungsklassen (sehr stabile (I) und neutrale (III/2) Schichtung ausgewählt)

disp_kla=["I", "III/2"]
all_kla=["I", "II", "III/1", "III/2", "IV", "V"]

# Definition Höhe Windprofile

z=np.linspace(10,200,100)


# Referenzhöhen [m] & Referenzwindgeschwindigkeiten [m/s] (frei wählbar)
# Aufrunden bei zweiter Nachkommastelle ab 5

z_A = [10, 150]     

u_A = {
    "10": 4.5,  # 10m = 4,5m/s (Wert: 4,12m/s)
    "150": 9.0  # 150m = 9,0 m/s (Wert: 8,46m/s)
}

# Definition Windprofil-Funktion (s. Abschnitt II 'Methoden')

def windprofil(u_A,z,z_A,m):
    """
    u_A - Windgeschwindigkeit in Referenzhöhe [m/s]
    z   - Höhe [m]
    z_A - Referenzhöhe [m]
    m   - Ausbreitungsklasse
    """
    return u_A*(z/z_A)**m

# Windprofil berechnen (Schleife über Referenzhöhe für die Klassen I und III/2)

u_land = {}
u_stadt = {}

for hoehe in z_A:
    u_land[hoehe] = {}
    u_stadt[hoehe] = {}
    for kla in disp_kla:
        u_land[hoehe][kla] = windprofil(u_A[str(hoehe)], z, hoehe, m_land[kla])
        u_stadt[hoehe][kla] = windprofil(u_A[str(hoehe)], z, hoehe, m_stadt[kla])


# Ausgabe der Windgeschwindigkeit bei 50 m für Land und Stadt bei einer Referenzhöhe von 10 m 
# Zusatzausgabe 

idx_50 = np.argmin(np.abs(z - 50))

print()
print("Windgeschwindigkeit bei 50 m Höhe:")
print()
print("Land, I:     ", round(u_land[10]["I"][idx_50], 2))
print("Land, III/2: ", round(u_land[10]["III/2"][idx_50], 2))
print("Stadt, I:    ", round(u_stadt[10]["I"][idx_50], 2))
print("Stadt, III/2:", round(u_stadt[10]["III/2"][idx_50], 2))
print()


# Ausgabe der Windgeschwindigkeiten über verschiedene Höhen für das Gauß-Fahnenmodell
# Referenzhöhe: 150m

u_all_land = {}
u_all_stadt = {}

for hoehe in [10, 20, 30, 40, 50, 150]:
    u_all_land[hoehe] = {}
    u_all_stadt[hoehe] = {}
    for kla in all_kla:
        u_all_land[hoehe][kla] = round(windprofil(u_A["150"], hoehe, 150, m_land[kla]), 2)
        u_all_stadt[hoehe][kla] = round(windprofil(u_A["150"], hoehe, 150, m_stadt[kla]), 2)

print("Land:", u_all_land)
print("Stadt:", u_all_stadt)

# Werte werden durch die vorgegebenden Rechenwerte (VDI 3782/1) für das 
# Gauß-Fahnenmodell umgerechnet (s. dazu Abschnitt II)

# Land: 
# 10: {'I': 3.3, 'II': 3.78, 'III/1': 4.45, 'III/2': 5.53, 'IV': 6.16, 'V': 6.5},
# 20: {'I': 4.27, 'II': 4.72, 'III/1': 5.33, 'III/2': 6.26, 'IV': 6.79, 'V': 7.07}, 
# 30: {'I': 4.96, 'II': 5.38, 'III/1': 5.92, 'III/2': 6.74, 'IV': 7.18, 'V': 7.42},
# 40: {'I': 5.52, 'II': 5.9, 'III/1': 6.38, 'III/2': 7.09, 'IV': 7.48, 'V': 7.68},
# 50: {'I': 5.99, 'II': 6.33, 'III/1': 6.76, 'III/2': 7.39, 'IV': 7.72, 'V': 7.89}

#Stadt: 
# 10: {'I': 2.2, 'II': 2.45, 'III/1': 3.89, 'III/2': 3.89, 'IV': 3.89, 'V': 5.24}, 
# 20: {'I': 3.16, 'II': 3.42, 'III/1': 4.82, 'III/2': 4.82, 'IV': 4.82, 'V': 6.01}, 
# 30: {'I': 3.9, 'II': 4.16, 'III/1': 5.46, 'III/2': 5.46, 'IV': 5.46, 'V': 6.52}, 
# 40: {'I': 4.53, 'II': 4.77, 'III/1': 5.97, 'III/2': 5.97, 'IV': 5.97, 'V': 6.91}, 
# 50: {'I': 5.08, 'II': 5.31, 'III/1': 6.4, 'III/2': 6.4, 'IV': 6.4, 'V': 7.22}

# Ausgabedateien

output_file_land_10 = "Windprofil (Land, Referenzhöhe 10m).png"
output_file_stadt_10 = "Windprofil (Stadt, Referenzhöhe 10m).png"
output_file_land_150 = "Windprofil (Land, Referenzhöhe 150m).png"
output_file_stadt_150 = "Windprofil (Stadt, Referenzhöhe 150m).png"
output_file_vgl_10 ="Windprofil (Vergleich Land & Stadt, Referenzhöhe 10m)_neu.png"
output_file_vgl_150 ="Windprofil (Vergleich Land & Stadt, Referenzhöhe 150m)_neu.png"

# Plots: Windprofile für neutrale und stabile Schichtung (Land & Stadt)

# Einstellungen:

plt.rc('legend', fontsize=8)
plt.rcParams["figure.dpi"] = 150
colors = {'I': 'red', 'III/2': 'blue'}

# Windprofil - Land, Referenzhöhe 10m

plt.figure(1, dpi=300)
for kla in ["I", "III/2"]:
    plt.plot(u_land[10][kla], z, label=kla, color=colors[kla])
plt.xlabel("Windgeschwindigkeit [m/s]", fontweight='bold')
plt.ylabel("Höhe über Grund [m]", fontweight='bold')
plt.title("Windprofil - Land, Referenzhöhe 10m", fontweight='bold')
plt.legend()
plt.grid(True, linewidth=0.4, color='lightgray')
plt.savefig(windprofile_path / output_file_land_10)

# Windprofil - Stadt, Referenzhöhe 10m

plt.figure(2, dpi=300)
for kla in ["I", "III/2"]:
    plt.plot(u_stadt[10][kla], z, label=kla, color=colors[kla])
plt.xlabel("Windgeschwindigkeit [m/s]", fontweight='bold')
plt.ylabel("Höhe über Grund [m]", fontweight='bold')
plt.title("Windprofil - Stadt, Referenzhöhe 10m", fontweight='bold')
plt.legend()
plt.grid(True, linewidth=0.4, color='lightgray')
plt.savefig(windprofile_path / output_file_stadt_10)

# Windprofil - Land, Referenzhöhe 150m

plt.figure(3, dpi=300)
for kla in ["I", "III/2"]:
    plt.plot(u_land[150][kla], z, label=kla, color=colors[kla])
plt.xlabel("Windgeschwindigkeit [m/s]", fontweight='bold')
plt.ylabel("Höhe über Grund [m]", fontweight='bold')
plt.title("Windprofil - Land, Referenzhöhe 150m", fontweight='bold')
plt.legend()
plt.grid(True, linewidth=0.4, color='lightgray')
plt.savefig(windprofile_path / output_file_land_150)

# Windprofil - Stadt, Referenzhöhe 150m

plt.figure(4, dpi=300)
for kla in ["I", "III/2"]:
    plt.plot(u_stadt[150][kla], z, label=kla, color=colors[kla])
plt.xlabel("Windgeschwindigkeit [m/s]", fontweight='bold')
plt.ylabel("Höhe über Grund [m]", fontweight='bold')
plt.title("Windprofil - Stadt, Referenzhöhe 150m", fontweight='bold')
plt.legend()
plt.grid(True, linewidth=0.4, color='lightgray')
plt.savefig(windprofile_path / output_file_stadt_150)

# Windprofil - Vergleich Land & Stadt, Referenzhöhe 10m

plt.figure(5, dpi=300)
for kla in ["I", "III/2"]:
    plt.plot(u_land[10][kla], z, '--', color=colors[kla], label=f"Land, {kla}")
    plt.plot(u_stadt[10][kla], z, '-', color=colors[kla], label=f"Stadt, {kla}")
plt.xlabel("Windgeschwindigkeit [m/s]", fontweight='bold')
plt.ylabel("Höhe über Grund [m]", fontweight='bold')
plt.title("Windprofil - Vergleich Land & Stadt, 10m", fontweight='bold')
plt.legend()
plt.grid(True, linewidth=0.4, color='lightgray')
plt.savefig(windprofile_path / output_file_vgl_10)

# Windprofil - Vergleich Land & Stadt, Referenzhöhe 150m

plt.figure(6, dpi=300)
for kla in ["I", "III/2"]:
    plt.plot(u_land[150][kla], z, '--', color=colors[kla], label=f"Land, {kla}")
    plt.plot(u_stadt[150][kla], z, '-', color=colors[kla], label=f"Stadt, {kla}")
plt.xlabel("Windgeschwindigkeit [m/s]", fontweight='bold')
plt.ylabel("Höhe über Grund [m]", fontweight='bold')
plt.title("Windprofil - Vergleich Land & Stadt, 150m", fontweight='bold')
plt.legend()
plt.grid(True, linewidth=0.4, color='lightgray')
plt.savefig(windprofile_path / output_file_vgl_150)
