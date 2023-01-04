import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns

class Fit():
    def r_t(s, r_s, l_t, N, W, L):
        return (r_s * s / (N * W + (N-1) * (2 *s + L))) + (2 * r_s * l_t / (N * W + (N-1) * (2 *s + L)))
    gmodel5 = Model(r_t)
    param5 = gmodel5.make_params()
    param5['r_s'].set(value = 1e8, min = 0)
    param5['l_t'].set(value = 1e-5, min = 1e-9)
    param5['L'].set(value = 3200e-4, vary = False)
    param5['W'].set(value = 5e-4, vary = False)
    param5['N'].set(value = 60, vary = False)
