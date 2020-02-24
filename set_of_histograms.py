import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('activity_periods_day_of_the_week_user_select_False.csv')

def histogram_builder(data_frame, column_for_analysis, list_of_selected_products_or_users):

    df = data_frame
    list_of_selected_products_or_users = list_of_selected_products_or_users
    if len(list_of_selected_products_or_users) >= 7:
        return print('list_of_selected_products_or_users should contain from 1 to 6 elements')

    fig, ax = plt.subplots(2, 3, sharex='col', sharey='row')

    # subplot_marker defines the iterator over indexes in list_of_selected_products_or_users.
    for subplot_marker in range(len(list_of_selected_products_or_users)):
        if subplot_marker < 3:
            subplot_column_coord = 0
            subplot_row_coord = subplot_marker
        else:
            subplot_column_coord = 1
            subplot_row_coord = subplot_marker - 3

        df_selected = df.loc[df[column_for_analysis] == list_of_selected_products_or_users[subplot_marker]].copy()

        # define barchart parameters
        y_values = df_selected.values[0]
        x_coordinates = df_selected.columns[1:len(df.columns) - 1]
        y_pos = np.arange(len(x_coordinates))
        ax[subplot_column_coord, subplot_row_coord].bar(y_pos, y_values[1:len(df.columns) - 1])
        ax[subplot_column_coord, subplot_row_coord].set_title('{}: {},  quantities/visits: {}'.format(
            column_for_analysis,df_selected[column_for_analysis].values[0], df_selected['Total'].sum()), fontsize=3)
        ax[subplot_column_coord, subplot_row_coord].set_xlabel('Day of the week', fontsize=5)  # Set text for the x axis
        ax[subplot_column_coord, subplot_row_coord].set_ylabel('Portion of quantities/visits',
                                                               fontsize=5)  # Set text for y axis

   

    return plt.savefig('histograms_{}_by_dow_list_of_select[0]_{}.png'.format(
                            column_for_analysis,list_of_selected_products_or_users[0]), dpi=300)


histogram_builder(df, 'Member ID', [28885382471, 28885348770, 28885369714, 28885372741, 28885388545, 28885371425] )

#['Princess', 'Berry Dairy  Lrg', 'Mango Berry Sml', 'Steak Cajun Chicken Wrap', 'MUSH Thai Crunch Salad', 'Steak Protein Pot Salad']
# ['MUSH Cobb Salad', 'Peanut Butter Cup', 'Tropical Chia Lrg', 'Citrus Glo Sml','Peanut Butter Bomb Sml', 'Peanut Butter Bliss Lrg']