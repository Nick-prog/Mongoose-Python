import os
import srs
import json
import pandas as pd
from pprint import pprint
from dotenv import load_dotnev

def recursive(link: object, contactid: str, mobilenumber: str):

    output = m.get_contact("11016573", mobilenumber)
    if output:
        data = json.loads(output)
        pprint(data)
        link.append(data['contactId'])
        # recursive(link, data['contactId'], data['mobileNumber'])
    return link

if __name__ == "__main__":

    # Load csv file, store numbers and contactids
    curr_dir = os.getcwd()
    csv_file = os.path.join(curr_dir, 'Mongoose Load ALL 012425.csv')
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    lookup_df = df[['ContactId', 'MobileNumber']]

    # Loop list until get_contact returns a value
    load_dotnev()
    auth_key = os.getenv("AUTH_KEY")
    m = srs.Mongoose(auth_key)
    node_dict = {}
    
    for index, row in lookup_df.iterrows():
        # print(row['ContactId'], row['MobileNumber'])
        # Nested Loop to locate all connected contactid nodes
        link = srs.LinkedList()
        link.append(row['ContactId'])
        node_dict[row['ContactId']] = recursive(link, row['ContactId'], row['MobileNumber'])
    
    # Print dict
    pprint(node_dict)