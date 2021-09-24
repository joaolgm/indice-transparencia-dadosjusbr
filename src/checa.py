import pandas as pd


def validez(valor):
    if valor == 0 or pd.isna(valor):
        return False
    else:
        return True
