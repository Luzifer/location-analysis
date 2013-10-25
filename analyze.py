#!/usr/bin/env python

import json, yaml, sys
from haversine import haversine
from dataquery import DataQuery
from datetime import datetime

config = yaml.load(open('config.yaml', 'r'))
dq = DataQuery(password = config['dbpass'])
lastweek = int(datetime.now().strftime('%s')) - 86400 * 7
dataset = dq.get_data_since(starttime = lastweek)

last_location = [0.0, 0.0]

# Prepare named count environment
named_count = {}
for key in config['named_locations'].keys():
  named_count[key] = 0

# Do analysis
for timestamp in sorted(dataset.keys()):
  lat, lon = dataset[timestamp]
  location = (float(lat), float(lon))

  for nlk in config['named_locations'].keys():
    for point in config['named_locations'][nlk]['points']:
      if haversine(tuple(location), (point['lat'], point['lon'])) < (float(config['cluster_move']) / 1000.0):
        named_count[nlk] = named_count[nlk] + 1

# Print named location percentage
sum_percentages = 0.0
data_count = len(dataset.keys())
for nlk in config['named_locations'].keys():
  perc = float(named_count[nlk]) / float(data_count) * 100.0
  sum_percentages = sum_percentages + perc
  print '%.1f%% at %s' % (perc, config['named_locations'][nlk]['display_name'])
print '%.1f%% on the road' % (100.0 - sum_percentages)


'''
Kriterien:
 * Wenn laenger X an einem Ort mit dem Umkreis Y verweilt => aufenthalt
 * Bekannte Orte => Prozentuale Auswertung
'''


