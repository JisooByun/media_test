from pyculiarity import detect_ts
from pyculiarity.date_utils import date_format
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
# %matplotlib inline
# def plot_ts(inDF, y,  savepath ):
#     fig = plt.figure(figsize = (22,12))
#
#     plt.plot(inDF.index, inDF[y], alpha = 0.4, label = y)
#     plt.legend(); plt.xlabel('time');plt.ylabel(y)
# #     plt.savefig(savepath, dpi = 300); plt.close()
#
# def plot_ts_anoms(inDF, savepath):
#     fig = plt.figure(figsize = (22,12))
#     plt.plot(inDF.index, inDF['value'], alpha=0.4, label ='value')
#     plt.plot(inDF.index, inDF['anoms'],  color='steelblue', alpha=0.4, marker='o', markersize='7',
#                 markeredgewidth = 1, markerfacecolor='None', markeredgecolor='red',label='anomalies')
#     if 'expected_value' in inDF.columns:
#         plt.plot(inDF.index, inDF['expected_value'], color = 'c', marker = '^', markersize = '7',
#                  markeredgewidth = 1, markerfacecolor='None', markeredgecolor='c',label='expected_value')
#
#     plt.legend(); plt.xlabel('time');plt.ylabel('value')
#     plt.savefig(savepath, dpi = 300); plt.close()
def make_df(index):

    conn_string = "host='localhost' dbname='media' user='media' password='123123'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    cur.execute("select * from media limit %s;" %(index+50620))
    timeS_DF = pd.DataFrame(cur.fetchall())
    timeS_DF.columns=['timestamp','value']
    print(timeS_DF)
    # n_file = 'kt_test_data'
    # timeS_DF = pd.read_csv('./%s.csv'% n_file, usecols = ['timestamp', 'value'])

    """ detect_ts grouped by only_last / longterm / resample_period """
    results = detect_ts(timeS_DF, max_anoms=0.01, direction='both', only_last= None)
    # results = detect_ts(timeS_DF, max_anoms=0.02, direction='both', only_last= None) #default
    # results = detect_ts(timeS_DF, max_anoms=0.02, direction='pos', only_last= None) #default
    # results = detect_ts(timeS_DF, max_anoms=0.02, direction='both', e_value=True,  only_last= None) # expected value enabled
    # resample_period='H'
    """ Plotting """
    # reformat the index and columns
    timeS_DF = timeS_DF.set_index('timestamp')

    anomsDF = results['anoms']
    anomsDF.drop(['timestamp'], axis = 1, inplace = True)
    anomsDF['is_anom'] = "point { size: 10; shape-type: circle; fill-color: #a52714; }"
    # anomsDF.columns = ['anom_value','is_anom']
    global merged_DF
    merged_DF = pd.merge(left = timeS_DF, right= anomsDF, left_index=True, right_index=True, how = 'left')
    # merged_DF.drop('anom_value',axis = 1,inplace=True)
    print(anomsDF)
    # print(merged_DF)

    # plot_ts(timeS_DF, 'value', './figures/orig_%s.png' % n_file ) # original data
    # plot_ts_anoms(merged_DF,'./void') # anoms marked
# two_weeks(0)

def choose_two(index):
    two_weeks_DF = merged_DF.iloc[48604+index:]
    print(two_weeks_DF)
    json_df = two_weeks_DF.to_json(orient='table')
    return json_df

# make_df(0)
