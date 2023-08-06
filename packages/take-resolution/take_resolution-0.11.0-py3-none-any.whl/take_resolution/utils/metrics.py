__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import numpy as np
import pandas as pd

DF = pd.DataFrame


def weighted_mean(df: DF, values_column: str, weight_column: str) -> float:
    """Takes weighted mean on `values_column` by `weighted_column`.
    
    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :param values_column: Column to take weighted mean.
    :type values_column: ``str``
    :param weight_column: Column with weight.
    :type weight_column: ``str``
    :return: Weighted mean.
    :rtype: ``float``
    """
    # noinspection PyUnresolvedReferences
    return np.vdot(df[values_column], df[weight_column]) / df[weight_column].sum()
