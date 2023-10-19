# apex-live-info
Script that grabs live info from [Apex Legends Status](https://apexlegendsstatus.com/).

Currently supports crafting and map rotations, and current status of live matchmaking servers.

May be repurposed into a Discord bot or something later, TBD.

## Usage

First, register for an API key [here](https://apexlegendsapi.com/).

Rename `config.cfg` to `api_config.cfg` and paste your API key into the `CLIENT_ID` field.

Run `python main.py` with the appropriate argument to get live info.

**Arguments**

`-c` or `--crafting` : Gets current crafting rotation.

`-m` or `--map` : Gets current map rotation for BR Pubs, BR Ranked, and Mixtape (Rotating LTM).

`-s` or `--store` : Gets the current recolor rotation from the in-game store. However, this is option
is currently bugged and does not work.

`-st` `--status` : Gets current status of live matchmaking servers for all regions.

### Example Argument
`python main.py -m` Gets the current map rotation (BR Pubs, BR Ranked, and rotating LTM).