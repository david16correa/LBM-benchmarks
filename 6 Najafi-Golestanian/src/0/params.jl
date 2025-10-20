#= ==========================================================================================
=============================================================================================
params
=============================================================================================
========================================================================================== =#

# space
xlims = (-100,100); # μm
ylims = (-25,25); # μm
dims = 2;

# fluid
viscosity = 2; # (μm)²/(μs)
relaxationTimeRatio = 30.5

# beads
radius = 3; # μm
coupleForces = true;
coupleTorques = false;

# moving arms
bondPairs = [(1,2), (2,3)]

D = 10 * radius # μm
epsilon = 3 * radius # μm
W = 1e-2 # μm/μs

function d1(time; D = D, epsilon = epsilon, W = W)
    alpha = (D-epsilon)/W
    t = time / (alpha)
    t = t%4
    if t < 1
        return D
    elseif t < 2
        t -= 1
        return D - t * (D-epsilon)
    elseif t < 3
        return epsilon
    else
        t -= 3
        return epsilon + t * (D-epsilon)
    end
end

function d2(time; D = D, epsilon = epsilon, W = W)
    alpha = (D-epsilon)/W
    t = time / (alpha)
    t = t%4
    if t < 1
        return D - t * (D-epsilon)
    elseif t < 2
        return epsilon
    elseif t < 3
        t -= 2
        return epsilon + t * (D-epsilon)
    else
        return D
    end
end

equilibriumDisplacements = [t -> d1(t), t -> d2(t)]

# initial positions
xs = [equilibriumDisplacements[1](0); 0; -equilibriumDisplacements[2](0)] # μm
ys = [0 0 0] # μm

# simulation
simulationTime = 42e3; # μs
ticksSaved = 100;
