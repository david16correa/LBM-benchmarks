# ---------------------------------------------------------------------------------------------
# ------------------------------------------ preamble -----------------------------------------
# ---------------------------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd

mpl.rc("figure", dpi=150)
mpl.rc("figure", figsize=(4,4))

plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'xtick.labelsize':9,
    'ytick.labelsize':9,
    'axes.labelsize':12,
})

# extra stuff
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter
import math
from scipy.spatial import cKDTree  # For finding nearest neighbors

# formatting
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-2, 2))  # Sets limits for when to use scientific notation


# ---------------------------------------------------------------------------------------------
# ------------------------------------------ methods ------------------------------------------
# ---------------------------------------------------------------------------------------------
def fluidOverview(df, particleDf, title, maxFluidSpeed = 1e-3, massDensityEpsilon = 1e-3):
#     df = df.query('coordinate_y <= 10 & coordinate_y >= -10')
    # figure preparation
#     fig, axes = plt.subplots(figsize = (5,2.5))
    fig, axes = plt.subplots(2, 1, figsize = (4,3))

#     fig.suptitle(f"$t = {df.time.values[0]:.2f}$", fontsize=16)
    fig.suptitle(title, fontsize=12)
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar


    # Create a meshgrid for plotting
    x_unique = df['coordinate_x'].unique()
    y_unique = df['coordinate_y'].unique()
    X, Y = np.meshgrid(x_unique, y_unique)
    
    xmax = x_unique.max()
    xmin = x_unique.min()
    ymax = y_unique.max()
    ymin = y_unique.min()

    # first plot
    upperLim = maxFluidSpeed
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

    axes[0].tick_params(labelbottom=False)
    axes[0].set_xticks([xmin, 0,xmax])
    axes[0].set_xticklabels([f'{xmin:.0f}', 0,f'{xmax:.0f}'])
    # axes[0].set_xlabel("$x ~ (\\mathrm{\\mu m})$")
    axes[0].set_yticks([ymin, 0, ymax])
    axes[0].set_yticklabels([f'{ymin:.0f}', 0,f'{ymax:.0f}'])
    # axes[0].set_ylabel("$y ~ (\\mathrm{\\mu m})$")

    fig.text(
        0.01, 0.5,
        '$y ~ (\\mu \\mathrm{m})$',
        va='center',
        ha='center',
        rotation='vertical',
        fontsize=12
    )


    cbar_ax = fig.add_axes([0.9, 0.55, 0.025, 0.3])  # [left, bottom, width, height] for the colorbar
#     cbar_ax = fig.add_axes([0.9, 0.15, 0.025, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$\\mathbf{u}$', fontsize=16)
#     cbar.set_label(label='$|\\mathbf{u}| ~ \\left(10^{-3}~\\mathrm{mm}/\\mathrm{s}\\right)$', fontsize=16)
    cbar.ax.tick_params(labelsize=15)

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels([f'{tick:.4f}' for tick in custom_ticks])
#     cbar.set_ticklabels(['$0$','$1.5$','$3$'])

    # bottom plot
    epsilon = massDensityEpsilon
    upperLim = 1. + epsilon
    lowerLim = 1. - epsilon
    cmap = plt.get_cmap('seismic')
    norm = plt.Normalize(lowerLim, upperLim)
    axes[1].pcolormesh(X,Y,
        df.massDensity.unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap,
    );
    
    axes[1].set_xticks([xmin, 0,xmax])
    axes[1].set_xticklabels([f'{xmin:.0f}', 0,f'{xmax:.0f}'])
    axes[1].set_xlabel("$x ~ (\\mathrm{\\mu m})$")
    axes[1].set_yticks([ymin, 0, ymax])
    axes[1].set_yticklabels([f'{ymin:.0f}', 0,f'{ymax:.0f}'])
    # axes[1].tick_params(labeldown=False)
