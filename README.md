# FactorioWorld

A mod for factorio that changes the map into a real-world map.  You can choose between 'Atlantic' and 'Pacific' centered.  

Note that it only changes the terrain, and not the spawning of resources. This is on the list of things to do, so maybe in the future!

# Download

You can get this mod here: https://mods.factorio.com/mods/TheOddler/factorio-world

# Usage

* Start a new game
* Choose a map layout - Atlantic or Pacific
* Choose a spawn city
* Map and terrain are generated from a map of Earth!

# Settings

Use the in-game mod settings to set:

* World Map: Atlantic or Pacific. The difference is which is in the center of the world.  Detailed uses about 4x memory.
* Map scaling factor: Can be anything between 0.01 and infinite (factors of 6 work well)
* Spawn:
    * Pick a location to start, or set to custom
    * When set to custom, it'll use the custom spawn x and y coordinates
* Repeat map: If set to false everything after the first iteration will become water
* Safe zone size: All water within this zone will be turned into dirt

# Available Spawn locations

This is a list of the regions and cities | found in 'data/spAawns.lua':

| Continent       | Region         | City        |
|:----------------|:---------------|:------------|
| Africa          | Mali           | Bamako      |
| Africa          | Congo          | Katanga     |
| Africa          | Chad           | Mongo       |
| Africa          | Egypt          | Cairo       |
| Africa          | Morocco        | Marrakech   |
| Asia            | China          | Beijing     |
| Asia            | China          | Kunming     |
| Asia            | Georgia        | Tbilisi     |
| Asia            | India          | Delhi       |
| Asia            | Saudi Arabia   | Riyadh      |
| Asia            | Mongolia       | Moron       |
| Europe          | Czech Republic | Prague      |
| Europe          | Russia         | Aktobe      |
| Europe          | Russia         | Bilibino    |
| Europe          | Russia         | Moscow      |
| Europe          | Russia         | Omsk        |
| Europe          | Russia         | Pechora     |
| Europe          | Russia         | Yakutsk     |
| Europe          | Spain          | Madrid      |
| North America   | Canada         | Brisay      |
| North America   | Canada         | Kapuskasing |
| North America   | Canada         | Saskatoon   |
| North America   | Greenland      | Summit Camp |
| North America   | Mexico         | Mexico City |
| North America   | United States  | Boise       |
| North America   | United States  | Scranton    |
| North America   | United States  | Topeka      |
| North America   | United States  | Ungalik     |
| South America   | Brazil         | Manaus      |
| South America   | Argentina      | Cordoba     |
| Oceania         | Australia      | Broome      |
| Oceania         | Australia      | Sydney      |


# Generating your own maps

The mod reads lua files generated by a converter writen in Python.
These files are generated based on an image.
Currently I'm using the "Natural Earth II with Shaded Relief, Water, and Drainages" image from [Natural Earth](http://www.naturalearthdata.com/downloads/10m-raster-data/10m-natural-earth-2/).

The 'Pacific' map has been modified to switch the continents and remove Antarctica.  

The generator simply iterates over each pixel, and assigns a tile-type to it.
The algorithm uses reference colors, and checks which one is closer to encode the types.
To compress the data a little I use a scheme where every tile-letter is followed by how many tiles there are of this type of that row.
The mod then takes these strings (one for each line of pixels), decompresses it to something it can read very quickly, and assigns the tiles a new type when a chunk is generated.

## Require Python libraries

* Pillow - for processing the images: `pip install Pillow`
* tqdm - for fast loading bars: `pip install tqdm`

## Usage

To generate a new lua file and load in into your game you'll have to do a little manual labour:

1. In `convert.py` change the settings at the top of the file
    * `image_file`: the name of the image to use (to be placed next to the `convert.py` file)
    * `resize_width`: the size you want the final map to be (can be set to `None` if you just want the same size as the provided image)
    * `terrain_codes`: set which colours are what terrains **!!DANGER!!** If you change these, you'll have to update the `terrain_codes` in `control.lua` as well
2. Run `convert.py`
3. Copy the created lua files (`World_large.lua` and `World_small.lua`) into the mod's root folder
4. Run the game and start a new game
