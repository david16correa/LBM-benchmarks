#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xmax = 20 # μm
x = range(-xmax, stop = xmax, step = 0.1);

# fluid
# water viscosity ≡ μ = 0.890 mPa s, water density ≡ ρ = 1000 kg/m³ → water kinematic shear viscosity ≡ ν ≡ μ/ρ = 0.890 (μm)²/(μs),
viscosity = 0.890 # (μm)²/(μs)
isFluidCompressible = false;

# wall
h = 10; # half width of channel, μm
solidNodes = [j > h || j < -h for i in x, j in x];

# pressure gradient
forceDensity = [1e-4, 0.0] # water density units * μm/μs²

# simulation
simulationTime = 1e3; # μs
ticksBetweenSaves = 100 |> snapshots -> simulationTime / step(x) / snapshots |> round |> Int64; # (about) 100 snapshots are saved
