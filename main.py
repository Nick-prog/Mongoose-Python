import os
import srs
import json
import pandas as pd
from pprint import pprint
from dotenv import load_dotenv

def recursive(lookup_df: pd.DataFrame, node_dict: dict, link: object, contactid: str, mobilenumber: str):
    # Set ContactId as the index
    lookup_df.set_index('ContactId', inplace=True)

    # 110165873 is Enrollment Mgmt Dept Code
    output = m.get_contact("11016573", mobilenumber)
    
    # Avoids all error message outputs for mobile number
    if len(output) > 100:
        data = json.loads(output)
        # pprint(data)
        link.append(data['contactId'])

        # Fetch the MobileNumber directly using the index
        try:
            mobile_number = lookup_df.at[data['contactId'], 'MobileNumber']
            print(mobile_number)
        except KeyError:
            print(f"ContactId {data['contactId']} not found")
            pass

        # recursive(node_dict, link, data['contactId'], data['mobileNumber'])
    
    node_dict[contactid] = link
    return

if __name__ == "__main__":
    load_dotenv()
    auth_key = os.getenv("AUTH_KEY")
    m = srs.Mongoose(auth_key)

    # Load csv file, store numbers and contactids
    curr_dir = os.getcwd()
    csv_file = os.path.join(curr_dir, 'Mongoose Load ALL 012425.csv')
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    lookup_df = df[['ContactId', 'MobileNumber']]

    # Loop list until get_contact returns a value
    node_dict = {}
    
    for index, row in lookup_df.iterrows():
        # print(row['ContactId'], row['MobileNumber'])
        # Nested Loop to locate all connected contactid nodes
        link = srs.LinkedList()
        link.append(row['ContactId'])
        recursive(lookup_df, node_dict, link, row['ContactId'], row['MobileNumber'])
    
    # Print dict
    pprint(node_dict)