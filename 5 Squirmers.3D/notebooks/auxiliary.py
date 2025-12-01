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
def squirmersOverview(df1, df2, df3, particleDf1, particleDf2, particleDf3, lims):
#     df = df.query('coordinate_y <= 10 & coordinate_y >= -10')
    # figure preparation
#     fig, axes = plt.subplots(figsize = (5,2.5))
    fig, axes = plt.subplots(1, 3, figsize = (5.25,1.5))

#     fig.suptitle(f"$t = {df.time.values[0]:.2f}$", fontsize=16)
    # fig.suptitle(title, fontsize=16)
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar


    dfs = [df1, df2, df3]
    particleDfs = [particleDf1, particleDf2, particleDf3]

    for id in range(3):
        df = dfs[id]
        particleDf = particleDfs[id]

        particleDf = particleDf.query(f"tick<={df.tick.values[0]}")
        positionX = particleDf.position_x.values[-1]
        positionY = particleDf.position_y.values[-1]
        positionZ = particleDf.position_z.values[-1]

        positionZid = np.abs(df.coordinate_z.values - positionZ).argmin()
        positionZ = df.coordinate_z.values[positionZid]

        df = df.query(f'(coordinate_x - {positionX})**2 <= {lims}**2 & (coordinate_y - {positionY})**2 <= {lims}**2 & coordinate_z == {positionZ} ')

        x_unique = df['coordinate_x'].unique()
        # Create a meshgrid for plotting
        y_unique = df['coordinate_y'].unique()
        X, Y = np.meshgrid(x_unique, y_unique)

        xmax = x_unique.max()
        xmin = x_unique.min()
        ymax = y_unique.max()
        ymin = y_unique.min()

        # finally plotting
        upperLim = 1e-4 * 2/3 # maximum fluid speed should be 2/3*1e-3
        lowerLim = 0.
        cmap = plt.get_cmap('cividis')
        norm = plt.Normalize(lowerLim, upperLim)

        axes[id].streamplot(X, Y, 
            df.fluidVelocity_x.unstack().values.transpose(),
            df.fluidVelocity_y.unstack().values.transpose(),
            density=0.5, linewidth=0.5, color="black",
        )


        axes[id].pcolormesh(X, Y,
            np.sqrt(df.fluidVelocity_x**2 + df.fluidVelocity_y**2).unstack().values.transpose(),
            vmin=lowerLim,
            vmax=upperLim,
            cmap=cmap, alpha = 0.85
        );

        axes[id].set_xticks([xmin, 0,xmax])
        axes[id].set_xticklabels([f'{xmin:.0f}', 0,f'{xmax:.0f}'])
        axes[id].set_yticks([ymin, 0, ymax])
        axes[id].set_yticklabels([f'{ymin:.0f}', 0,f'{ymax:.0f}'])

        if id == 0:
            axes[id].set_ylabel("$y ~ (\\mathrm{\\mu m})$")
        else:
            axes[id].tick_params(labelleft=False)

        if id == 1:
            axes[id].set_xlabel("$x ~ (\\mathrm{\\mu m})$")

        squirmerRadius = 4;

        # Create a mask as a filled polygon (circle patch with alpha for masking)
        myColor='#F7F7F7'
        mask = Circle((positionX, positionY), squirmerRadius, transform=axes[id].transData, color=myColor, linestyle='', alpha=1, zorder=2)
        axes[id].add_patch(mask)

        particleDf = particleDf.query(f"(position_x - {positionX})**2 + (position_y - {positionY})**2 < ({squirmerRadius}/2)**2")

        # axes[id].plot(particleDf.position_x[:-2], particleDf.position_y[:-2], color='magenta', alpha = 0.5, linewidth=1, zorder=4)  # Trajectory line

        axes[id].arrow(
            particleDf.position_x.values[0], particleDf.position_y.values[0],
            positionX - particleDf.position_x.values[0], positionY - particleDf.position_y.values[0],
            length_includes_head = False,
            head_width=1,
            head_length=1,
            fc='magenta',
            ec='magenta',
            # alpha=0.5,
            zorder=4
        )


    cbar_ax = fig.add_axes([0.9, 0.15, 0.025, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$\\mathbf{u}/u_\\mathrm{max}$')

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels([0.0, 0.5, 1.0])

    return fig, axes

def NSOverview(
        nsDf1, nsDf2, nsDf3,
        lims):
    fig, axes = plt.subplots(1, 3, figsize = (5.25,1.5))

#     fig.suptitle(f"$t = {df.time.values[0]:.2f}$", fontsize=16)
    # fig.suptitle(title, fontsize=16)
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar

    nsDfs = [nsDf1, nsDf2, nsDf3]
    for id in range(3):
        df = nsDfs[id]

        positionX = 0
        positionY = 0

        df = df.query(f'(coordinate_x - {positionX})**2 <= {lims}**2 & (coordinate_y - {positionY})**2 <= {lims}**2')

        x_unique = df['coordinate_x'].unique()
        # Create a meshgrid for plotting
        y_unique = df['coordinate_y'].unique()
        X, Y = np.meshgrid(x_unique, y_unique)

        xmax = x_unique.max()
        xmin = x_unique.min()
        ymax = y_unique.max()
        ymin = y_unique.min()

        # finally plotting
        upperLim = 1e-3 * 2/3 # maximum fluid speed should be 2/3*1e-3
        lowerLim = 0.
        cmap = plt.get_cmap('cividis')
        norm = plt.Normalize(lowerLim, upperLim)

        axes[id].streamplot(X, Y, 
            df.fluidVelocity_x.unstack().values.transpose(),
            df.fluidVelocity_y.unstack().values.transpose(),
            density=0.5, linewidth=0.5, color="black",
        )

        axes[id].pcolormesh(X, Y,
            np.sqrt(df.fluidVelocity_x**2 + df.fluidVelocity_y**2).unstack().values.transpose(),
            vmin=lowerLim,
            vmax=upperLim,
            cmap=cmap, alpha = 0.85
        );

        axes[id].set_xticks([xmin, 0,xmax])
        axes[id].set_xticklabels([f'{xmin:.0f}', 0,f'{xmax:.0f}'])
        axes[id].set_yticks([ymin, 0, ymax])
        axes[id].set_yticklabels([f'{ymin:.0f}', 0,f'{ymax:.0f}'])

        if id == 0:
            axes[id].set_ylabel("$y ~ (\\mathrm{\\mu m})$")
        else:
            axes[id].tick_params(labelleft=False)

        if id == 1:
            axes[id].set_xlabel("$x ~ (\\mathrm{\\mu m})$")

        squirmerRadius = 4;

        # Create a mask as a filled polygon (circle patch with alpha for masking)
        myColor='#F7F7F7'
        mask = Circle((positionX, positionY), squirmerRadius, transform=axes[id].transData, color=myColor, linestyle='', alpha=1, zorder=2)
        axes[id].add_patch(mask)

        axes[id].arrow(
            # particleDf.position_x.values[0], particleDf.position_y.values[0],
            -2, 0,
            2, 0,
            length_includes_head = False,
            head_width=1,
            head_length=1,
            fc='magenta',
            ec='magenta',
            # alpha=0.5,
            zorder=4
        )

    cbar_ax = fig.add_axes([0.9, 0.15, 0.025, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$\\mathbf{u}/u_\\mathrm{max}$')

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels([0.0, 0.5, 1.0])

    return fig, axes

def plotTrjs(particleDf1, particleDf2, particleDf3, targetTime = -1):
    fig, axes = plt.subplots(1, 3, figsize = (5.25,1.5))
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar

    particleDfs = [particleDf1, particleDf2, particleDf3]

    Bs = [3.099114022039876e-5, 0.0001000125888171962, 3.095684660447413e-5]

    for id in range(3):
        particleDf = particleDfs[id]
        B = Bs[id]

        totalTime = particleDf.time.values[-1]

        if targetTime == -1:
            targetTime = totalTime

        targetDistance = np.round(totalTime * 2/3 * B, decimals=1)

        particleDf = particleDf.query(f"time<={targetTime}")
        particleTime = particleDf.time.values

        nsDisplacement = particleTime*2/3*B

        def myTerribleDivide(a,b):
            if (a != 0) & (b != 0):
                return a/b
            elif (a == 0) | (b == 0):
                return 0


        # axes[id].plot(particleTime, particleDf.position_x.values, label = "\\texttt{LBMengine.jl}")
        # axes[id].plot(particleTime, particleTime*2/3*B, label = "NS solution")
        # axes[id].plot(particleTime, particleDf.position_y.values, label = "$y$")
        axes[id].plot(particleTime, particleDf.position_x.values-nsDisplacement)

        axes[id].set_xlim([0, totalTime])
        axes[id].set_xticks([0, totalTime])
        axes[id].set_xticklabels([0, f'{totalTime/1000:.0f}'])
        axes[id].set_ylim([-2/1000, 3/100])
        axes[id].set_yticks([0, 3/100])
        axes[id].set_yticklabels(["0", "$3 \\times 10^{-2}$"])


        if id == 0:
            axes[id].set_ylabel("$x_{\\mathtt{LBM}} - x_\\mathrm{NS} ~ (\\mu \\mathrm{m})$")
        else:
            axes[id].tick_params(labelleft=False)

        if id == 1:
            axes[id].set_xlabel("$t ~ (\\mathrm{ms})$")

        # if id == 2:
        #     axes[id].legend(loc='lower right')

    return fig, axes

def plotVels(particleDf1, particleDf2, particleDf3, targetTime = -1):
    fig, axes = plt.subplots(1, 3, figsize = (5.25,1.5))
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar

    particleDfs = [particleDf1, particleDf2, particleDf3]

    Bs = [0.000030991140220398757, 0.0001000125888171962, 0.000030956846604474135]

    for id in range(3):
        particleDf = particleDfs[id]
        B = Bs[id]


        totalTime = particleDf.time.values[-1]

        if targetTime == -1:
            targetTime = totalTime

        particleDf = particleDf.query(f"time<={targetTime}")
        particleTime = particleDf.time.values

        axes[id].plot(particleTime, np.sqrt(particleDf.velocity_x**2 + particleDf.velocity_y**2 + particleDf.velocity_z**2).values)
        axes[id].axhline(2/3*B, color = "black", alpha = 0.5, linewidth=1, linestyle='dashed', zorder = 1)
        # axes[id].plot(particleTime, particleDf.position_y.values, label = "$y$")

        axes[id].set_xlim([0, totalTime])
        axes[id].set_xticks([0, totalTime])
        axes[id].set_xticklabels([0, 2])
        axes[id].set_ylim([0, 2/3*B * 1.1])
        axes[id].set_yticks([0, B/3, 2/3*B])
        axes[id].set_yticklabels([0, 0.5, 1])

        if id == 0:
            axes[id].set_ylabel("$v/v_\\mathrm{NS}$")
        else:
            axes[id].tick_params(labelleft=False)

        if id == 1:
            axes[id].set_xlabel("$t ~ (\\mathrm{ms})$")

        # if id == 2:
            # axes[id].legend(loc='upper center')

    return fig, axes
