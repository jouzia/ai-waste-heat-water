"""Break-even and Pareto analysis primitives."""
from __future__ import annotations
import numpy as np

def break_even_linear(x: np.ndarray, y: np.ndarray) -> float | None:
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float)
    if x.size != y.size or x.size < 2: raise ValueError("x and y must have equal length >= 2")
    order=np.argsort(x); x=x[order]; y=y[order]
    for i in range(len(x)-1):
        if y[i] == 0: return float(x[i])
        if y[i]*y[i+1] < 0: return float(x[i] - y[i]*(x[i+1]-x[i])/(y[i+1]-y[i]))
    return None

def pareto_mask(values: np.ndarray, *, minimize: tuple[bool,...]) -> np.ndarray:
    a=np.asarray(values,dtype=float)
    if a.ndim != 2 or a.shape[1] != len(minimize): raise ValueError("values must be 2-D and match minimize")
    z=a.copy()
    for j,is_min in enumerate(minimize):
        if not is_min: z[:,j]*=-1
    mask=np.ones(len(a),dtype=bool)
    for i in range(len(a)):
        if not mask[i]: continue
        dominates=np.all(z <= z[i],axis=1) & np.any(z < z[i],axis=1); dominates[i]=False
        mask[dominates]=False
    return mask