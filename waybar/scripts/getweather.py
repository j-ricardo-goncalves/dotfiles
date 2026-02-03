#!/bin/python
# NEEDS MASSIVE IMPROVEMENTS BUT IT WORKS, YIPPIE
# To do next:
# Get wind str
# Get precInt meaning
# Argument functionality in the terminal
# More things, the sky is the limit
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
If you want to use the program, don't use the help flags.'''
LANGUAGUES = ('PT','EN')
defaultLang = 'EN'
import requests
import sys

args = sys.argv[1:]
if len(args) < 1 or '--help' in args or '-h' in args:
    print(HELP_MESSAGE)
    exit()

CITY = args[0]
if args[1] in LANGUAGUES:
    defaultLang = args[1]

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

# could let it be but for now its more comprehensible this way
tMax = weather['tMax']
tMin = weather['tMin']
windDir = weather['predWindDir']
windStr = weather['classWindSpeed']
weatherType = weather['idWeatherType']
precProb = weather['precipitaProb']
precInt = weather['classPrecInt']

weatherTypeCodes = requests.get('https://api.ipma.pt/open-data/weather-type-classe.json')
typeJson = weatherTypeCodes.json()
for i in typeJson['data']:
    if i['idWeatherType'] == weatherType:
        info = i[f'descWeatherType{defaultLang}']

print(f"{tMin}-{tMax}ºC: {info}")
