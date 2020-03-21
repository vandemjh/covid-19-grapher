# JSON pulled from https://pomber.github.io/covid19/timeseries.json
import json
import os
import math

timeseries = json.loads(open("timeseries.json","r").read())

caseTotals = {}
for country in timeseries:
    for day in timeseries[country]:
        if (not day["date"] in caseTotals):
            caseTotals.update({day["date"] : day["confirmed"]})
        else:
            caseTotals[day["date"]] += day["confirmed"]


print (caseTotals)

try:
    import matplotlib.pyplot as plt
except:
    print("\tIt doesn't look like you have matplotlib installed!\n\tThat's fine, the results of the scrape are exported to file.\n\tYou can also install it using \"pip3 install matplotlib\"")
    quit()
