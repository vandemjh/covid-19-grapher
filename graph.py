# JSON pulled from https://pomber.github.io/covid19/timeseries.json
import json
import os
import math
import requests
import datetime
from utils import *

""" CONSTANTS """
# Axis settings for matplotlib images
AXIS_SETTINGS = [0.167, 0.167, 0.7, 0.7]
# Countries to display in table on main page
NUM_COUNTRIES_TO_DISPLAY = 5

# timeseries = json.loads(open("timeseries.json","r").read())
timeseries = json.loads(
    requests.get("https://pomber.github.io/covid19/timeseries.json").content
)

caseTotals = getTotalCasesByDay(timeseries)


try:
    import matplotlib.pyplot as plt
except:
    print(
        '\tIt doesn\'t look like you have matplotlib installed!\n\tYou can install it using "pip3 install matplotlib"'
    )
    quit()


def createScatter(dates, cases, country, fileName):

    fig = plt.figure()
    ax = fig.add_axes(AXIS_SETTINGS)
    ax.scatter(list(range(len(dates))), list(cases))
    ax.set_xlabel("Dates")
    ax.set_ylabel("Number of Cases")

    plt.xticks(range(len(dates)), skipOver(list(dates), 3), size="small", rotation="45")
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    # plt.suptitle('Number of occurances by code fragement (10% of values)', fontsize = 12)
    dateTime = datetime.datetime.today()
    ax.set_title(
        "Number of cases in "
        + country
        + " as of "
        + str(dateTime.month)
        + "-"
        + str(dateTime.day)
        + " @ "
        + str(dateTime.hour if dateTime.hour < 12 else dateTime.hour - 12) + (" AM" if dateTime.hour < 12 else " PM")

    )
    # plt.show()
    plt.savefig(fileName)
    plt.close(fig)


createScatter(caseTotals.keys(), caseTotals.values(), "total", "covid")
# print(getCountriesInfectedTotals(timeseries)["Norway"])

table = ""
dropdown = ""
# Updates the Most Infected table
mostInfected = getTopCountriesInfected(timeseries, NUM_COUNTRIES_TO_DISPLAY)
count = 0
# <a class="dropdown-item" href="countries/">Action</a>
# <a class="dropdown-item" href="countries/">Another action</a>
for country in mostInfected:
    countryCases = getCasesForCountry(timeseries, country)
    createScatter(
        countryCases.keys(),
        countryCases.values(),
        country,
        "countries/" + country.lower(),
    )
    dropdown += (
        '<a class="dropdown-item" href="countries/'
        + country.lower()
        + ".png"
        + '">'
        + country
        + "</a>"
    )
    count += 1
    table += "<tr><td>" + str(count) + "</td>"
    table += "<td>" + country + "</td>"
    table += "<td>" + str(mostInfected[country]) + "</td></tr>"

with open("index.html", "r") as html:
    index = str(html.read())
with open("index.html", "w") as html:
    startTable = index.find("<!-- TABLE_DATA_START_HERE -->") + len(
        "<!-- TABLE_DATA_START_HERE -->"
    )
    endTable = index.find("<!-- TABLE_DATA_END_HERE -->")
    html.write(index[0:startTable] + "\n" + table + "\n" + index[endTable : len(index)])

with open("index.html", "r") as html:
    index = str(html.read())
with open("index.html", "w") as html:
    startDropdown = index.find("<!-- DROPDOWN_DATA_START_HERE -->") + len(
        "<!-- DROPDOWN_DATA_START_HERE -->"
    )
    endDropdown = index.find("<!-- DROPDOWN_DATA_END_HERE -->")
    html.write(
        index[0:startDropdown]
        + "\n"
        + dropdown
        + "\n"
        + index[endDropdown : len(index)]
    )


casesByCountry = getCasesByCountry(timeseries)
fig = plt.figure()
ax = fig.add_axes(AXIS_SETTINGS)

for country in casesByCountry:
    if country in mostInfected:
        dates = list(casesByCountry[country].keys())
        cases = list(casesByCountry[country].values())
        ax.plot(range(len(dates)), cases, label=country)

plt.legend(loc="upper left")
ax.set_xlabel("Dates")
ax.set_ylabel("Number of Cases")
plt.xticks(range(len(dates)), skipOver(list(dates), 3), size="small", rotation="45")
dateTime = datetime.datetime.today()
ax.set_title("Cases in top " + str(NUM_COUNTRIES_TO_DISPLAY) + " Infected Countries")
plt.savefig("top")
plt.close(fig)
