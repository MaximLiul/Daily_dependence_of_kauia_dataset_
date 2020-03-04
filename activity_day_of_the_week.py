import pandas as pd
import math

df = pd.read_csv('kauia_dataset_excluded_extras.csv')

def activity_day_of_the_week(data_frame, date_column,
                            transaction_column, # if there is no a transaction column in the data_frame then put transaction_column = 'index'
                            column_for_analysis_name,
                            product_column='StockCode', user_column='CustomerID',
                            quantity_column='Quantity',
                            is_normalized=True,
                            select_certain_id=None,
                            output_file=None):  # for users_column the method counts visits; for product_column it counts quantity

   list_of_selected_columns = [column_for_analysis_name, date_column, transaction_column,
                               quantity_column]
   df = data_frame[list_of_selected_columns].copy()

   # convert data string to day of the week
   df[date_column] = pd.to_datetime(df[date_column])
   df[date_column] = df[date_column].dt.day_name()

#if there is no a transaction column in the data_frame then we create it and assign an index value to the transaction column
   if transaction_column == 'index':
        df[transaction_column] = df.index


   if column_for_analysis_name == product_column:
       df_grouped_by_column_for_analysis_time_interval = df.groupby([column_for_analysis_name, date_column])[
           quantity_column].sum().unstack().fillna(0).reset_index()
   elif column_for_analysis_name == user_column:

       df_grouped_by_column_for_analysis_time_interval_transaction = df.groupby(
           [column_for_analysis_name, transaction_column, date_column], as_index=False).count()

       # counting the number of visits for each user for a considered day of the week
       df_grouped_by_column_for_analysis_time_interval = \
           df_grouped_by_column_for_analysis_time_interval_transaction.groupby(
               [column_for_analysis_name, date_column])[transaction_column].count().unstack().fillna(0).reset_index()
   else:
       return print('column_for_analysis_name value is not correct')

   days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

   df_grouped_by_column_for_analysis_time_interval['Total'] = df_grouped_by_column_for_analysis_time_interval[days_list].sum(
       axis=1)
   # reordering of the columns
   columns = [column_for_analysis_name, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
              'Total']
   df_grouped_by_column_for_analysis_time_interval = df_grouped_by_column_for_analysis_time_interval[columns]

   # normalization: create a list of days of the week (columns of a df_grouped_by_column_for_analysis_time_interval) and
   # iterate over them, dividing on a total amount of visits/quantities
   if is_normalized:

       for day in days_list:
           df_grouped_by_column_for_analysis_time_interval[day] = df_grouped_by_column_for_analysis_time_interval[
                                                                      day] / \
                                                                  df_grouped_by_column_for_analysis_time_interval[
                                                                      'Total']

   if output_file is not None:
       if select_certain_id is None:
           return df_grouped_by_column_for_analysis_time_interval.sort_values('Total',
                                                                              ascending=False).to_csv('{}.csv'.format(output_file), index = False)
       else:
           return df_grouped_by_column_for_analysis_time_interval.loc[
               df_grouped_by_column_for_analysis_time_interval.index == select_certain_id].to_csv('{}.csv'.format(output_file), index = False)
   else:
       if select_certain_id is None:
           return df_grouped_by_column_for_analysis_time_interval
       else:
           return df_grouped_by_column_for_analysis_time_interval.loc[
               df_grouped_by_column_for_analysis_time_interval.index == select_certain_id]




activity_day_of_the_week(df, 'Transaction Date',
                            'Transaction ID', # if there is no a transaction column in the data_frame then put transaction_column = 'index'
                            'Member ID',
                            'Product Name', 'Member ID',
                            'Product Quantity',
                            is_normalized=True,
                            select_certain_id=None,
                            output_file='check_check_product_name2')