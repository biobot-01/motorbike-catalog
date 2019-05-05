#!/usr/bin/env python3

import sys

import requests
from requests.exceptions import HTTPError

print('Running tests on app....\n')
address = input('Enter server address.\nIf left blank the connection '
                'will be set to "http://localhost:8000": ')

if address == '':
    address = 'http://localhost:8000'

# Make a get request to index page
print('\nTest 1: Making a GET request to http://localhost:8000...')
try:
    url = 'http://localhost:8000'
    r = requests.get(url)
    r.raise_for_status()
except HTTPError as http_e:
    print('Test 1 FAILED: Could not make GET request to /')
    print(http_e)
    sys.exit()
else:
    print('Test 1 PASSED: Successfully made GET request to /')

# Make a get request to bike manufacturer
print('Test 2: Making a GET requests to /bikes/<manufacturer>')
try:
    manufacturers = ['Honda', 'Kawasaki', 'Suzuki', 'Yamaha']
    for manufacturer in manufacturers:
        url = address + '/bikes/{}'.format(manufacturer)
        r = requests.get(url)
        r.raise_for_status()
except HTTPError as http_e:
    print('Test 2 FAILED: Could not make GET requests to '
          '/bikes/<manufacturer>')
    print(http_e)
    sys.exit()
else:
    print('Test 2 PASSED: Successfully made GET requests to '
          '/bikes/<manufacturer>')
    print('ALL TESTS PASSED!!')
