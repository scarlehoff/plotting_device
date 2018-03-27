# Error propagation functions
import numpy as np

quiet_nan = True

def divide(a,b):
    if b == 0.0 and quiet_nan:
        return 1.0

    return a/b

def division_w_err(a_in,b_in, da = 0.0, db = 0.0):
    if isinstance(a_in, (tuple, list)) and len(a_in) == 2:
        a = a_in[0]
        da = a_in[1]
    else:
        a = a_in
    if isinstance(b_in, (tuple, list)) and len(b_in) == 2:
        b = b_in[0]
        db = b_in[1]
    else:
        b = b_in
    
    if b == 0.0 and quiet_nan:
        return 1.0, 0.0

    res = a/b

    err = pow(da/b,2) + pow(db*a/b/b,2)
    err = np.sqrt(err)

    return res, err
