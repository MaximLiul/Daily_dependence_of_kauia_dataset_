import pandas as pd
import math


df = pd.read_csv('kauia_dataset_excluded_extras.csv')

def activity_day_of_the_week(data_frame, column_for_analysis, date_column, quantity_column,
                                transaction_column, product_or_user = 'user', # product_or_user == 'user' counts visits; product_or_user == 'product' counts quantity
                                select_product_or_user = False):
    df = data_frame
    # convert data string to hours (int)
    df[date_column] = pd.to_datetime(df[date_column])
    df[date_column] = df[date_column].dt.day_name()

    if product_or_user == 'product':
        df_grouped_by_column_for_analysis_time_interval = df.groupby([column_for_analysis, date_column])[quantity_column].sum().unstack().fillna(0)
    elif product_or_user == 'user':
        # here  [quantity_column].count() is just a dummy; without it we can not use a grouped df on the next step.
        # on my home computer [transaction_column].count() made an error "cannot insert Transaction ID, already exists"
        df_grouped_by_column_for_analysis_time_interval_transaction = df.groupby(
                                [column_for_analysis, transaction_column, date_column],as_index=False)[quantity_column].count()

        # counting the number of visits for each user for a considered day of the week
        df_grouped_by_column_for_analysis_time_interval = df_grouped_by_column_for_analysis_time_interval_transaction.groupby(
                                                                [column_for_analysis, date_column])[transaction_column].count().unstack().fillna(0)
    else:
        print('product_or_user value is not correct')

    df_grouped_by_column_for_analysis_time_interval['Total'] = df_grouped_by_column_for_analysis_time_interval.sum(axis=1)

    columns = ['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday','Sunday', 'Total']
    df_grouped_by_column_for_analysis_time_interval = df_grouped_by_column_for_analysis_time_interval[columns]

    # normalization: create a list of days of the week (columns of a df_grouped_by_column_for_analysis_time_interval) and
    # iterate over them, dividing on a total amount of visits/quantities
    days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days_list:
        df_grouped_by_column_for_analysis_time_interval[day] = df_grouped_by_column_for_analysis_time_interval[day] / df_grouped_by_column_for_analysis_time_interval['Total']


    if select_product_or_user == False:
        return df_grouped_by_column_for_analysis_time_interval.sort_values('Total',
                                        ascending=False).to_csv('activity_periods_day_of_the_week_{}_select_{}.csv'.format(product_or_user, select_product_or_user))
    else:
        return df_grouped_by_column_for_analysis_time_interval.loc[
                     df_grouped_by_column_for_analysis_time_interval.index == select_product_or_user].to_csv(
                            'activity_periods_day_of_the_week_{}_select_{}.csv'.format(product_or_user, select_product_or_user))

activity_day_of_the_week(df, 'Product Name', 'Transaction Date', 'Product Quantity',
                                'Transaction ID', product_or_user = 'product',
                                                select_product_or_user = False)
