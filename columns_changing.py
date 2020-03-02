import pandas as pd


df = pd.read_csv('activity_periods_of_the_day_user_number_of_hours_1_select_False.csv')

columns = ['Member ID', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', 'Total']

df = df[columns]

df.to_csv('activity_periods_of_the_day_user_number_of_hours_1_sorted_columns.csv', index = False)