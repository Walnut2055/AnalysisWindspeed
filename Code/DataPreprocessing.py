import os
import pandas as pd
from Module.Config import HOME_PATH, YEAR, WD_LIST
from Module.Utile import makefolder

# Path setting #
DATA_PATH = HOME_PATH + "Data/RawData/"
RESULT_PATH = HOME_PATH + "Data/WSData/"
makefolder(RESULT_PATH)

#
# Analysis wind speed of AWS data
#
# Append year data #
TOTAL_ASOS = pd.DataFrame([])
for y in YEAR:
    # Data load #
    ASOS_df = pd.read_csv(DATA_PATH + "{}_ASOS.txt".format(y), delimiter="\t", engine='python')

    # Need column #
    ASOS_df = ASOS_df[['지점', '지점명', '일시', '풍속(m/s)', '풍향(16방위)', '풍속 QC플래그']]

    # Append data #
    TOTAL_ASOS = pd.concat([TOTAL_ASOS, ASOS_df], axis=0).reset_index(drop=True)

#
# If flag exist in the data, this work is deleting flag data #
#
y_list, m_list, d_list, new_date = [], [], [], []
for d in TOTAL_ASOS['일시'].tolist():
    y_list.append(int(d[0:4]))
    m_list.append(int(d[5:7]))
    d_list.append(int(d[8:10]))
    new_date.append('{}{}{}'.format(d[0:4], d[5:7], d[8:10]))
TOTAL_ASOS['year'], TOTAL_ASOS['month'], TOTAL_ASOS['day'], TOTAL_ASOS['date'] = y_list, m_list, d_list, new_date

# Unnecessary column delete #
USE_df = TOTAL_ASOS.drop(columns=['일시']).copy()

# Separate of WS in the 16-directions #
ii = 1
for wd in WD_LIST:
    if wd == 'ZERO':
        USE_df.loc[(USE_df['풍속(m/s)'] < 0.5), 'WD_CLASS'] = 'ZERO'
    elif wd == 'N':
        USE_df.loc[(USE_df['풍속(m/s)'] >= 0.5) & (USE_df['풍향(16방위)'] >= 0) & (USE_df['풍향(16방위)'] <= 11.25), 'WD_CLASS'] = 'N'
        USE_df.loc[(USE_df['풍속(m/s)'] >= 0.5) & (USE_df['풍향(16방위)'] > 11.25 * 31) & (USE_df['풍향(16방위)'] <= 11.25 * 32), 'WD_CLASS'] = 'N'
    else:
        USE_df.loc[(USE_df['풍속(m/s)'] >= 0.5) & (USE_df['풍향(16방위)'] > 11.25*ii) & (USE_df['풍향(16방위)'] <= 11.25 * (ii+2)), 'WD_CLASS'] = wd
        print(wd)
        print(ii)
        ii += 2

# Separate of WS in the 4-classes #
USE_df.loc[(USE_df['풍속(m/s)'] < 0.5), 'WS_CLASS'] = 'A'
USE_df.loc[(USE_df['풍속(m/s)'] >= 0.5) & (USE_df['풍속(m/s)'] < 3.4), 'WS_CLASS'] = 'B'
USE_df.loc[(USE_df['풍속(m/s)'] >= 3.4) & (USE_df['풍속(m/s)'] < 8.0), 'WS_CLASS'] = 'C'
USE_df.loc[(USE_df['풍속(m/s)'] >= 8.0), 'WS_CLASS'] = 'D'

# Saved data #
USE_df.to_csv(RESULT_PATH + "WS_DATA_test.txt", sep="\t", index=False)
print("ASOS Data preprocessing finish")