#     axes[1].set_ylabel("$y ~ (\\mathrm{mm})$")

    cbar_ax = fig.add_axes([0.9, 0.13, 0.025, 0.3])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label(label='$\\rho$', fontsize=16)
    cbar.ax.tick_params(labelsize=15)

    custom_ticks = np.array([lowerLim, 1 ,upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels(custom_ticks)
    cbar.set_ticklabels([f'{tick:.3f}' for tick in custom_ticks])

    auxDf = particleDf.query(f"tick<={df.tick.values[0]}")
    particleIds = np.unique(particleDf.particleId.values)
    for id in particleIds:
        axes[0].plot(auxDf.query(f'particleId == {id}').position_x, auxDf.query(f'particleId == {id}').position_y, color='magenta', alpha = 0.5, linewidth=2, zorder=4)  # Trajectory line
        axes[1].plot(auxDf.query(f'particleId == {id}').position_x, auxDf.query(f'particleId == {id}').position_y, color='magenta', alpha = 0.5, linewidth=2, zorder=4)  # Trajectory line

    plt.subplots_adjust(wspace=0.5)  # smaller wspace = less horizontal space between plots
    return fig, axes

def pltFluidVelocity(df, particleDf, maxFluidSpeed = 1e-3):
#     df = df.query('coordinate_y <= 10 & coordinate_y >= -10')
    # figure preparation
#     fig, axes = plt.subplots(figsize = (5,2.5))
    fig, axes = plt.subplots(figsize = (4.5,1.5))

    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar


    positionX = particleDf.query(f"particleId == {2}").position_x.values[-1]
    positionY = particleDf.query(f"particleId == {2}").position_y.values[-1]

    df = df.query(f'(coordinate_x - {positionX})**2 <= {70}**2')

    particleDf = particleDf.query(f"time == {df.time.values[-1]}")

    # Create a meshgrid for plotting
    x_unique = df['coordinate_x'].unique()
    y_unique = df['coordinate_y'].unique()
    X, Y = np.meshgrid(x_unique, y_unique)

    xmax = x_unique.max()
    xmin = x_unique.min()
    ymax = y_unique.max()
    ymin = y_unique.min()

    # first plot
    upperLim = maxFluidSpeed
    lowerLim = 0.
    cmap = plt.get_cmap('cividis')
    norm = plt.Normalize(lowerLim, upperLim)

    axes.streamplot(X, Y, 
        df.fluidVelocity_x.unstack().values.transpose(),
        df.fluidVelocity_y.unstack().values.transpose(),
        density=0.85, linewidth=0.5, color="black",
    )

    axes.pcolormesh(X, Y,
        np.sqrt(df.fluidVelocity_x**2 + df.fluidVelocity_y**2).unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap, alpha = 0.85
    );

    # axes.tick_params(labelbottom=False)
    axes.set_xticks([xmin, 0,xmax])
    axes.set_xticklabels([f'{xmin:.0f}', 0,f'{xmax:.0f}'])
    axes.set_xlabel("$x ~ (\\mathrm{\\mu m})$")
    axes.set_yticks([ymin, 0, ymax])
    axes.set_yticklabels([f'{ymin:.0f}', 0,f'{ymax:.0f}'])
    axes.set_ylabel("$y ~ (\\mathrm{\\mu m})$")

    cbar_ax = fig.add_axes([0.9, 0.15, 0.025, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$\\mathbf{u}$')

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
    # cbar.set_ticklabels([0, 0.5, 1])
    cbar.set_ticklabels(['$0$','$W/2$','$W$'])

    beadRadius = 3

    myColor='#F7F7F7'
    for id in range(3):
        positionX = particleDf.query(f"particleId == {id+1}").position_x.values[-1]
        positionY = particleDf.query(f"particleId == {id+1}").position_y.values[-1]
        mask = Circle((positionX, positionY), beadRadius, transform=axes.transData, color=myColor, linestyle='', alpha=1, zorder=2)
        axes.add_patch(mask)

    return fig, axes

def fluidOverview2(df1, df2, title):
    fig, axes = plt.subplots(1, 2, figsize = (6,2.7))

    fig.suptitle(title, fontsize=16, y=1.05)
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar

    # Create a meshgrid for plotting
    x_unique = df1['coordinate_x'].unique()
    y_unique = df1['coordinate_y'].unique()
    X, Y = np.meshgrid(x_unique, y_unique)
    
    xmax = x_unique.max()
    xmin = x_unique.min()
    ymax = y_unique.max()
    ymin = y_unique.min()

    # first plot
    axes[0].set_title("particle frame")
    upperLim = 1e-3 * 2/3 + 1e-4 # maximum fluid speed should be 2/3*1e-3
    lowerLim = 0.
    cmap = plt.get_cmap('cividis')
    norm = plt.Normalize(lowerLim, upperLim)

    axes[0].streamplot(X, Y, 
        df1.fluidVelocity_x.unstack().values.transpose(),
        df1.fluidVelocity_y.unstack().values.transpose(),
        density=0.85, linewidth=0.5, color="black",
    )
    
    
    axes[0].pcolormesh(X, Y,
        np.sqrt(df1.fluidVelocity_x**2 + df1.fluidVelocity_y**2).unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap, alpha = 0.85
    );

    axes[0].set_xticks([xmin, 0,xmax])
    axes[0].set_xticklabels([f'{xmin:.0f}', 0,f'{xmax:.0f}'])
    axes[0].set_xlabel("$x ~ (\\mathrm{\\mu m})$")
    axes[0].set_yticks([ymin, 0, ymax])
    axes[0].set_yticklabels([f'{ymin:.0f}', 0,f'{ymax:.0f}'])
    axes[0].set_ylabel("$y ~ (\\mathrm{\\mu m})$")

    cbar_ax = fig.add_axes([0.9, 0.15, 0.025, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$\\mathbf{u}$', fontsize=16)
#     cbar.set_label(label='$|\\mathbf{u}| ~ \\left(10^{-3}~\\mathrm{mm}/\\mathrm{s}\\right)$', fontsize=16)
    cbar.ax.tick_params(labelsize=15)

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels([f'{tick:.4f}' for tick in custom_ticks])
#     cbar.set_ticklabels(['$0$','$1.5$','$3$'])

    # bottom plot
    axes[1].set_title("lab frame")
    axes[1].streamplot(X, Y, 
        df2.fluidVelocity_x.unstack().values.transpose(),
        df2.fluidVelocity_y.unstack().values.transpose(),
        density=0.85, linewidth=0.5, color="black",
    )
    
    
    axes[1].pcolormesh(X, Y,
        np.sqrt(df2.fluidVelocity_x**2 + df2.fluidVelocity_y**2).unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap, alpha = 0.85
    );

    axes[1].set_xticks([xmin, 0,xmax])
    axes[1].set_xticklabels([f'{xmin:.0f}', 0,f'{xmax:.0f}'])
    axes[1].set_xlabel("$x ~ (\\mathrm{\\mu m})$")
    axes[1].set_yticks([ymin, 0, ymax])
    axes[1].tick_params(labelleft=False)
    
    return fig, axes

def plotTrj(ogDf, targetTime = -1):
    radius = 3
    e = 3*radius
    D = 10*radius
    W = 1e-2
    expectedSpeed = 0.7 * W * (radius/D) * ((D - e)/D)**2


    totalTime = ogDf.time.values[-1]

    if targetTime == -1:
        targetTime = totalTime

    df = ogDf.query(f"time<={targetTime}")
    particleTime = df.time.values

    fig, axes = plt.subplots(figsize=(3,1.5))

    particleTime = df.time.unique()
    nParticles = len(df.particleId.unique())
    for Id in np.arange(nParticles):
        axes.plot(particleTime, df.query(f"particleId == {Id+1}").position_x.values, alpha = 0.85, label=f"$x_{Id+1}$", zorder = 2)

    axes.plot(particleTime, particleTime * expectedSpeed, color = "black", alpha = 0.5, linewidth=1, linestyle='dashed', zorder = 1)

    for onset in [n * 8400 for n in range(6) if n*8400 <= targetTime+1]:
        axes.axvline(onset, color = "#CA3D34", alpha = 0.5, linewidth=1, linestyle='dashed', zorder = 0)

    axes.set_xlim(0, 4.3e4)
    axes.set_xticks([0, 1e4, 2e4, 3e4, 4e4])
    axes.set_xticklabels([0, 10, 20, 30, 40])

    axes.set_ylim(-35,50)
    axes.set_yticks([-30, 0, 30])

    axes.set_xlabel("$t ~ (\\mathrm{ms})$")
    axes.set_ylabel("$x ~ (\\mu \\mathrm{m})$")

    return fig, axes
