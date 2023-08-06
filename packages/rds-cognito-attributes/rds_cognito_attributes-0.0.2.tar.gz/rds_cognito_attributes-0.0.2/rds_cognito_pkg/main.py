import time
import datetime
import csv
import sys
import os

from RDS_Cognito_attribute_alignment.rds_cognito_pkg.models import User
from RDS_Cognito_attribute_alignment.rds_cognito_pkg.functions import get_db_data, connect_to_db
from RDS_Cognito_attribute_alignment.rds_cognito_pkg.settings import RDS_TABLE_COLUMN, COGNITO_ATTRIBUTE, FOLDER_NAME


# This variable will hold your RDS connection object which will be used later in the script.
my_connection = connect_to_db(
    db_user='app',
    db_password='Sd#smXXaKraQLQ7r7b',
    db_host='povprdbp01.cu3hu9sx5vpk.us-east-1.rds.amazonaws.com',
    db_port='3306',
    db_database='vpcdbp01')


# Create a variable to hold your user information and call the get_db_data function using the my_connection variable.
user_list = get_db_data(my_connection)
evaluated_user_list = []
user_count = 0

# Loop through all the users returned from the DB and add their data to the evaluated_user_list
for user in user_list:
    time.sleep(.75)
    user_count += 1
    new_user = User(user[0], user[1])
    new_user.get_cognito_attr_value()

    user_dict = {}

    user_dict['user_id'] = new_user.user_id
    user_dict[RDS_TABLE_COLUMN] = new_user.rds_value
    user_dict[COGNITO_ATTRIBUTE] = new_user.cognito_value
    user_dict['evaluation'] = new_user.rds_cognito_match()

    evaluated_user_list.append(user_dict)

    sys.stdout.write(f'\rUsers processed: {user_count}')
    sys.stdout.flush()

report_name = f'{RDS_TABLE_COLUMN}_{datetime.datetime.now()}.csv'

print(f'\nCreating {report_name}')

if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

with open(os.path.join(FOLDER_NAME, report_name), 'w', newline='') as report:

    fieldnames = [
        'user_id',
        RDS_TABLE_COLUMN,
        COGNITO_ATTRIBUTE,
        'evaluation'
    ]
    writer = csv.DictWriter(report, fieldnames=fieldnames)

    writer.writeheader()
    for data in evaluated_user_list:
        writer.writerow(data)

print(f'\nProcess Complete!')
