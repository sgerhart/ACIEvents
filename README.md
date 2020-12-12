# ACIEvents

ACIEvents allows you to subscribe to ACI events and react on them. 

### Requirements

Python Version:

    Python3, tested with 3.7

Python Libraries Required:

    websocket-client
    https://github.com/websocket-client/websocket-client
    
    requests version 2.22
    https://2.python-requests.org/en/master/


APIC Versions:
Should work with all version of ACI

    Tested with version
    3.2, 4.0, 4.1


### Directions

Command Line
    
    -i APIC address, -u username (readonly access), -p password
    python3 main.py -i 10.87.96.214 -u admin -p blahblah
    
To subscribe to events you need to know which object your interested in and find the class. You can find the 
class via using the API inspector, object explorer, etc. The easiest way is to interact with the UI and see 
what is happening in the background via the API inspector.  When the class is found, it will have to added to the
build_subscription function in query.py. You will created a url like the example below and add it url_subscr = {}.

Example: 

    # Events that show if static paths were created, deleted under an EPG
    rvRsPath_url = url + 'class/fvRsPathAtt.json?subscription=yes'
    
    url_subscr = {rvRsPath_url, lnode_subscr_url, tagInst_url}
    
    
The next step is to add a section under the on_message function which is located in listener.py. When a message is received, it
will be a formatted in JSON, so just parse it and build a upon it. 

