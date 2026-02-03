# Gauß-Fahnenmodell

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path

# Speicherpfade

BASE_DIR = Path(__file__).resolve().parent
plots_path = BASE_DIR / "Plots"
emissions_path = plots_path / "Emissionskonzentrationen (Klasse, Gebiet, 10-50m)"
immissions_path = plots_path / "Immissionskonzentration (Höhe, Klasse, Rauhigkeit, Gebiet)"
immissions_path.mkdir(parents=True, exist_ok=True)
emissions_path.mkdir(parents=True, exist_ok=True)

# Gebiete festlegen

gebiet = "Stadt"   # oder "Land"

# Fahnenausbreitungsparameter für effektive Quellhöhe bis 50m 

F={"I":1.294, "II": 0.801, "III/1": 0.640, "III/2":0.659, "IV": 0.876, "V": 1.503}
G={"I":0.241, "II": 0.264, "III/1": 0.215, "III/2":0.165, "IV": 0.127, "V": 0.151}
f={"I":0.718, "II": 0.754, "III/1": 0.784, "III/2":0.807, "IV": 0.823, "V": 0.833}
g={"I":0.662, "II": 0.774, "III/1": 0.885, "III/2":0.996, "IV": 1.108, "V": 1.219}

# Windgeschwindigkeit in Emissionshöhe [m/s] (s. Windprofile)
# Höhen [m]: 10, 20, 30, 40, 50
# Aufrunden bei zweiter Nachkommastelle ab 5

u_land = {
    "I":    [3.0,4.5,4.5,6.0,6.0],
    "II":   [3.0,4.5,4.5,6.0,6.0],
    "III/1":[4.5,4.5,6.0,6.0,6.0],
    "III/2":[6.0,6.0,6.0,7.5,7.5],
    "IV":   [6.0,6.0,7.5,7.5,7.5],
    "V":    [6.0,7.5,7.5,7.5,7.5]
}

u_stadt = {
    "I":    [2.0,3.0,4.5,4.5,4.5],
    "II":   [3.0,3.0,4.5,4.5,4.5],
    "III/1":[4.5,4.5,6.0,6.0,6.0],
    "III/2":[4.5,4.5,6.0,6.0,6.0],
    "IV":   [4.5,4.5,6.0,6.0,6.0],
    "V":    [4.5,6.0,6.0,6.0,7.5]
}

u = u_land if gebiet == "Land" else u_stadt

# Ausbreitungsklassen & Emissionshöhen [m]

disp_kla=["I"] # z.B. ["I", "II", "III/1", "III/2", "IV", "V"]
hoehen=[10,20,30,40,50]

# Definition Gaußfunktion (s. Abschnitt 2 'Methoden')

def c(x,y,z,H,u,disp_kla):
    """
    x        - Longitudinalkoordinate mit Ursprung in der Fahnenmitte
    y        - Lateralkoordinate mit Ursprung in der Fahnenmitte
    z        - Höhe über Grund [m]
    H        - Effektive Fahnenhöhe [m]
    u        - Windgeschwindigkeit aus Windprofilen [m/s]
    disp_kla - Ausbreitungsklassen (m)
    return   - Immissionskonzentrationen für verschiedene Höhen je Klasse
    """
    sigma_y=F[disp_kla]*(x/1)**f[disp_kla]
    sigma_z=G[disp_kla]*1*(x/1)**g[disp_kla]
    Quellterm=1/(u*2*np.pi*sigma_y*sigma_z)
    exp_y=np.exp(-(y**2) / (2*sigma_y**2))
    exp_z=np.exp(-0.5*((z-H) / sigma_z)**2)+np.exp(-0.5*((z+H) /sigma_z)**2)
    c=Quellterm*exp_y*exp_z
    return c

# Distanen zur Quelle

x=np.linspace(1,1000,100)

# Plot: Emissionskonzentration je Ausbreitungsklasse mit verschiedenen Freisetzungshöhen  

plt.rc('legend', fontsize=8)

colors = ['red', 'navy', 'deepskyblue', 'orange', 'green']

for disp in range(len(disp_kla)):
    kla = disp_kla[disp]
    name_kla = str(kla).replace("/", "_")

    for hoehe in range(len(hoehen)):
        H = hoehen[hoehe]
        u_neu = u[kla][hoehe]

        plt.plot(
            x,
            c(x, 0, 0, H, u_neu, kla) * 1e6,
            label=f"{H} m Emissionshöhe",
            color=colors[hoehe % len(colors)],
            linewidth=1.8
        )

    plt.title(f"Ausbreitungsklasse {kla}, {gebiet}", fontweight='bold')
    plt.xlabel("Entfernung zur Quelle [m]", fontweight='bold')
    plt.ylabel(r"$\mathbf{Emittierte\ Konzentration\ [ppm] }$")

    plt.minorticks_on()
    plt.grid(True, which='both', linewidth=0.4, color='lightgray')

    plt.legend()
    plt.savefig(emissions_path / f"Emissionskonzentration (Klasse {name_kla}, {gebiet}, 10-50m).png", dpi=300)
    plt.show()
    
# Plot: Immissionskonzentration in verschiedenen Freisetzungshöhen (Fläche)

plt.rc('legend', fontsize=8)
plt.rcParams["figure.dpi"] = 150   

levels = [1, 2, 3, 4, 5, 7, 10, 14, 19, 25]
level_colors = ['red', 'orange', 'green', 'deepskyblue', 'navy',
                'purple', 'brown', 'magenta', 'olive', 'black']

x = np.linspace(1, 4200, 3500)
y = np.linspace(-400, 400, 800)
X, Y = np.meshgrid(x, y)

for hoehe in range(len(hoehen)):
    H_neu = hoehen[hoehe]
    kla_neu = "V" # z.B. ["I", "II", "III/1", "III/2", "IV", "V"]
    u_neu = u[kla_neu][hoehe]
    C = c(X, Y, 0, H_neu, u_neu, kla_neu) * 1e6

    fig, ax = plt.subplots()

    contours = ax.contour(X, Y, C, levels=levels, colors=level_colors, linewidths=1.8, antialiased=True)    

    ax.set_xlabel("Entfernung x [m]", fontweight='bold')
    
    ax.set_ylabel("Entfernung y [m]", fontweight='bold')
    
    ax.set_title(f"Ausbreitungskategorie {kla_neu}, Höhe {H_neu} m, {gebiet}", fontweight='bold')
   
    ax.set_xticks(np.arange(0, 4201, 400))
    ax.set_yticks(np.arange(-400, 401, 200))

    ax.set_xlim(-100, 4200)
    ax.set_ylim(-420, 420)
    
    ax.set_axisbelow(False)
    ax.grid(True, linewidth=0.4, color='lightgray', zorder=10)
    ax.tick_params(zorder=11)

    ax.set_aspect('equal', adjustable='box')

    legend_elements = [Line2D([0], [0], color=level_colors[i], lw=2, label=f"{levels[i]}")
        for i in range(len(levels))]
    
    ax.legend(handles=legend_elements, title='Konzentrationen [ppm]', loc='upper center', 
          bbox_to_anchor=(0.5, -0.5), ncol=5, frameon=True)

    fig.savefig(immissions_path / f"Immissionskonzentration (Höhe {H_neu}m, Klasse {kla_neu.replace('/', '_')}, {gebiet}).png", 
            dpi=300, bbox_inches="tight")
    plt.show()
    
