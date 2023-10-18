import argparse
import configparser
import requests
from requests.exceptions import HTTPError

# get API key
config = configparser.ConfigParser()
config.read('api_config.cfg')
auth = '?auth=' + config['Credentials']['CLIENT_ID']
BASE_URL = 'https://api.mozambiquehe.re/'

def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--request', type=str,
                        help='Specify the request type (crafting, map, or store)', required=True)
    args = parser.parse_args()

    # check for valid args
    if args.request:
        param = ''
        if 'crafting'.casefold() == args.request.casefold():
            req = 'crafting'
            json = make_request(req, param)
            items = get_current_crafting(json)
            print('Current Crafting Rotation:')
            print_results(items, ' | ')
        elif 'map'.casefold() == args.request.casefold():
            req = 'maprotation'
            param = 'version=2'
            json = make_request(req, param)
            maps = get_current_maps(json)
            print('Current Map Rotation:')
            print_results(maps, ': ')
        elif 'store'.casefold() == args.request.casefold():
            req = 'store'
            # TODO
        else:
            raise ValueError('Invalid request type. Try crafting, map, or store.')


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


def get_current_crafting(json):
    items = {}
    for j in json:
        for b in j['bundleContent']:
            item = capitalize_string(b['itemType']['name'].replace('_', ' '))
            rarity = b['itemType']['rarity']
            cost = b['cost']
            if item not in items:
                items[item] = 'Rarity: ' + rarity + ' | Cost: ' + str(cost)
    return items


def get_current_maps(json):
    res = {}
    res['BR Pubs'] = json['battle_royale']['current']['map']
    res['BR Ranked'] = json['ranked']['current']['map']
    res['LTM - ' + json['ltm']['current']['eventName']] = json['ltm']['current']['map']
    return res


def get_current_store(json):
    # TODO
    return None


def print_results(res, spacer):
    for r in res:
        print(r + spacer + res[r])


# Custom function that capitalizes the first letter of every word.
# Compared to other similar functions, this one does not alter the capitalization of other letters.
def capitalize_string(str):
    words = str.split()
    cap_words = [capitalize_first_letter(word) for word in words]
    return ' '.join(cap_words)


# Capitalizes first letter of a word, but leaves the rest untouched.
def capitalize_first_letter(word):
    if word:
        return word[:1].upper() + word[1:]
    else:  # in case input is empty
        return word


if __name__== "__main__":
    main()