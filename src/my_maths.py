# Error propagation functions
import numpy as np

quiet_nan = True

def divide(a,b):
    if b == 0.0 and quiet_nan:
        return 1.0

    return a/b

def division_w_err(a,b, da = None, db = None):
    if b == 0.0 and quiet_nan:
        return 1.0, 0.0
    
    res = a/b

    err = pow(da/b,2) + pow(db*a/b/b,2)
    err = np.sqrt(err)

    return res, err
