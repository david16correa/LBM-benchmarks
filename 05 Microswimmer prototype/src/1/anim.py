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
src_n = os.path.basename(os.getcwd())
dataDir = f'../../data.lbm/{src_n}/'

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

particleDf = pd.read_csv(dataDir+"particlesTrj.csv")

id=-5
finalFluidDf = pd.read_csv(dataDir + f"fluidTrj_{ticks[id]}.csv").set_index(["id_x","id_y"]).sort_index()
finalPosX = particleDf.position_x.values[id]
finalPosY = particleDf.position_y.values[id]

radius = 4
auxRadius = radius+0.5
uM = np.sqrt(finalFluidDf.query(f'(coordinate_x - {finalPosX})**2 + (coordinate_y - {finalPosY})**2 > {auxRadius}**2').fluidVelocity_x**2 + finalFluidDf.query(f'(coordinate_x - {finalPosX})**2 + (coordinate_y - {finalPosY})**2 > {auxRadius}**2').fluidVelocity_y**2).max()

# the data is read
for tickId in np.arange(len(ticks)):
    fluidDf = pd.read_csv(dataDir + f"fluidTrj_{ticks[tickId]}.csv").set_index(["id_x","id_y"]).sort_index()
    figure.plotFig(fluidDf, uM, particleDf, tickId)

    plt.savefig(f"{outputDir}/{tickId}.png", format="png", dpi=300, bbox_inches="tight")
    plt.close()

mkAnimSh = f'ffmpeg -framerate 10 -i {outputDir}/%d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -pix_fmt yuv420p anims/output.mp4'
os.system(mkAnimSh)
os.system(f'rm -r {outputDir}')

# ffmpeg -loglevel quiet -framerate 5 -i frames.lbm/%d.png -c:v libx264 -pix_fmt yuv420p anims/output.mp4
