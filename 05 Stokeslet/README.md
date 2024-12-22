# 05 Stokeslet

Following [Graham (2018)](https://doi.org/10.1017/9781139175876), a stokeslet is the solution to a Stokes flow in an unbounded domain driven by a point force F exerted at the origin:
```math
\nabla \cdot \mathbf{u} = 0, \quad - \nabla p + \eta \nabla^2 \mathbf{u} + \mathbf{F} \delta(\mathbf{x}) = \mathbf{0}.
```

The aim of this experiment is to verify the engine correctly reproduces the analytical solution to the stokeslet.
