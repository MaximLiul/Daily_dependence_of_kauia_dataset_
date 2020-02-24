import pandas as pd
import math
import numpy as np


df = pd.read_csv('kauia_dataset_excluded_extras.csv')

def activity_periods_of_the_day(data_frame, column_for_analysis, date_column, quantity_column,
                                transaction_column, number_of_hours_in_interval, product_or_user = 'user', list_of_excluded_hours = [],
                                select_product_or_user = False):
                                                                    # excluded_hours is a list of hours (from 0 to 23) which are excluded from the consideration
                                                                    # product_or_user == 'user' counts visits; product_or_user == 'product' counts quantity
    df = data_frame
    # convert data string to hours (int)
    df[date_column] = pd.to_datetime(df[date_column])
    df[date_column] = df[date_column].dt.hour

    # exclusion of hours, chosen in list_of_excluded_hours
    df_selected = df.loc[~(df[date_column].isin(list_of_excluded_hours))].copy()

    # create an array of considered hours
    list_of_considered_hours = df_selected[date_column].unique()
    list_of_considered_hours.sort()
    # append an extra element to the end of array in order not to have problems with names of columns
    list_of_considered_hours = np.append(list_of_considered_hours, list_of_considered_hours[len(list_of_considered_hours) - 1] + 1)

    # calculation of amount of hours within time interval; we round it to the bigger side in order to cover all considered time

    # creation of 'Time Interval' column and full filling it by the strings what correspond to the interval what is suitable for a considered product_or_user
    min_hour_value_in_interval = 0
    while min_hour_value_in_interval < list_of_considered_hours[len(list_of_considered_hours) - 2]:
           # we use min() function in order to prevent the situation when index will exceed an array's length
            df_selected.loc[(df_selected[date_column] >= list_of_considered_hours[
                min_hour_value_in_interval]) & (df_selected[date_column] <= list_of_considered_hours[
                 min(min_hour_value_in_interval +  number_of_hours_in_interval - 1, len(list_of_considered_hours) - 1)]), 'Time Interval'] = \
                        '{}-{}'.format(list_of_considered_hours[min_hour_value_in_interval],
                            list_of_considered_hours[min(min_hour_value_in_interval + number_of_hours_in_interval, len(list_of_considered_hours) - 1)])
            print(df_selected['Time Interval'].unique())
            min_hour_value_in_interval+= number_of_hours_in_interval




   # creation of a df, where indexes are product_or_user and colums are time intervals
    if product_or_user == 'product':
        df_grouped_by_column_for_analysis_time_interval = df_selected.groupby([column_for_analysis, 'Time Interval'])[quantity_column].sum().unstack().fillna(0)
    elif product_or_user == 'user':
        # here  [quantity_column].count() is just a dummy; without it we can not use a grouped df on the next step.
        # on my home computer [transaction_column].count() made an error "cannot insert Transaction ID, already exists"
        df_grouped_by_column_for_analysis_time_interval_transaction = df_selected.groupby([column_for_analysis, transaction_column, 'Time Interval']
                                                                                          ,as_index=False)[quantity_column].count()
        #counting the number of visits for each user in a considered time interval
        df_grouped_by_column_for_analysis_time_interval = df_grouped_by_column_for_analysis_time_interval_transaction.groupby(
                                                                [column_for_analysis, 'Time Interval'])[transaction_column].count().unstack().fillna(0)
    else:
        print('product_or_user value is not correct')

    df_grouped_by_column_for_analysis_time_interval['Total'] = df_grouped_by_column_for_analysis_time_interval.sum(axis=1)

    # normalization: create a list of intervals (columns of a df_grouped_by_column_for_analysis_time_interval)
     # and iterate over them, dividing on a total amount of visits/quantities
    list_of_intervals = df_selected['Time Interval'].unique()
    for interval in list_of_intervals:
        df_grouped_by_column_for_analysis_time_interval[interval] = \
            df_grouped_by_column_for_analysis_time_interval[interval]/df_grouped_by_column_for_analysis_time_interval['Total']

    if select_product_or_user == False:
        return df_grouped_by_column_for_analysis_time_interval.sort_values('Total', ascending=False).to_csv(
                            'activity_periods_of_the_day_{}_number_of_hours_{}_select_{}.csv'.format(
                                product_or_user, number_of_hours_in_interval, select_product_or_user))
    else:
        return df_grouped_by_column_for_analysis_time_interval.loc[
            df_grouped_by_column_for_analysis_time_interval.index == select_product_or_user].to_csv(
                'activity_periods_of_the_day_{}_number_of_hours_{}_select_{}.csv'.format(
                    product_or_user, number_of_hours_in_interval, select_product_or_user))

activity_periods_of_the_day(df, 'Member ID', 'Transaction Date', 'Product Quantity',
                                'Transaction ID', 1, product_or_user = 'user', list_of_excluded_hours = [0,1,18,19,20,21,22,23],
                                select_product_or_user = False)