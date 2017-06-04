
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client, file
from oauth2client import tools
from oauth2client.file import Storage
#from quickstart import get_credentials

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/slides.googleapis.com-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/presentations.readonly'
SCOPES = 'https://www.googleapis.com/auth/presentations'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Slides API Python Quickstart'

def get_credentials():

    #credential_path = os.path.join(credential_dir, 'slides.googleapis.com-python-quickstart.json')
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'client_secret.json')
    """
    home_dir = os.path.expanduser('.')
    credential_path = os.path.join(home_dir, 'client_secret.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('slides', 'v1', http=http)
"""
flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()
credentials = STORAGE.get()
credentials = tools.run(flow, STORAGE, http=http)
http = credentials.authorize(http)
"""
presentationId = '1v9dyXD-z3OXachFxD5Bij8MH6LQc5kB-uMaDuPN0KEs'
presentation = service.presentations().get(
        presentationId=presentationId).execute()
slides = presentation.get('slides')


# Add a slide at index 1 using the predefined 'TITLE_AND_TWO_COLUMNS' layout and
# the ID page_id.
page_id = "MyNewSlide_001"

requests = [
    {
        'createSlide': {
            'objectId': page_id,
            'insertionIndex': '1',
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
            }
        }
    }
]

# If you wish to populate the slide with elements, add element create requests here,
# using the page_id.

# Execute the request.
body = {
    'requests': requests
}
response = service.presentations().batchUpdate(presentationId=presentationId,
                                                      body=body).execute()
create_slide_response = response.get('replies')[0].get('createSlide')
print('Created slide with ID: {0}'.format(create_slide_response.get('objectId')))