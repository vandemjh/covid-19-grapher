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
dates = caseTotals.keys()
cases = caseTotals.values()
dateRange = []
for i in range(len(dates)):
    dateRange.append(i)

try:
    import matplotlib.pyplot as plt
except:
    print("\tIt doesn't look like you have matplotlib installed!\n\tThat's fine, the results of the scrape are exported to file.\n\tYou can also install it using \"pip3 install matplotlib\"")
    quit()

axesSettings = [.11,.11,.8,.8]

fig = plt.figure()
ax = fig.add_axes(axesSettings)
ax.scatter(dateRange, cases)
ax.set_xlabel("Dates")
ax.set_ylabel("Number of Cases")
# plt.suptitle('Number of occurances by code fragement (10% of values)', fontsize = 12)
ax.set_title("Number of cases by date")
# plt.show()
plt.savefig("covid")
plt.close(fig)
