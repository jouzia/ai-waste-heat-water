"""Deterministic experiment runner."""
import numpy as np
from .engine import simulate
from .models import Scenario


def run_grid(base: Scenario, parameter: str, values: np.ndarray):
    rows=[]
    for value in np.asarray(values,dtype=float):
        data=base.model_dump(mode="python")
        root,field=parameter.split(".",1)
        data[root][field]=float(value)
        result=simulate(Scenario.model_validate(data))
        rows.append(result.model_dump())
    return rows