import os
import pandas as pd
from Module.Config import HOME_PATH, YEAR, MONTH, WD_LIST, WS_LIST, AREA
from Module.Utile import makefolder

# Path setting #
DATA_PATH = HOME_PATH + "Data/"
RESULT_PATH = HOME_PATH + "Result/"
makefolder(RESULT_PATH)

#
# Analysis wind speed of AWS data #
#
# Data load #
WS_DATA = pd.read_csv(DATA_PATH + "WS_DATA.txt", delimiter="\t", encoding='utf-8')

for Y in YEAR:
    COL_LIST = ['WS'] + WD_LIST

    for m in MONTH:
        global control_df
        if m == 'All':
            dec_df = WS_DATA.loc[(WS_DATA['year'] == int(Y)) & (WS_DATA['month'] == 12)].reset_index(drop=True).copy()
            jfm_df = WS_DATA.loc[(WS_DATA['year'] == int(Y) + 1) & ((WS_DATA['month'] >= 1) & (WS_DATA['month'] <= 3))].reset_index(drop=True).copy()
            control_df = pd.concat([dec_df, jfm_df], axis=0).reset_index(drop=True)
        if m == 12:
            control_df = WS_DATA.loc[(WS_DATA['year'] == int(Y)) & (WS_DATA['month'] == 12)].reset_index(drop=True).copy()
        if m == 1:
            control_df = WS_DATA.loc[(WS_DATA['year'] == int(Y) + 1) & (WS_DATA['month'] == 1)].reset_index(drop=True).copy()
        if m == 2:
            control_df = WS_DATA.loc[(WS_DATA['year'] == int(Y) + 1) & (WS_DATA['month'] == 2)].reset_index(drop=True).copy()
        if m == 3:
            control_df = WS_DATA.loc[(WS_DATA['year'] == int(Y) + 1) & (WS_DATA['month'] == 3)].reset_index(drop=True).copy()

        st_df = pd.DataFrame([])
        for st in AREA:
            matrix_df = pd.DataFrame([], columns=COL_LIST)
            matrix_df['WS'] = WS_LIST

            for ws in WS_LIST:

                for wd in WD_LIST:
                    matrix = control_df.loc[(control_df['지점명'] == st) & (control_df['WS_CLASS'] == ws) & (control_df['WD_CLASS'] == wd)]
                    matrix_df.loc[(matrix_df['WS'] == ws), '{}'.format(wd)] = len(matrix)

            # Index setting #
            matrix_df = matrix_df.set_index('WS')

            # Columns setting #
            class_sum = matrix_df.sum(axis=1)
            matrix_df['SUM'] = class_sum
            matrix_df['Station'] = st

            # Calculate total sum #
            total_sum = matrix_df['SUM'].sum()

            for col in matrix_df.columns:
                if col == 'Station':
                    pass
                else:
                    try:
                        matrix_df['{}'.format(col)] = (matrix_df['{}'.format(col)] / total_sum) * 100
                        matrix_df['{}'.format(col)] = matrix_df['{}'.format(col)].apply(lambda x: f"{x:.1f}")
                    except ZeroDivisionError as err:
                        print("Error {} {} : {}".format(Y, m, err))
                        break

            # 19개 권역 자료 병합 #
            st_df = pd.concat([st_df, matrix_df], axis=0)

        print("Year : {} // Month : {}".format(Y, m))
        st_df.to_csv(RESULT_PATH + "WDWS_{}_{}.txt".format(Y, m), sep='\t')
