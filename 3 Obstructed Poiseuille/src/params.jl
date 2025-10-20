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

# wall
walledDimensions = [2]

# obstruction
radius = 1.0; # μm
center = [-5, 0.]; # μm
obstruction = (x,y) -> norm([x,y] - center) < radius

# pressure gradient
forceDensity = [1e-4, 0.0] # water density units * μm/μs²

# simulation
simulationTime = 1e3; # μs
ticksSaved = 100
