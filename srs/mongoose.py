import http.client
import json

class Mongoose:

    def __init__(self, auth:str):
        self.auth = auth
        self.conn = http.client.HTTPSConnection("api.mongooseresearch.com")

    def get_contact(self, dept_code: str, mobile_number: str):
        self.conn.request("GET", f"/v2/contacts/{dept_code}/{mobile_number}", headers={'Authorization': f'Basic {self.auth}=='})
        res = self.conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    
    def update_contact(self, dept_code: str, payload: dict):
        self.conn.request("POST", f"/v2/contacts/{dept_code}", payload, headers={'Content-Type': 'application/json',
                                                                                  'Accept': 'application/json',
                                                                                  'Authorization': f'Basic {self.auth}=='})
        res = self.conn.getresponse()
        data = res.read()
        return data.decode("utf-8")