# ==========================================================================================
# ==========================================================================================
# preamble
# ==========================================================================================
# ==========================================================================================

# important stuff
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
# extra stuff
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter
import math

mpl.rc("figure", dpi=150)
mpl.rc("figure", figsize=(4,4))

plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'xtick.labelsize':15,
    'ytick.labelsize':15,
    'axes.labelsize':20,
})

# formatting
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-2, 2))  # Sets limits for when to use scientific notation

# directory of the data is saved
dataDir = f'../data.lbm/'
# dataDir = f'output.lbm/'

# all ticks are found using regular expressions
pattern = r'fluidTrj_(\d+)\.csv'
files = os.listdir(dataDir)
ticks = []

for file in files:
    match = re.search(pattern, file)
    if match:
        ticks.append(int(match.group(1)))

ticks.sort()

# directory where files will be saved is created
outputDir = "frames.lbm"
os.makedirs(outputDir, exist_ok=True)
os.makedirs("anims", exist_ok=True)

# ==========================================================================================
# ==========================================================================================
# plotting
# ==========================================================================================
# ==========================================================================================

def fluidOverview(df):
    df = df.query('coordinate_y <= 10 & coordinate_y >= -10')
    # figure preparation
#     fig, axes = plt.subplots(figsize = (5,2.5))
    fig, axes = plt.subplots(2, 1, figsize = (5,5))

#     fig.suptitle(f"$t = {fluidDf.time.values[0]:.0f}$", fontsize=16)
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar

    # Create a meshgrid for plotting
    x_unique = df['coordinate_x'].unique()
    y_unique = df['coordinate_y'].unique()
    X, Y = np.meshgrid(x_unique, y_unique)

    # first plot
    upperLim = 0.003
    lowerLim = 0.
    cmap = plt.get_cmap('cividis')
    norm = plt.Normalize(lowerLim, upperLim)

    axes[0].streamplot(X, Y, 
        df.fluidVelocity_x.unstack().values.transpose(),
        df.fluidVelocity_y.unstack().values.transpose(),
        density=0.85, linewidth=0.5, color="black",
    )


    axes[0].pcolormesh(X, Y,
        np.sqrt(df.fluidVelocity_x**2 + df.fluidVelocity_y**2).unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap, alpha = 0.85
    );
#     axes[0].tick_params(labelbottom=False)
    axes[0].set_xticks([-20, 0, 20])
    axes[0].set_xlabel("$x ~ (\\mathrm{mm})$")
    axes[0].set_yticks([-10, 0, 10])
    axes[0].set_ylabel("$y ~ (\\mathrm{mm})$")

    cbar_ax = fig.add_axes([0.9, 0.55, 0.025, 0.3])  # [left, bottom, width, height] for the colorbar
#     cbar_ax = fig.add_axes([0.9, 0.15, 0.025, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$|\\mathbf{u}| ~ \\left(10^{-3}~\\mathrm{mm}/\\mathrm{s}\\right)$', fontsize=16)
    cbar.ax.tick_params(labelsize=15)

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
#     cbar.set_ticklabels([f'{tick:.3f}' for tick in custom_ticks])
    cbar.set_ticklabels(['$0$','$1.5$','$3$'])

    # bottom plot
    upperLim = 1.01
    lowerLim = 0.99
    cmap = plt.get_cmap('seismic')
    norm = plt.Normalize(lowerLim, upperLim)
    axes[1].pcolormesh(X,Y,
        df.massDensity.unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap,
    );
    axes[1].set_xticks([-20, 0, 20])
    axes[1].set_xlabel("$x ~ (\\mathrm{mm})$")
    axes[1].set_yticks([-10, 0, 10])
    axes[1].set_ylabel("$y ~ (\\mathrm{mm})$")

    cbar_ax = fig.add_axes([0.9, 0.13, 0.025, 0.3])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label(label='$\\rho$', fontsize=16)
    cbar.ax.tick_params(labelsize=15)

    custom_ticks = np.array([lowerLim, 1 ,upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels(custom_ticks)
    cbar.set_ticklabels([f'{tick:.2f}' for tick in custom_ticks])

    return fig, axes

# the data is read
for tickId in np.arange(len(ticks)):
    fluidDf = pd.read_csv(dataDir + f"fluidTrj_{ticks[tickId]}.csv").set_index(["id_x","id_y"]).sort_index()
    fig, axes = fluidOverview(fluidDf)
    plt.savefig(f"{outputDir}/{tickId}.png", format="png", dpi=1000, bbox_inches="tight")
    plt.close()

mkAnimSh = f'ffmpeg -loglevel quiet -framerate 5 -i {outputDir}/%d.png -c:v libx264 -pix_fmt yuv420p anims/output.mp4'
os.system(mkAnimSh)
# os.system(f'rm -r {outputDir}')


# ffmpeg -loglevel quiet -framerate 5 -i frames.lbm/%d.png -c:v libx264 -pix_fmt yuv420p anims/output.mp4
