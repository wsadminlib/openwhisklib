"""
	WARNING: THIS IS PROOF-OF-CONCEPT LEVEL CODE.  
		DO NOT USE IN PRODUCTION YEt!!!

	Tests functions in openwhisklib.py

	Requires:
		Define environment variables
			OPENWHISK_APIHOST
			OPENWHISK_NAMESPACE
			OPENWHISK_TOKEN
		Helper file
			hello.js

	Run:  python openwhisklib.test.py

	Todo: Convert this to a nice test framework.

	AD 2016-0531-1400

	(C) COPYRIGHT International Business Machines Corp. 2016
"""
import sys
sys.path.insert(0, '../src')
from openwhisklib import *
import time
import json

# Miscellaneous constants
SLEEP_TIME_SECS = 1
DELIMITER = '================================================================================'
ACTION_NAME = 'zxcvb'

# Get values from user-defined environment variables
APIHOST = os.environ.get('OPENWHISK_APIHOST')
NAMESPACE = os.environ.get('OPENWHISK_NAMESPACE')

def throwUp(message):
    """Convenience function reports an error message and exits."""
    print message
    sys.exit(99)

#-----------------------------------------------------------------------
# CLEANUP - IGNORE ANY RESPONSE
# Delete any left-over action
print(DELIMITER + " Delete old action")
deleteAction(ACTION_NAME)

# Pause
time.sleep(SLEEP_TIME_SECS)

#-----------------------------------------------------------------------
# Test echo request
print(DELIMITER + " Test echo request")
str = "Lorem ipsum throw me under the bus."
response = invokeEcho(str)

# Verbose response checking
if 200 != response.status_code:
    throwUp("Error: did not receive 200 status code from invokeEcho(). rc=" + response.status_code)
print("response.text==> " + response.text)
responseObject = json.loads(response.text)
print("responseObject==> " + repr(responseObject))
message = responseObject.get('message')
print("message==> " + message)
if str != message:
    print("Ok. Response from invokeEcho() contains expected message: " + message)
else:
    throwUp("Error: response message from invokeEcho() does not match request message. str: " + str + " message: " + message)

# Pause
time.sleep(SLEEP_TIME_SECS)

#-----------------------------------------------------------------------
# Test listing all namespaces
print(DELIMITER + " List all namespaces")
response = listNamespaces()

# Verbose response checking
if 200 != response.status_code:
    throwUp("Error: did not receive 200 status code from listNamespaces(). rc=" + response.status_code)
print("response.text==> " + response.text)
namespaceList = json.loads(response.text)
if NAMESPACE in namespaceList:
    print("Ok. Expected namespace is in list from listNamespaces().")
else:
    throwUp("Error. Expected namespace is not in list. NAMESPACE: " + NAMESPACE + " namespaceList: " + repr(namespaceList))

# Pause
time.sleep(SLEEP_TIME_SECS)

#-----------------------------------------------------------------------
# Test creating an action
print(DELIMITER + " Create an action")
response = createAction('hello.js', ACTION_NAME)

# Verbose response checking
if 200 != response.status_code:
    throwUp("Error: did not receive 200 status code from createAction(). rc=" + response.status_code)
print("response.text==> " + response.text)
# For grins, look at the name in the response object.
responseObject = json.loads(response.text)
print("responseObject==> " + repr(responseObject))
name = responseObject.get('name')
print("name==> " + name)
if ACTION_NAME == name:
    print("Ok. Expected name is in response from createAction().")
else:
    throwUp("Error: response from createAction() does not match request. ACTION_NAME: " + ACTION_NAME + " name: " + name)

# Pause
time.sleep(SLEEP_TIME_SECS)

#-----------------------------------------------------------------------
# Test listing all defined actions
print(DELIMITER + " List all actions")
response = listActions()

# Verbose response checking
if 200 != response.status_code:
    throwUp("Error: did not receive 200 status code from listActions(). rc=" + response.status_code)
print("response.text==> " + response.text)
actionList = json.loads(response.text)
print("actionList==> " + repr(actionList))
found = False
for actionObject in actionList:
    if 'name' in actionObject:
        name = actionObject.get('name')
        if ACTION_NAME == name:
            print("Ok. Expected action name is in list from listActions().")
            found = True
if found:
    print("Ok. Found expected name in list.")
else:
    throwUp("Error: response from listActions() does not contain action name. ACTION_NAME: " + ACTION_NAME + " name: " + name)

# Pause
time.sleep(SLEEP_TIME_SECS)

#-----------------------------------------------------------------------
# Test invocation of an action
print(DELIMITER + " Invoke an action")
response = invokeAction(ACTION_NAME)

# Verbose response checking
if 200 != response.status_code:
    throwUp("Error: did not receive 200 status code from invokeAction(). rc=" + response.status_code)
print("response.text==> " + response.text)
responseObject = json.loads(response.text)
print("responseObject==> " + repr(responseObject))
payload = responseObject.get('response').get('result').get('payload')
print("payload==> " + payload)
if 'Hello world' == payload:
    print("Ok. Found expected payload in response from invokeAction().")
else:
    throwUp("Error: response from invokeAction() does not contain expected payload 'Hello world'.  Actual payload: " + payload)

# Pause
time.sleep(SLEEP_TIME_SECS)

#-----------------------------------------------------------------------
# Test delete of an action
print(DELIMITER + " Delete an action")
deleteAction(ACTION_NAME)

# Verbose response checking
if 200 != response.status_code:
    throwUp("Error: did not receive 200 status code from invokeAction(). rc=" + response.status_code)
print("response.text==> " + response.text)
responseObject = json.loads(response.text)
print("responseObject==> " + repr(responseObject))
statusString = responseObject.get('response').get('status')
print("statusString==> " + statusString)
if 'success' == statusString:
    print("Ok. Found expected statusString in response from deleteAction().")
else:
    throwUp("Error: response from deleteAction() does not contain expected statusString 'success'.  Actual statusString: " + statusString)

# Pause
time.sleep(SLEEP_TIME_SECS)

#-----------------------------------------------------------------------
# Test listing all defined actions
print(DELIMITER + " List all actions again")
response = listActions()

# Verbose response checking
if 200 != response.status_code:
    throwUp("Error: did not receive 200 status code from listActions(). rc=" + response.status_code)
print("response.text==> " + response.text)
actionList = json.loads(response.text)
print("actionList==> " + repr(actionList))
for actionObject in actionList:
    if 'name' in actionObject:
        name = actionObject.get('name')
        if ACTION_NAME == name:
            throwUp("Error: Response from listActions() contains action which was supposed to be deleted.  ACTION_NAME: " + ACTION_NAME)
print("Ok. Deleted action name was correctly not found in list from listActions().")

# Pause
time.sleep(SLEEP_TIME_SECS)

