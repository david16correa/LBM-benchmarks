#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xmax = 100 # μm
x = range(-xmax, stop = xmax, step = 0.1);
walledDimensions = [1,2];

# fluid
# water viscosity ≡ μ = 0.890 mPa s, water density ≡ ρ = 1000 kg/m³ → water kinematic shear viscosity ≡ ν ≡ μ/ρ = 0.890 (mm)²/(s),
viscosity = 0.890 # (μm)²/(μs)
isFluidCompressible = false;

# stokeslet
radius = 0.1; # μm
position = [0., 0];
force = [1e-3, 0.]; # mass density units * μm/μs²
# a cylindrically normalized gaussian is used to approximate a Dirac delta
stokeslet = [force * exp(-(i^2+j^2)/(2*radius^2))/(2*pi*radius^2) for i in x, j in x]; # mass density units * μm/μs²

# simulation
simulationTime = 1e3; # μs
ticksBetweenSaves = 10 |> snapshots -> simulationTime / step(x) / snapshots |> round |> Int64; # (about) 500 snapshots are saved
