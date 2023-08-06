
import logging
import json
import requests

# needs to be in sync with setup.py and documentation (conf.py, branch gh-pages)
__version__ = '0.0.1'

class Symcon:
    '''Connects to IP-Symcon instance via json rpc request'''

    def __init__(self, server, port=3777,
                 protocol="http", username="", password=""):
        '''
        Instantiate connector object.

        :param server: address of ip-symcon server
        :param port: http(s) port of server
        :param protocol: 'http' or 'https'
        :param username: username for http(s) basicAuth validation
        :param password: (global) http(s) password
        '''
        self.log = logging.getLogger("Symcon")

        validprots = ['http', 'https']
        self.server = server
        self.port = port
        self.username = username
        self.password = password

        # Check if protocol is supported
        if protocol in validprots:
            self.protocol = protocol
        else:
            self.log.error("Invalid protocol: {}".format(protocol))

        self.baseurl = "{}://{}:{}@{}:{}/api/".format(protocol, username, password, server, port)
        self.headers = "content-type: application/json"
        self.headers = ""
        self.log.info("Server ist " + server)

    def send(self,payload):
        try:
            r = requests.post(
                self.baseurl, data=json.dumps(payload), headers=self.headers)
            if(r.status_code != 200):
                raise ValueError("ip-symcon api did not respond with http okay code 200")

        except:
            print("Unexpected error occured on calling ip-symcon api")
            raise

        jsonResult = json.loads(r.text)

        # check for error in response
        if "error" in jsonResult:
            raise ValueError(jsonResult["error"]["message"])
        
        return jsonResult["result"]

    
    # ------------------------------------
    # Execute ip-symcon command
    # Returns message provided by ip-symcon
    # Example #1: IPS_GetKernelDir
    # Example #2: IPS_GetKernelVersion
    # ------------------------------------
    def execCommand(self,cmd):
        payload = {
            "method": cmd,
            "params": [],
            "jsonrpc": "2.0",
            "id": 0
        }
        return self.send(payload)


    # ------------------------------------
    # Runs ip-symcon script
    # Returns just "True" if script exists or throws exception if scriptId is unknown.
    # Any returns or echo outputs in ip-symcon script will not be returned
    # ------------------------------------
    def execScript(self,scriptId):
        payload = {
            "method": "IPS_RunScript",
            "params": [scriptId],
            "jsonrpc": "2.0",
            "id": 0
        }
        return self.send(payload)

    # ------------------------------------
    # Returns (raw) value of variable
    # If formatted is true output will be formatted according to var profile
    # ------------------------------------
    def getValue(self,varId,formatted=False):
        method = "GetValue"
        if formatted:
            method = "GetValueFormatted"
        payload = {
            "method": method,
            "params": [varId],
            "jsonrpc": "2.0",
            "id": 0
        }
        return self.send(payload)

    # ------------------------------------
    # Sets value of variable
    # ------------------------------------
    def setValue(self,varId,value):
        payload = {
            "method": "SetValue",
            "params": [varId,value],
            "jsonrpc": "2.0",
            "id": 0
        }
        return self.send(payload)

    # ------------------------------------
    # Request action of variable
    # ------------------------------------
    def requestAction(self,varId,value):
        payload = {
            "method": "RequestAction",
            "params": [varId,value],
            "jsonrpc": "2.0",
            "id": 0
        }
        return self.send(payload)

    # ------------------------------------
    # Get object details
    # ------------------------------------
    def getObjDetails(self,varId):
        payload = {
            "method": "IPS_GetObject",
            "params": [varId],
            "jsonrpc": "2.0",
            "id": 0
        }
        
        tmp = self.send(payload)
        return json.dumps(tmp)
        
    # ------------------------------------
    # Find object by name
    # Returns objectid if object is found
    # ------------------------------------
    def getIdByName(self,objectName,parentId):
        payload = {
            "method": "IPS_GetObjectIDByName",
            "params": [objectName,parentId],
            "jsonrpc": "2.0",
            "id": 0
        }
        return self.send(payload)

    # ------------------------------------
    # List details from child objects under parent objectId (non recursive)
    # Returns list with child object details
    # ------------------------------------
    def getChildsList(self,parentId):
        payload = {
            "method": "IPS_GetChildrenIDs",
            "params": [parentId],
            "jsonrpc": "2.0",
            "id": 0
        }
        listChilds = self.send(payload)
        listDetails = []
        for i in listChilds:
            listDetails.append(self.getObjDetails(i))
        
        return json.dumps(listDetails)