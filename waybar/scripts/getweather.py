#!/usr/bin/env python3
import requests
import sys

HELP_MESSAGE ='''Usage: ./getweather.py CITY [LANGUAGE] [OPTION...]
Get a simple weather forecast for your city.

  -h, --help    show this message
  
Language:
  PT            show the message in Portuguese(default)
  EN            show the message in English

Options:
  -v            increase message verbosity
  -q            decrease message verbosity

For now the only cities that are supported are portuguese cities,
the major ones as listed in the IPMA website.
If you want to use the program, don't use the help flags.
More flags to come in the feature I guess, idk what I could whant'''
LANGUAGUES = ('PT','EN')
VERBOSITY = ('-v', '-q')
defaultLang = 'EN'
defaultVerbosity = 1

#--get arguments--#
args = sys.argv[1:]
if len(args) < 1 or '--help' in args or '-h' in args:
    print(HELP_MESSAGE)
    exit()

verbosity = defaultVerbosity + args.count('-v') - args.count('-q')

CITY = args[0]
if len(args) > 1 and args[1] in LANGUAGUES:
    defaultLang = args[1]

def get_desc(url, key, value, desc_field):
    data = requests.get(url).json()['data']
    for item in data:
        if str(item[key]) == str(value):
            return item[f'{desc_field}{defaultLang}']
    return None

cityCodes = requests.get('https://api.ipma.pt/open-data/distrits-islands.json')
cityJson = cityCodes.json()
for zone in cityJson['data']:
    if zone['local'] == CITY:
        zoneNumber = zone['globalIdLocal']
        break

weatherToday = requests.get('https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/hp-daily-forecast-day0')
weatherJson = weatherToday.json()
for zone in weatherJson['data']:
    if zone['globalIdLocal'] == zoneNumber:
        weather = zone
        break

tMax = weather['tMax']
tMin = weather['tMin']
windDir = weather['predWindDir']
windStr = weather['classWindSpeed']
weatherType = weather['idWeatherType']
precProb = weather['precipitaProb']
try:
    precInt = weather['classPrecInt']
except KeyError:
    precInt = 0

weatherDesc = get_desc('https://api.ipma.pt/open-data/weather-type-classe.json', 'idWeatherType', weatherType, 'descWeatherType')
wind = get_desc('https://api.ipma.pt/open-data/wind-speed-daily-classe.json', 'classWindSpeed', windStr, 'descClassWindSpeedDaily')
prec = get_desc('https://api.ipma.pt/open-data/precipitation-classe.json', 'classPrecInt', precInt, 'descClassPrecInt')

if verbosity  <= 1:
    print(f'{tMin}-{tMax}ºC: {weatherDesc.lower()}') 
elif verbosity > 1:
    windDesc = f'{wind.lower()} wind {windDir}' if defaultLang == 'EN' else f'vento {wind.lower()} {windDir}'
    print(f'{tMin}-{tMax}ºC: {weatherDesc.lower()} - {windDesc}')
