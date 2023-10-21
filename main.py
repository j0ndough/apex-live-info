import argparse
import asyncio
import configparser
import httpx

# get API key
config = configparser.ConfigParser()
config.read('api_config.cfg')
auth = '?auth=' + config['Credentials']['CLIENT_ID']
BASE_URL = 'https://api.mozambiquehe.re/'

def main():
    # parse args
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--crafting', action='store_true',
                        help='Gets the current crafting rotation.')
    group.add_argument('-m', '--map', action='store_true',
                        help='Gets the current map rotation (BR Pubs/BR Ranked/Mixtape LTM).')
    group.add_argument('-s', '--store', action='store_true',
                        help='Gets the current recolor rotation in the store (currently bugged).')
    group.add_argument('-st', '--status', action='store_true',
                        help='Gets the current server status for Apex Legends.')
    args = parser.parse_args()

    param = {}
    if args.crafting:
        req = 'crafting'
        json = asyncio.run(make_request(req, param))
        items = get_current_crafting(json)
        print('Current Crafting Rotation:')
        print_results(items, ' | ')
    elif args.map:
        req = 'maprotation'
        param['version'] = '2'
        json = asyncio.run(make_request(req, param))
        maps = get_current_maps(json)
        print('Current Map Rotation:')
        print_results(maps, ': ')
    elif args.status:
        req = 'servers'
        json = asyncio.run(make_request(req, param))
        status = get_current_status(json)
        print('Current matchmaking server status (provided by ALS):')
        print_results(status, ' - ')
    elif args.store:
        # Retriving recolor information from the store is currently bugged
        req = 'store'
        # json = asyncio.run(make_request(req, param))
        print("No recolor information found.")


async def make_request(req: str, params: dict) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL + req + auth, params=params)
            response.raise_for_status()
            json_response = response.json()
            return json_response
    except httpx.HTTPError as http_err:
        print(http_err)
        raise SystemError
    except Exception as e:
        print('Other error occurred. ' + e + '. Please try again.')
        raise SystemError


def get_current_crafting(json: dict) -> dict:
    items = {}
    for j in json:
        for b in j['bundleContent']:
            item = capitalize_string(b['itemType']['name'].replace('_', ' '))
            rarity = b['itemType']['rarity']
            cost = b['cost']
            if item not in items:
                items[item] = 'Rarity: ' + rarity + ' | Cost: ' + str(cost)
    return items


def get_current_maps(json: dict) -> dict:
    res = {}
    res['BR Pubs'] = json['battle_royale']['current']['map']
    res['BR Ranked'] = json['ranked']['current']['map']
    res['LTM - ' + json['ltm']['current']['eventName']] = json['ltm']['current']['map']
    return res


# The store endpoint is currently bugged and does not return recolor information.
def get_current_store(json: dict) -> dict:
    # TODO
    # recolors = {}
    # return recolors
    return None


# Get current matchmaking server status for all regions.
def get_current_status(json: dict) -> dict:
    servers = json['EA_novafusion']
    res = dict.fromkeys(['EU West', 'EU East', 'US West', 'US Central', 'US East', 'South America', 'Asia'])
    for s, r in zip(servers, res):
        res[r] = 'Status: ' + servers[s]['Status'] + ', Response Time: ' + str(servers[s]['ResponseTime']) + ' ms'
    return res

def print_results(res: dict, spacer: str):
    for r in res:
        print(r + spacer + res[r])


# Custom function that capitalizes the first letter of every word.
# Compared to other similar functions, this one does not alter the capitalization of other letters.
def capitalize_string(str: str) -> str:
    words = str.split()
    cap_words = [capitalize_first_letter(word) for word in words]
    return ' '.join(cap_words)


# Capitalizes first letter of a word, but leaves the rest untouched.
def capitalize_first_letter(word: str) -> str:
    if word:
        return word[:1].upper() + word[1:]
    else:  # in case input is empty
        return word


if __name__== "__main__":
    main()