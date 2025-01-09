# dependencies
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
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

def plotFig(df):
    df = df.query('coordinate_y <= 10 & coordinate_y >= -10')
    # figure preparation
    fig, axes = plt.subplots(figsize = (11,5.5))
    fig.subplots_adjust(right=0.875)  # Adjust the right space to make room for the colorbar
    fig.suptitle(f"$t = {df.time.values[0]:.0f}$", fontsize=16)

    # Create a meshgrid for plotting
    x_unique = df['coordinate_x'].unique()
    y_unique = df['coordinate_y'].unique()
    X, Y = np.meshgrid(x_unique, y_unique)

    # first plot
    upperLim = 0.01
    lowerLim = 0.
    cmap = plt.get_cmap('cividis')
    norm = plt.Normalize(lowerLim, upperLim)

    axes.pcolormesh(X, Y,
        np.sqrt(df.fluidVelocity_x**2 + df.fluidVelocity_y**2).unstack().values.transpose(),
        vmin=lowerLim,
        vmax=upperLim,
        cmap=cmap, alpha = 0.85
    );
    axes.set_xticks([-20, 0, 20])
    axes.set_xlabel("$x ~ (\\mu \\mathrm{m})$")
    axes.set_yticks([-10, 0, 10])
    axes.set_ylabel("$y ~ (\\mu \\mathrm{m})$")
    
    # Create a mask for the quiver plot
    maskStep = int(len(x_unique)/20)
    mask = (df['coordinate_x'].isin(x_unique[::maskStep])) & (df['coordinate_y'].isin(y_unique[::maskStep])) & (
        (df.fluidVelocity_x**2 + df.fluidVelocity_y**2 > 1e-16)
    )
    # Filter the DataFrame
    filtered_df = df[mask]
    
    axes.quiver(
        filtered_df['coordinate_x'], 
        filtered_df['coordinate_y'], 
        (filtered_df.fluidVelocity_x / np.sqrt(filtered_df.fluidVelocity_x**2 + filtered_df.fluidVelocity_y**2)),
        (filtered_df.fluidVelocity_y / np.sqrt(filtered_df.fluidVelocity_x**2 + filtered_df.fluidVelocity_y**2)),
        scale = 30,
    )
    
    # axes.axvline(-10, color = "#CA3D34", alpha = 1, linewidth=3, linestyle='dashed')

    cbar_ax = fig.add_axes([0.9, 0.15, 0.025, 0.7])  # [left, bottom, width, height] for the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, alpha=0.85)
    cbar.set_label(label='$\\mathbf{u}/u_s$')

    custom_ticks = np.array([lowerLim, upperLim/2, upperLim])
    cbar.set_ticks(custom_ticks)
    cbar.set_ticklabels(['$0.0$','$0.5$','$1.0$'])
    
    return fig, axes
