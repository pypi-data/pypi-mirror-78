def l_pdseries_2_l_dfs(l_series, ndfs):
    import pandas as pd
    import numpy as np
    df_number = len (l_series)/int(ndfs)
    required_columns_l = [f"M{i}" for i in range(0, int(df_number))]
    c  = [i for i in range(0, len(l_series)+int(df_number), int(df_number))]
    df_l = []
    col_l = []
    for i in range(1, ndfs+1):
        il = []
        [il.append(col) for col in range(c[i-1], c[i])]
        col_l.append(il)
        df_l.append(pd.DataFrame(np.array([np.array(l_series[j]) for j in col_l[i-1]]).T, columns=required_columns_l).dropna(axis=0))
    return  df_l

