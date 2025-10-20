#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xlims = (-20, 20) # μm
ylims = (-10, 10) # μm

# fluid
# water viscosity ≡ μ = 0.890 mPa s, water density ≡ ρ = 1000 kg/m³ → water kinematic shear viscosity ≡ ν ≡ μ/ρ = 0.890 (μm)²/(μs),
viscosity = 0.890 # (μm)²/(μs)
relaxationTimeRatio = 30.5

# wall
walledDimensions = [2]

# pressure gradient
forceDensity = [1e-4, 0.0] # water density units * μm/μs²

# simulation
simulationTime = 1e3; # μs
ticksSaved = 100
