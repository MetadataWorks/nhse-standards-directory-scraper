
from decouple import config
import pandas as pd
from email_notification.send_email import send_email_notification
import glob
import os.path
import json
import numpy as np



def get_last_scraped_file():

    max_file = None

    folder_path = r'comparison_files/*.xlsx'
    files = glob.glob(folder_path)

    if files!=[]:
        max_file = max(files, key=os.path.getctime)

    return max_file



def compare_current_data_with_last_scraped_data(current_scraped_data_file, last_scraped_data_file):

    message = 'Hello there!'


    if last_scraped_data_file != None:

        df1 = pd.read_excel(last_scraped_data_file, header=0,  keep_default_na=False)
        df2 = pd.read_excel(current_scraped_data_file, header=0,  keep_default_na=False)
        

        sheet1_titles = df1['Title'].tolist()
        sheet2_titles = df2['Title'].tolist()
        print(len(sheet1_titles), len(sheet2_titles))


        missing_titles = [title for title in sheet1_titles if title not in sheet2_titles]
        print('missing apis in df2: ', missing_titles)

        if missing_titles != []:
            missing = ', '.join(missing_titles)
            message += f'\n\nList of missing APIs: \n{missing}'

        new_titles = [title for title in sheet2_titles if title not in sheet1_titles]
        print('new apis in df2: ', new_titles)

        if new_titles != []:
            new = ', '.join(new_titles)
            message += f'\n\nList of newly added APIs: \n{new}'


        for title in missing_titles:
            df1 = df1.drop(df1[df1['Title']==title].index)
            print(f'dropped this missing api from df1: {title}')

        for title in new_titles:
            df2 = df2.drop(df2[df2['Title']==title].index)
            print(f'dropped this new api from df2: {title}')


        print('###############################################')
        print('df1 shape', df1.shape)
        print('df2 shape', df2.shape)


        print('###############################################')
        print('df1 equals df2 : ', df1.equals(df2))

        # print(df1.values)
        # print(df2.values)


        comparison_values = df1.values == df2.values
        print('###############################################')
        print('comparison_values', comparison_values)


        rows, cols = np.where(comparison_values==False)
        print('changes rows: ', rows)
        print('changes columns: ', cols)


        for item in zip(rows,cols):
            print('row: ', item[0], 'col: ', item[1])
            api_title = df2.iloc[item[0], 1]
            api_attribute = df2.columns[item[1]]    
                
            print(f"A change is detected in API - {api_title} (attribute = {api_attribute})")
            message += f"\n\nA change is detected in API - '{api_title}' (attribute = {api_attribute})"

            print('{} --> {}'.format(df1.iloc[item[0], item[1]], df2.iloc[item[0], item[1]]))


        if message == 'Hello there!':
            print('no changes detected among last and current scraped data')
        
        else:
            try:
                receiver_email_adress = json.loads(config('receiver_email_id'))
                print('receiver_email_adress', receiver_email_adress)
                send_email_notification(receiver_email_adress, message)
                print('Email notification sent')
            
            except Exception as e:
                print(e)
                print('error while sending email notification')



    else:
        print('There is no previous data file to compare this current data with.')



