#!/bin/env/python
import requests
import argparse
import sys

'''
lco_cancel_all.py
Cancels pending requests for ALL targets on the proposal!
Daniel Bayliss 20181012
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
        description='Script schedules observations on LCO')
parser.add_argument(
        '-p', '--proposal', type=str,
        help='lco proposal id',
        required=True)
parser.add_argument(
        '-k', '--kill', type=str,
        default="no", help='really kill requests? "yes" or "no"? default is no.',
        required=False)
args = parser.parse_args()

proposal_id = args.proposal
state_request = 'PENDING'

response = requests.get(
    'https://observe.lco.global/api/userrequests/?state='+state_request+'&proposal='+proposal_id,
    headers={'Authorization': 'Token {}'.format(API_TOKEN)}
)

try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

id_list = []

if args.kill != "yes":
    print "WARNING - This machine kills fascists (and ALL your proposal requests)"

for request in response.json()['results']:
    target_name = request['requests'][0]['target']['name']
    telescope = request['requests'][0]['location']['telescope_class']
    request_id = request['id']
    group_id = request['group_id']
    state = request['state']
    submitter = request['submitter']
    print "request found:",target_name,request_id,state,submitter,telescope,group_id
    if args.kill == "yes":
        print "request cancelled",target_name,request_id,state,submitter,telescope
        response = requests.post(
            'https://observe.lco.global/api/userrequests/{}/cancel/'.format(request_id),
            headers={'Authorization': 'Token {}'.format(API_TOKEN)}
        )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        print('Request failed: {}'.format(response.content))
        raise exc

if args.kill != "yes":
    print "WARNING - This machine kills fascists (and ALL your proposal requests)"
