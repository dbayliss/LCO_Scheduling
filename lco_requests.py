#!/bin/env/python
import requests
import argparse
import sys

'''
lco_requests.py
Gets lco request info
Daniel Bayliss 20180930
'''

# Read your authentacation token from a file "token.txt"
try:
    tokenfile = open("token.txt", "r")
    API_TOKEN = str(tokenfile.readline().strip())
    tokenfile.close()
except IOError:
    print('File token.txt not found')
    sys.exit()

parser = argparse.ArgumentParser(
        description='Script gets request info from LCO')
parser.add_argument(
        '-p', '--proposal', type=str,
        help='lco proposal id',
        required=True)
parser.add_argument(
        '-u', '--user', type=str,
        help='lco user id',
        required=True)
parser.add_argument(
        '-s', '--state', type=str,
        help='state: PENDING, SCHEDULED, WINDOW_EXPIRED, COMPLETED, CANCELED',
        default="PENDING", required=False,)
args = parser.parse_args()

user_name = args.user
proposal_id = args.proposal
state_request = args.state

response = requests.get(
    'https://observe.lco.global/api/userrequests/?state='+state_request+'&proposal='+proposal_id+'&user='+user_name,
    headers={'Authorization': 'Token {}'.format(API_TOKEN)}
)

try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

for request in response.json()['results']:
    target_name = request['requests'][0]['target']['name']
    telescope = request['requests'][0]['location']['telescope_class']
    utstart = request['requests'][0]['windows']
    request_id = request['id']
    state = request['state']
    submitter = request['submitter']
    print target_name,request_id,state,submitter,telescope

