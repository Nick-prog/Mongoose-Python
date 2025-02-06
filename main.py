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
    if data['contactId'] == None or link.search(contactid) != None and len(link.hash_table) > 1:
        # print(f"{data['contactId']} leads to None. {data['firstName']} {data['lastName']} {data['mobileNumber']}")
        return link

    elif int(data['contactId']) != contactid:
        link.append(data['contactId'])
        # Look up contactid in import file for new updated number.
        try:
            mobile_number = new_df.loc[int(data['contactId']), "MobileNumber"]
            # print(f"{data['contactId']}, {mobile_number}")
        except:
            # print('No contactid found in import file!')
            return link
        link = recursive(new_df, link, int(data['contactId']), mobile_number)

    return link
        
def csv_file_linkedlist_lookup(csv_file: str):
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

    out_file = os.path.join(curr_dir, "file_import_output.txt")

    for key, value in node_dict.items():
        value.display(out_file)

def single_contact_linkedlist_lookup(contactid: int, mobilenumber: int, csv_file: str, print_flag: bool):
    main_df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    data = {
        'ContactId': [contactid],
        'MobileNumber': [mobilenumber]
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

    if print_flag:

        out_file = os.path.join(curr_dir, "single_output.txt")

        for key, value in node_dict.items():
            value.display(out_file)
    else:
        
        return node_dict

def single_contact_linkedlist_update(contactid: int, mobilenumber: int, csv_file: str, print_flag: bool):
    main_df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    df = main_df.set_index("ContactId")

    node_dict = single_contact_linkedlist_lookup(contactid, mobilenumber, csv_file, print_flag)
    node_list = []

    for key, value in node_dict.items():
        pprint(value.hash_table)
        print('\n')
        for item in value.hash_table:
            payload = json.dumps({
                "mobileNumber": str(df.loc[int(item), "MobileNumber"]),
                "uniqueCampusId": str(item),
                "firstName": str(df.loc[int(item), "FirstName"]),
                "lastName": str(df.loc[int(item), "LastName"]),
                "customFields":{
                    "Orientation_Date": str(df.loc[int(item), "Orientation_Date"]),
                    "Admission_Type": str(df.loc[int(item), "Admission_Type"]),
                    "College": str(df.loc[int(item), "College"]),
                    "Major": str(df.loc[int(item), "Major"]),
                    "City": str(df.loc[int(item), "City"]),
                    "Entry_Term": str(df.loc[int(item), "Entry_Term"]),
                    "MV_Hold": str(df.loc[int(item), "MV_Hold"]),
                    "Status": str(df.loc[int(item), "Status"]),
                    "Enrolled": str(df.loc[int(item), "Enrolled"]),
                    "Owner": str(df.loc[int(item), "Owner"]),
                    "Stage": str(df.loc[int(item), "Stage"]),
                    "Javelina_Preview_Day": str(df.loc[int(item), "Javelina_Preview_Day"]),
                    "State": str(df.loc[int(item), "State"]),
                    "County": str(df.loc[int(item), "County"]),
                    "Campus": str(df.loc[int(item), "Campus"]),
                    "HSName": str(df.loc[int(item), "HSName"])
                    },
                "allowMobileUpdate": "true"
                })
            node_list.append(payload)

    # pprint(node_list)

    for idx, item in enumerate(node_list):
        output = m.update_contact(dept_code="11016573", payload=node_list[(len(node_list)-1)-idx])
        print(item)
        print(len(output))
        if len(output) == 274:
            raise RuntimeError("Duplicate found in import!", output)
        elif len(output) == 56:
            raise RuntimeError("Mobile Number is not valid!", output)
        print(output, '\n')
        time.sleep(0.5)

if __name__ == "__main__":
    load_dotenv()
    auth_key = os.getenv("AUTH_KEY")
    m = srs.Mongoose(auth_key)

    # Load csv file, store numbers and contactids.
    curr_dir = os.getcwd()
    csv_file = os.path.join(curr_dir, 'Mongoose Load ALL 012425.csv')

    # Check multiple numbers from a csv file.
    # csv_file_linkedlist_lookup(csv_file)

    # Single number search, IF True will generate an txt file with found linked listed.
    # single_contact_linkedlist_lookup(contactid, mobilenumber, csv_file, True)

    # Update Mongoose contact based on txt file.
    # To update a link of contacts, you must start at the base of the chain.
    # EX: 1883912 -> 1971921 -> 1913150 -> 1744852, start with 1883912 and its new phone number
    # DO NOT FORGET to delete the head manually or update it. 
    # IF you forget, you will need to move the start point to another earlier part of the linked list.
    # Double check your work with the csv import file.
    single_contact_linkedlist_update(1971993, 9566677238, csv_file, False)
    
    # Update Mongoose contact based on manual payload.
    # Set any dict value to 'nan' if empty.
    # payload = json.dumps({
    #     "mobileNumber": "9566930986",
    #     "uniqueCampusId": "1448015",
    #     "firstName": "Victoria",
    #     "lastName": "Vela",
    #     "customFields":{
    #         "Orientation_Date": "nan",
    #         "Admission_Type": "nan",
    #         "College": "College of Agriculture & Natural Resources",
    #         "Major": "Agriculture Science",
    #         "City": "Zapata",
    #         "Entry_Term": "Spring 2025",
    #         "MV_Hold": "nan",
    #         "Status": "nan",
    #         "Enrolled": "Not Enrolled",
    #         "Owner": "nan",
    #         "Stage": "Decision",
    #         "Javelina_Preview_Day": "nan",
    #         "State": "TX",
    #         "County": "nan",
    #         "Campus": "Main",
    #         "HSName": "Zapata High School"
    #         },
    #     "allowMobileUpdate": "true"
    #     })
    # output = m.update_contact(dept_code="11016573", payload=payload)
    # print(output)