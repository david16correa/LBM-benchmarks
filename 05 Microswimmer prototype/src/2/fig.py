# dependencies
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import pandas as pd
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter

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

radius = 4

def plotFig(df, uM, particleDf, id):
    posX = particleDf.position_x.values[id]
    posY = particleDf.position_y.values[id]
    # figure preparation
    fig, axes = plt.subplots(figsize = (8,8))
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar
    fig.suptitle(f"$t = {df.time.values[0]:.0f}$", fontsize=16)
    
    # Create a meshgrid for plotting
    x_unique = df['coordinate_x'].unique()
    y_unique = df['coordinate_y'].unique()
    X, Y = np.meshgrid(x_unique, y_unique)
    
    xmax = x_unique.max()
    xmin = x_unique.min()
    ymax = y_unique.max()
    ymin = y_unique.min()
    
    # first plot
    upperLim = 1
    lowerLim = 0.
    cmap = plt.get_cmap('cividis')
    norm = plt.Normalize(lowerLim, upperLim)

    axes.streamplot(X, Y, 
        df.fluidVelocity_x.unstack().values.transpose(),
        df.fluidVelocity_y.unstack().values.transpose(),
#         density=1.0, linewidth=1, color="black",
        density=1.5, linewidth=1, color="black",
    )
    
    
    axes.pcolormesh(X, Y,
        (np.sqrt(df.fluidVelocity_x**2 + df.fluidVelocity_y**2)/uM).unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap, alpha = 0.85
    );
    axes.set_xticks([xmin, 0, xmax])
    axes.set_xlabel("$x ~ (\\mathrm{\\mu m})$")
    axes.set_yticks([ymin, 0, ymax])
    axes.set_ylabel("$y ~ (\\mathrm{\\mu m})$")
    cbar_ax = fig.add_axes([0.9, 0.15, 0.04, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$\\mathbf{u}/u_\\mathrm{max}$')

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels([f'{tick:.1f}' for tick in custom_ticks])

    # Create a mask as a filled polygon (circle patch with alpha for masking)
    myColor='#F7F7F7'
    mask = Circle((posX, posY), radius, transform=axes.transData, color=myColor, linestyle='', alpha=1, zorder=2)
    axes.add_patch(mask)

    axes.plot(particleDf.position_x.values[:id], particleDf.position_y.values[:id], color='#CA3D34', linewidth=2, zorder=4)  # Trajectory line


    return fig, axes

