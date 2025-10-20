#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xlims = (-15,15)

# fluid
# water viscosity ≡ μ = 0.890 mPa s, water density ≡ ρ = 1000 kg/m³ → water kinematic shear viscosity ≡ ν ≡ μ/ρ = 0.890 (μm)²/(ms),
viscosity = 0.890 # (μm)²/(μs)

# wall
walledDimensions = [1,2];

# particle
massDensity = 1.; # water density units
radius = 1.0; # μm
position = [0, 1.5-15]; # μm
coupleTorques = false;
coupleForces = false;
angularVelocity = 1e-6; # rad/μs

# simulation
simulationTime = 1e3; # μs
ticksSaved = 100
