from argparse import ArgumentParser
import os
import csv
import requests
import json

APP_ID_KEY = 'SENDBIRD_APPLICATION_ID'
TOKEN_KEY = 'SENDBIRD_TOKEN'
ENV_FILE = '.env'

USER_ID = 'user_id'
NICKNAME = 'nickname'
PROFILE_URL = 'profile_url'


def configFile():
    # Append to existing
    f = open(ENV_FILE, 'a')
    if f is None:
        # Oop - create a new one!
        f = open(ENV_FILE, 'w+')
    return f


def newApplicationId():
    print(f'Sendbird application id:')
    aid = input()
    # TODO: Validation
    if aid is None or aid == '':
        print(f'Invalid application id')
        return newApplicationId()
    f = configFile()
    f.write(f"{APP_ID_KEY}='{aid}'\n")
    f.close()
    return aid


def newToken():
    print(f'Sendbird primary or secondary token:')
    token = input()
    # TODO: Validation
    if token is None:
        print(f'Invalid token')
        return newToken()
    f = configFile()
    f.write(f"{TOKEN_KEY}='{token}'\n")
    f.close()
    return token


def getEnvValue(target_key):
    if os.path.exists(ENV_FILE) == False:
        return None
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            if target_key != key:
                continue
            # Strip those quotes
            value = value[1:-1]
            return value


def getApplicationId():
    aid = getEnvValue(APP_ID_KEY)
    if aid is None:
        aid = newApplicationId()
    return aid


def getToken():
    token = getEnvValue(TOKEN_KEY)
    if token is None:
        token = newToken()
    return token


def specifySourceCSV():
    print('Enter a .csv file with user data to upload:')
    result = input()
    return result


def getEndpoint(app_id):
    return f'https://api-{app_id}.sendbird.com/v3'


def getHeaders(token):
    return {
        'Content-Type': 'application/json',
        'Api-Token': token
    }


def createUser(data, app_id, token):
    if data[USER_ID] is None:
        print(f'Missing {USER_ID} from {data}')
        return
    if data[NICKNAME] is None:
        print(f'Missing {NICKNAME} from {data}')
        return
    if data[PROFILE_URL] is None:
        print(f'Missing {PROFILE_URL} from {data}')
        return
    endpoint = getEndpoint(app_id) + '/users'
    headers = getHeaders(token)
    # print(f'endpoint: {endpoint}')
    # print(f'headers: {headers}')
    # TODO: Validate data
    print(
        f'Sending create user request for user with nickname: {data[NICKNAME]}...')
    r = requests.post(url=endpoint, headers=headers, data=json.dumps(data))
    print(f'Response code: {r.status_code}: {r.reason}')


def main(csv_file):
    print()
    if csv_file is None:
        print(f'Source .csv file NOT specified')
        csv_file = specifySourceCSV()
    if os.path.exists(csv_file) == False:
        print(
            f'Source {csv_file} .csv file not found. Please check the source file and path.')
        return False
    aid = getApplicationId()
    token = getToken()

    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            createUser(row, aid, token)

    return True


# Parse Args
parser = ArgumentParser()
parser.add_argument("-f", "--file",
                    dest="file",
                    help=".csv filepath to import and upload to the target Sendbird app")

args = parser.parse_args()

# Run baby run
main(args.file)
