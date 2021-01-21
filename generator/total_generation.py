import pandas as pd
from generator.dataset_generator import user_generator, bills_generator, \
    main_data_generator, accounts_generator, userdata_generator
import random
from datetime import datetime
def generate_data(n):
    """create file with users"""
    user_gen = user_generator(n)
    to_user_file = pd.DataFrame(data=user_gen)
    to_user_file.to_csv('base/data_set/users.csv')

    """create file with user's bills"""
    bill_gen =bills_generator(user_gen['hr_id'])
    to_bill_file = pd.DataFrame(data=bill_gen)
    to_bill_file.to_csv('base/data_set/user_bills.csv')

    """create file with user proxy data"""
    main_gen =main_data_generator(user_gen['hr_id'])
    to_main_file = pd.DataFrame(data=main_gen)
    to_main_file.to_csv('base/data_set/main_users.csv')


    users = pd.read_csv('base/data_set/users.csv')

    """create comp_serv table"""
    result_columns = pd.read_excel('generator/serv.xlsx')
    columns = result_columns.columns
    new_columns = columns.insert(0,'SERV and COMP')
    new_df = pd.DataFrame(columns=new_columns)
    new_columns = new_df.columns
    diapazon = len(new_columns)

    for index, user in users.iterrows():
        user_dict = {}
        user_dict['UID'] = user['hr_id']
        user_dict['Name'] = user['username']
        for col in new_columns[3:diapazon]:
            user_dict[col] = None
        for i in range(random.randint(8,12)):
            serv_x = random.randint(2,diapazon-1)
            for ind in range(3,diapazon):
                column = new_columns[ind]
                if serv_x == ind:
                    user_dict[column] = random.randint(-200, 200)

        new_df = new_df.append(user_dict, ignore_index=True )

    SERV=[]
    for i, row in new_df.iterrows():
        SERV.append(sum([row[j] for j in new_columns[3:] if row[j] and row[j]<0]))

    COMP=[]
    for i, row in new_df.iterrows():
        COMP.append(sum([row[j] for j in new_columns[3:] if row[j] and row[j]>0]))

    new_df['SERV and COMP'] = list(zip(SERV, COMP))
    new_df.to_csv('base/data_set/services.csv')

    """create FEES table"""
    columns = ['hr_id','SUM','ST HELP Nadezhda Iushkova','ST HELP Valeria Mandrolko',
               'Broken technique','Coach session','Test Gellup +1',
               ]
    diapazon = len(columns)
    df_fees = pd.DataFrame(columns=columns)

    for index, user in users.iterrows():
        user_dict = {}
        for col in columns:
            user_dict[col] = None
        user_dict['hr_id'] = user['hr_id']
        for i in range(random.randint(1, 6)):
            serv_x = random.randint(2,diapazon-1)
            for ind in range(2,diapazon):
                column = columns[ind]
                if serv_x == ind:
                    user_dict[column] = random.randint(-200, -10)
        df_fees = df_fees.append(user_dict, ignore_index=True )
        df_fees['SUM'] = df_fees.iloc[:, 2:diapazon].sum(axis=1)
    df_fees.to_csv('base/data_set/fees.csv')
    df_fees.to_excel('base/data_set/fees.xlsx')



    user_csv = pd.read_csv('base/data_set/users.csv')
    user_main_list = pd.read_csv('base/data_set/main_users.csv')
    user_bill = pd.read_csv('base/data_set/user_bills.csv')
    date_reconciliation = datetime.today()

    """create file with user's accounts"""
    account_gen =accounts_generator(user_csv, user_main_list)
    to_account_file = pd.DataFrame(data=account_gen)
    to_account_file.to_csv('base/data_set/accounts.csv')

    """create file with user's accounts"""
    userdata_gen =userdata_generator(user_csv, user_main_list, user_bill, date_reconciliation)
    to_userdata_file = pd.DataFrame(data=userdata_gen)
    to_userdata_file.to_csv('base/data_set/userdata.csv')

    """______________________create txt with manager id___________________________"""
    import configparser

    config = configparser.ConfigParser()
    config.read("cred/config.ini")

    with open('base/data_set/manager_id.txt','w') as file:
        file.write(config['manager_id']['user_id'])
