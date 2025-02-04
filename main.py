import os
import srs
import json
import pandas as pd
from pprint import pprint
from dotenv import load_dotenv
from tqdm import tqdm
import time
import sys

# sys.setrecursionlimit(10000) # default set to 1000

def recursive(new_df: pd.DataFrame, link: list, contactid: int, mobilenumber: int):

    # 110165873 is Enrollment Mgmt Dept Code
    output = m.get_contact("11016573", mobilenumber)

    if len(output) < 100:
        return link
    
    # Avoids all error message outputs for mobile number
    data = json.loads(output)
    # pprint(data)
    if data['contactId'] == None or link.search(contactid) != None and len(link.hash_table) > 1:
        # print(f"{data['contactId']} leads to None. {data['firstName']} {data['lastName']} {data['mobileNumber']}")
        return link

    elif int(data['contactId']) != contactid:
        link.append(data['contactId'])
        # Look up contactid in import file for new updated number.
        try:
            mobile_number = new_df.loc[int(data['contactId']), "MobileNumber"]
            print(f"{data['contactId']}, {mobile_number}")
        except:
            print('No contactid found in import file!')
            return link
        link = recursive(new_df, link, int(data['contactId']), mobile_number)

    return link
        
def file_import_check():
    csv_file = os.path.join(curr_dir, 'Mongoose Load ALL 012425.csv')
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    lookup_df = df[['ContactId', 'MobileNumber']]

    # Set ContactId as index for faster lookups
    new_df = lookup_df.set_index("ContactId")
    # lookup_df.set_index('ContactId', inplace=True)
    # pprint(new_df)

    # Loop list until get_contact returns a value
    node_dict = {}

    for index, row in tqdm(lookup_df.iterrows(), desc='Recursive Loop', unit='iteration'):
        # print(index, row['ContactId'], row['MobileNumber'])

        # Set up link node for initial contactid
        link = srs.HashLinkedList()
        link.append(row['ContactId'])

        # Nested Loop to locate all connected contactid nodes
        link = recursive(new_df, link, row['ContactId'], row['MobileNumber'])
        node_dict[index] = link

        time.sleep(0.05)

    out_file = os.path.join(curr_dir, "output.txt")

    for key, value in node_dict.items():
        value.display(out_file)

def single_check():
    csv_file = os.path.join(curr_dir, 'Mongoose Load ALL 012425.csv')
    main_df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    data = {
        'ContactId': [1987995],
        'MobileNumber': [8325739902]
    }

    df = pd.DataFrame(data)

    # Set ContactId as index for faster lookups
    new_df = main_df.set_index("ContactId")

    # Loop list until get_contact returns a value
    node_dict = {}

    for index, row in tqdm(df.iterrows(), desc='Recursive Loop', unit='iteration'):
        # print(index, row['ContactId'], row['MobileNumber'])

        # Set up link node for initial contactid
        # link = srs.LinkedList()
        link = srs.HashLinkedList()
        link.append(row['ContactId'])

        # Nested Loop to locate all connected contactid nodes
        link = recursive(new_df, link, row['ContactId'], row['MobileNumber'])
        node_dict[index] = link

        time.sleep(0.05)

    out_file = os.path.join(curr_dir, "output.txt")

    for key, value in node_dict.items():
        value.display(out_file)


if __name__ == "__main__":
    load_dotenv()
    auth_key = os.getenv("AUTH_KEY")
    m = srs.Mongoose(auth_key)

    # Load csv file, store numbers and contactids
    curr_dir = os.getcwd()

    # Check multiple numbers from a csv file
    file_import_check()

    # Single number search
    # single_check()
    
    