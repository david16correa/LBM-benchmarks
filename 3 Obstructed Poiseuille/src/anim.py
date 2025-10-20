# ==========================================================================================
# ==========================================================================================
# preamble
# ==========================================================================================
# ==========================================================================================

# important stuff
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

# function to plot every frame
import fig

# directory of the data is saved
dataDir = '../data.lbm/'

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
os.mkdir(outputDir)
os.mkdir("anims")

# ==========================================================================================
# ==========================================================================================
# plotting
# ==========================================================================================
# ==========================================================================================


fluidDf = pd.read_csv(dataDir + f"fluidTrj_{ticks[-1]}.csv").set_index(["id_x","id_y"]).sort_index()
uM = np.sqrt(fluidDf.fluidVelocity_x**2 + fluidDf.fluidVelocity_y**2).max()

# the data is read
for tickId in np.arange(len(ticks)):
    fluidDf = pd.read_csv(dataDir + f"fluidTrj_{ticks[tickId]}.csv").set_index(["id_x","id_y"]).sort_index()
    figure.plotFig(fluidDf, uM)

    plt.savefig(f"{outputDir}/{tickId}.png", format="png", dpi=300, bbox_inches="tight")
    plt.close()

mkAnimSh = f'ffmpeg -framerate 10 -i {outputDir}/%d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -pix_fmt yuv420p anims/output.mp4'
os.system(mkAnimSh)
os.system(f'rm -r {outputDir}')

# ffmpeg -loglevel quiet -framerate 5 -i frames.lbm/%d.png -c:v libx264 -pix_fmt yuv420p anims/output.mp4
