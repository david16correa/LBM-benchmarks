#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xmax = 15 # μm
x = range(-xmax, stop = xmax, step = 0.1);
walledDimensions = [1,2];

# fluid
# water viscosity ≡ μ = 0.890 mPa s, water density ≡ ρ = 1000 kg/m³ → water kinematic shear viscosity ≡ ν ≡ μ/ρ = 0.890 (μm)²/(ms),
viscosity = 0.890 # (μm)²/(μs)
isFluidCompressible = false;

# particle
massDensity = 1.; # water density units
radius = 1.0; # μm
position = [0, 1.5-xmax]; # μm
coupleTorques = false;
coupleForces = false;
angularVelocity = 1e-6; # rad/μs
scheme = :ladd;

# simulation
simulationTime = 1e3; # μs
ticksBetweenSaves = 100 |> snapshots -> simulationTime / step(x) / snapshots |> round |> Int64; # (about) 100 snapshots are saved
