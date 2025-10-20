#= this script is intended to be run using:
    julia main.jl > out.out 2>&1 &
=#
#= ==========================================================================================
=============================================================================================
preamble
=============================================================================================
========================================================================================== =#

# directories and paths
cd(@__DIR__); srcPath = pwd() # params.jl will be read here
cd(".."); outPath = pwd() # data output directory will be created here
cd(".."); envPath = pwd() # the environment is here
cd(srcPath) # the simulation must be run here

# Environment
using Pkg; Pkg.activate(envPath)

# packages
using LBMengine

# parameters
include("$srcPath/params.jl")

#= ==========================================================================================
=============================================================================================
main
=============================================================================================
========================================================================================== =#

println("initializing model..."); flush(stdout);
model = modelInit(;
    xlims = xlims,
    ylims = ylims,
    viscosity = viscosity,
    relaxationTimeRatio = relaxationTimeRatio,
    walledDimensions = walledDimensions,
    forceDensity = forceDensity,
    saveData = true
);

println("running simulation..."); flush(stdout);
@time LBMpropagate!(model; verbose = true, simulationTime = simulationTime, ticksSaved = ticksSaved);

println("plotting the mass density and fluid velocity..."); flush(stdout);
plotMassDensity(model); plotFluidVelocity(model);

println("moving data..."); flush(stdout);
mv("$srcPath/output.lbm", "$outPath/data.lbm")
