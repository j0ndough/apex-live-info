# apex-live-info
Script that grabs live info from [Apex Legends Status](https://apexlegendsstatus.com/).
Currently supports crafting and map rotations.

May be repurposed into a Discord bot or something later, TBD.

## Usage

First, register for an API key [here](https://apexlegendsapi.com/).

Rename `config.cfg` to `api_config.cfg` and paste your API key into the `CLIENT_ID` field.

Run `python main.py` with the appropriate arguments and options to get live info.

**Arguments**

`-r <R>` or `--request <REQUEST>` : Specifies the desired live info request with a desired option.

Request options:

`crafting` : Gets current crafting rotation.

`map` : Gets current map rotation for BR Pubs, BR Ranked, and Mixtape (Rotating LTM).

### Example Argument
`python main.py -r map` Gets the current map rotation (BR Pubs, BR Ranked, and rotating LTM).