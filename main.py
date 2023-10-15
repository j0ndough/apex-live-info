import configparser
import requests
from requests.exceptions import HTTPError

config = configparser.ConfigParser()
config.read('api_config.cfg')
auth = '?auth=' + config['Credentials']['CLIENT_ID']
BASE_URL = 'https://api.mozambiquehe.re/'

def main():
    req = 'maprotation'
    param = 'version=2'
    json = make_request(req, param)
    maps = get_current_maps(json)
    print("Current map rotation:")
    for mode in maps:
        print(mode + ": " + maps[mode])


def make_request(req, param):
    try:
        response = requests.get(BASE_URL + req + auth, params=param)
        response.raise_for_status()
        json_response = response.json()
        return json_response
    except HTTPError as http_err:
        print(http_err)
        raise SystemError
    except requests.exceptions.RequestException:
        print('Other error occurred. Please try again.')
        raise SystemExit


def get_current_maps(json):
    res = {}
    res['BR Pubs'] = json['battle_royale']['current']['map']
    res['BR Ranked'] = json['ranked']['current']['map']
    res['LTM - ' + json['ltm']['current']['eventName']] = json['ltm']['current']['map']
    return res

if __name__== "__main__":
    main()