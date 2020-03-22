# JSON pulled from https://pomber.github.io/covid19/timeseries.json
import json
import os
import math
import requests

# timeseries = json.loads(open("timeseries.json","r").read())
timeseries = json.loads(requests.get("https://pomber.github.io/covid19/timeseries.json").content)

caseTotals = {}
for country in timeseries:
    for day in timeseries[country]:
        if (not day["date"] in caseTotals):
            caseTotals.update({day["date"] : day["confirmed"]})
        else:
            caseTotals[day["date"]] += day["confirmed"]


# print (caseTotals)
dates = caseTotals.keys()
cases = caseTotals.values()
dateRange = []
for i in range(len(dates)):
    dateRange.append(i)

try:
    import matplotlib.pyplot as plt
except:
    print("\tIt doesn't look like you have matplotlib installed!\n\tYou can install it using \"pip3 install matplotlib\"")
    quit()

axesSettings = [.135,.135,.8,.8]

fig = plt.figure()
ax = fig.add_axes(axesSettings)
ax.scatter(dateRange, cases)
ax.set_xlabel("Days since January 22nd")
ax.set_ylabel("Number of Cases")
# plt.suptitle('Number of occurances by code fragement (10% of values)', fontsize = 12)
ax.set_title("Number of cases over time")
# plt.show()
plt.savefig("covid")
plt.close(fig)
