using CairoMakie

include("$srcPath/params.jl")
fig, ax, hm = stokeslet |> M -> [sqrt(m[1]^2 + m[2]^2) for m in M] |> M -> heatmap(M[lb:ub,lb:ub]); Colorbar(fig[:, end+1], hm); fig
stokeslet |> M -> [sqrt(m[1]^2 + m[2]^2) for m in M] |> M -> sum(m * step(x)^2 for m in M)



model.fluidVelocity |> M -> [sqrt(m[1]^2 + m[2]^2) for m in M] |> M -> heatmap(M[lb:ub,lb:ub]); Colorbar(fig[:, end+1], hm); fig

fig, ax, hm = model.fluidVelocity |> M -> [sqrt(m[1]^2 + m[2]^2) for m in M] |> M -> heatmap(M); Colorbar(fig[:, end+1], hm); fig

