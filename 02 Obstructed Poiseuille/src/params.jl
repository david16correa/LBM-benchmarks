#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xmax = 20 # mm
x = range(-xmax, stop = xmax, step = 0.1);

# fluid
# water viscosity ≡ μ = 0.890 mPa s, water density ≡ ρ = 1000 kg/m³ → water kinematic shear viscosity ≡ ν ≡ μ/ρ = 0.890 (mm)²/(s),
viscosity = 0.890 # (mm)²/(s)
isFluidCompressible = false;

# wall
h = 10; # half width of channel, mm
solidNodes = [j > h || j < -h for i in x, j in x];

# pressure gradient
forceDensity = [1e-4, 0.0] # water density units * mm/s²

# particle
radius = 1.0; # mm
position = [-5, 0.]; # mm
coupleTorques = false;
coupleForces = false;
scheme = :ladd;

# simulation
simulationTime = 1e3; # s
ticksBetweenSaves = 100 |> snapshots -> simulationTime / step(x) / snapshots |> round |> Int64; # (about) 100 snapshots are saved
