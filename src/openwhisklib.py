"""
	WARNING: THIS IS PROOF-OF-CONCEPT LEVEL CODE.  
		DO NOT USE IN PRODUCTION YET!!!


	Set of utility functions to communicate with OpenWhisk at Bluemix


	Requires:
		Define environment variables
			OPENWHISK_APIHOST
			OPENWHISK_NAMESPACE
			OPENWHISK_TOKEN


	Todo: Clean, organize, and modularize this code.


	AD 2016-0531-1429

	(C) COPYRIGHT International Business Machines Corp. 2016
"""
import os
import requests
import json
import sys


# Check for required environment variables.
if 'OPENWHISK_APIHOST' not in os.environ:
	print("Invocation error: Environment variable OPENWHISK_APIHOST must be defined.")
	sys.exit(99)
if 'OPENWHISK_NAMESPACE' not in os.environ:
	print("Invocation error: Environment variable OPENWHISK_NAMESPACE must be defined.")
	sys.exit(99)
if 'OPENWHISK_TOKEN' not in os.environ:
	print("Invocation error: Environment variable OPENWHISK_TOKEN must be defined.")
	sys.exit(99)
    

# Miscellaneous constants
HEADERS = {\
	'Authorization': 'Basic ' + os.environ.get('OPENWHISK_TOKEN'),\
	'content-type': 'application/json'\
}
APIHOST = os.environ.get('OPENWHISK_APIHOST')
NAMESPACE = os.environ.get('OPENWHISK_NAMESPACE')
APIVERSION = 'v1'



def createAction(filename, action):
	"""Uploads contents of the specified file to the specified action."""

	# Read the file into a string

	code = open(filename).read()
	#print('File ' + filename + ' contents: >>>' + code + '<<<')

	# Define the request

	url = 'https://' + APIHOST + '/api/' + APIVERSION + '/namespaces/' + NAMESPACE + '/actions/' + action

	payload = {"exec": {"kind": "nodejs", "code": code}}
	# print('payload: ' + repr(payload))

	# Issue the request

	print('Issuing put request: url=' + url + ' payload: ' + repr(payload) + ' headers=' + repr(HEADERS))
	response = requests.put(url, data=json.dumps(payload), headers=HEADERS, verify=False)

	# Show the response

	print('Response status_code=%i' % response.status_code)
	print(response.text)

	return(response)


def deleteAction(action):
	"""Deletes the specified action."""

	# Define the request 

	url = 'https://' + APIHOST + '/api/' + APIVERSION + '/namespaces/' + NAMESPACE + '/actions/' + action

	# Issue the request

	print('Issuing delete request: url=' + url + ' headers=' + repr(HEADERS))
	response = requests.delete(url, headers=HEADERS, verify=False)

	# Show the response

	print('Response status_code=%i' % response.status_code)
	print(response.text)

	return(response)


def invokeAction(action):
	"""Invokes the specified action in blocking mode."""

	# Define the request 

	url = 'https://' + APIHOST + '/api/' + APIVERSION + '/namespaces/' + NAMESPACE + '/actions/' + action + '?blocking=true&result=false'

	payload = {}

	# Issue the request

	print('Issuing request: url=' + url + ' payload=' + repr(payload) + ' headers=' + repr(HEADERS))
	response = requests.post(url, data=json.dumps(payload), headers=HEADERS, verify=False)

	# Show the response

	print('Response status_code=%i' % response.status_code)
	print(response.text)

	return(response)


def invokeEcho(message):
	"""Issues a very basic echo request"""

	# Define the request 

	url = 'https://' + APIHOST + '/api/' + APIVERSION + '/namespaces/whisk.system/actions/samples/echo?blocking=true&result=true'

	payload = { 'message': message }

	# Issue the request

	print('Issuing request: url=' + url + ' payload=' + repr(payload) + ' headers=' + repr(HEADERS))
	response = requests.post(url, data=json.dumps(payload), headers=HEADERS, verify=False)

	# Show the response

	print('Response status_code=%i' % response.status_code)
	print(response.text)

	return(response)


def listActions():
	"""Lists the actions defined in openwhisk at bluemix."""

	# Define the request 

	url = 'https://' + APIHOST + '/api/' + APIVERSION + '/namespaces/' + NAMESPACE + '/actions?skip=0&limit=30'

	# Issue the request

	print('Issuing request: url=' + url + ' headers=' + repr(HEADERS))
	response = requests.get(url, headers=HEADERS, verify=False)

	# Show the response

	print('Response status_code=%i' % response.status_code)
	print(response.text)

	return(response)


def listNamespaces():
	"""Lists the namespaces defined in openwhisk at bluemix."""

	# Define the request 

	url = 'https://' + APIHOST + '/api/' + APIVERSION + '/namespaces/'

	# Issue the request

	print('Issuing request: url=' + url + ' headers=' + repr(HEADERS))
	response = requests.get(url, headers=HEADERS, verify=False)

	# Show the response

	print('Response status_code=%i' % response.status_code)
	print(response.text)

	return(response)





