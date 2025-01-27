import http.client

class Mongoose:

    def __init__(self, auth:str):
        self.conn = http.client.HTTPSConnection("api.mongooseresearch.com")
        self.payload = ''
        self.headers = {
        'Authorization': f'Basic {auth}=='
        }

    def get_contact(self, dept_code: str, extra: str):
        self.conn.request("GET", f"/v2/contacts/{dept_code}/{extra}", self.payload, self.headers)
        res = self.conn.getresponse()
        data = res.read()
        return data.decode("utf-8")