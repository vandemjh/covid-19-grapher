# JSON pulled from https://pomber.github.io/covid19/timeseries.json
import json
import os
import math
import requests
import datetime
from utils import *

# timeseries = json.loads(open("timeseries.json","r").read())
timeseries = json.loads(requests.get("https://pomber.github.io/covid19/timeseries.json").content)

numberOfCountries = 5
caseTotals = getTotalCasesByDay(timeseries)
# toPrint = (getCountriesInfectedTotals(timeseries))
# print(getTopCountriesInfected(timeseries, 5))
# exit()

# print (caseTotals)


try:
    import matplotlib.pyplot as plt
except:
    print("\tIt doesn't look like you have matplotlib installed!\n\tYou can install it using \"pip3 install matplotlib\"")
    quit()


def createScatter(dates, cases, country, fileName):
    axesSettings = [.167,.167,.7,.7]

    fig = plt.figure()
    ax = fig.add_axes(axesSettings)
    ax.scatter(range(len(dates)), cases)
    ax.set_xlabel("Dates")
    ax.set_ylabel("Number of Cases")

    plt.xticks(range(len(dates)), skipOver(list(dates), 3), size="small", rotation="45")
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    # plt.suptitle('Number of occurances by code fragement (10% of values)', fontsize = 12)
    dateTime = datetime.datetime.today()
    ax.set_title("Number of cases in " + country + " as of " + str(dateTime.month) + "-" + str(dateTime.day) + " @ " + str(dateTime.hour) + ":" + (str(dateTime.minute)))
    # plt.show()
    plt.savefig(fileName)
    plt.close(fig)

createScatter(caseTotals.keys(), caseTotals.values(), "total", "covid")
print(getCasesByCountry(timeseries)["Norway"])
print(getCountriesInfectedTotals(timeseries)["Norway"])
    # print (country)
