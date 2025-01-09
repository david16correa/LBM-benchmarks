#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xmax = 20 # μm
x = range(-xmax, stop = xmax, step = 0.1); # μm

# fluid
# water viscosity ≡ μ = 0.890 mPa s, water density ≡ ρ = 1000 kg/m³ → water kinematic shear viscosity ≡ ν ≡ μ/ρ = 0.890 (mm)²/(s),
viscosity = 0.890 # (μm)²/(μs)
isFluidCompressible = true;

# particle
massDensity = 1.; # mass density units
radius = 4.; # μm
position = [0., 0]; # μm
coupleTorques = false;
coupleForces = true;
angularVelocity = 1e-3; # μs⁻¹

# simulation
simulationTime = 1e3; # μs
ticksBetweenSaves = 100 |> snapshots -> simulationTime / step(x) / snapshots |> round |> Int64; # (about) 100 snapshots are saved
