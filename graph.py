# JSON pulled from https://pomber.github.io/covid19/timeseries.json
import json
import os
import math
import requests
import datetime
import numpy
from PIL import Image
from utils import *
from predict import *

""" CONSTANTS """
# Axis settings for matplotlib images
AXIS_SETTINGS = [0.167, 0.167, 0.7, 0.7]
# Countries to display in table on main page
NUM_COUNTRIES_TO_DISPLAY = 8
todaysDayNumber = (datetime.date.today() - datetime.date(2020, 1, 22)).days
NUM_PREDICTIONS = 120

timeseries = json.loads(
    requests.get("https://pomber.github.io/covid19/timeseries.json").content
)

# caseTotals = getTotalCasesByDay(timeseries)
# print(regress(list(range(len(caseTotals.keys()))), list(caseTotals.values())))
# exit()


try:
    import matplotlib.pyplot as plt
except:
    print(
        '\tIt doesn\'t look like you have matplotlib installed!\n\tYou can install it using "pip3 install matplotlib"'
    )
    quit()


def createChart(
    dates,
    cases,
    country,
    fileName,
    xAxis="Dates",
    yAxis="Number of Cases",
    type="scatter",
):
    fig = plt.figure()
    ax = fig.add_axes(AXIS_SETTINGS)
    if type == "scatter":
        ax.scatter(list(range(len(dates))), list(cases))
        trend = multipleRegress(list(range(len(dates))), list(cases))
        trendpoly = numpy.poly1d(trend)
        plt.plot(
            list(range(len(dates))),
            trendpoly(list(range(len(dates)))),
            "red",
            label="Trend",
        )
        # print(numpy.polyval(trendpoly, 9))
    if type == "loglog":
        ax.loglog(list(range(len(dates))), list(cases))
    if type == "plot":
        ax.plot(list(range(len(dates))), list(cases))
    ax.set_xlabel(xAxis)
    ax.set_ylabel(yAxis)
    ax.legend()

    plt.xticks(
        range(len(dates)), skipOver(list(dates), 3), size="small", rotation="45"
    )
    dateTime = datetime.datetime.today()
    ax.set_title(
        "Number of cases in "
        + country
        + " as of "
        + str(dateTime.month)
        + "-"
        + str(dateTime.day)
        + " @ "
        + str(dateTime.hour if dateTime.hour < 12 else dateTime.hour - 11)
        + (" AM" if dateTime.hour < 12 else " PM")
        + " GMT"
    )
    plt.savefig(fileName)
    plt.close(fig)


# print(getChangeInInfected(timeseries, 20)["Norway"])
# print(getCasesForCountry(timeseries, "Norway"))


caseTotals = getTotalCasesByDay(timeseries)


# case getCasesByCountry(timeseries) For multiple countries... TODO vandemjh
# multipleRegress(list(range(len(caseTotals.keys()))), list(caseTotals.values()));

createChart(caseTotals.keys(), caseTotals.values(), "total", "covid")
# quit()

table = ""
dropdown = ""
# Updates the Most Infected table
mostInfected = getTopCountriesInfected(timeseries, NUM_COUNTRIES_TO_DISPLAY)
count = 0
for country in mostInfected:
    countryCases = getCasesForCountry(timeseries, country)
    createChart(
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

findAndReplace(
    "index.html",
    table,
    "<!-- TABLE_DATA_START_HERE -->",
    "<!-- TABLE_DATA_END_HERE -->",
)

findAndReplace(
    "index.html",
    dropdown,
    "<!-- DROPDOWN_DATA_START_HERE -->",
    "<!-- DROPDOWN_DATA_END_HERE -->",
)

""" Linear Regression """
pred = predict(
    list(range(len(caseTotals.keys()))),
    list(caseTotals.values()),
    numPredictions=NUM_PREDICTIONS,
)

findAndReplace(
    "index.html",
    "\nconst tomorrow = "
    + str(todaysDayNumber + 1)
    + "\nconst today = tomorrow - 1"
    + ";\nconst predictions = "
    + str(pred)
    + "; \n",
    "<!-- PREDICTION_DATA_START_HERE -->",
    "// <!-- PREDICTION_DATA_STOP_HERE -->",
)


findAndReplace(
    "index.html",
    "{:,.0f}".format(round(max(pred)))
    + " People infected on "
    + str(
        datetime.timedelta(days=(pred.index(max(pred)) - todaysDayNumber))
        + datetime.date.today()
    ),
    "<!-- EXPECTED_PEAK_START -->",
    "<!-- EXPECTED_PEAK_STOP -->",
)

# print((max(pred)))
clear = None
try:
    for i in range(pred.index(max(pred))):
        if pred[pred.index(max(pred)) + i] <= 0:
            clear = pred.index(pred[pred.index(max(pred)) + i]) + pred.index(
                max(pred)
            )
            break
except:
    None
# print(clear)
findAndReplace(
    "index.html",
    "The model is currently unable to accurately predict an end to the outbreak.  Maybe check back tomorrow."
    if clear is None
    else str(
        datetime.timedelta(days=(clear - todaysDayNumber))
        + datetime.date.today()
    ),
    "<!-- EXPECTED_END_START -->",
    "<!-- EXPECTED_END_STOP -->",
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
plt.xticks(
    range(len(dates)), skipOver(list(dates), 3), size="small", rotation="45"
)
dateTime = datetime.datetime.today()
ax.set_title(
    "Cases in top " + str(NUM_COUNTRIES_TO_DISPLAY) + " Infected Countries"
)
plt.savefig("top")
plt.close(fig)

# Function to loop through when creating gif
def createRateOfChangeGraph(fileName, step):
    rateOfChangeOfCasesByCountry = getChangeInInfected(timeseries, step)
    fig = plt.figure()
    ax = fig.add_axes(AXIS_SETTINGS)
    for country in rateOfChangeOfCasesByCountry:
        if country in mostInfected:
            dates = list(rateOfChangeOfCasesByCountry[country].keys())
            cases = list(rateOfChangeOfCasesByCountry[country].values())
            ax.plot(range(len(dates)), cases, label=country)

    plt.legend(loc="upper left")
    ax.set_xlabel("Dates")
    ax.set_ylabel("Rate of change of cases")
    plt.xticks(
        range(len(dates)), skipOver(list(dates), 3), size="small", rotation="45"
    )
    dateTime = datetime.datetime.today()
    ax.set_title(
        "Rate of change of top "
        + str(NUM_COUNTRIES_TO_DISPLAY)
        + " Infected Countries (average of "
        + str(step)
        + " days)"
    )
    plt.savefig(fileName + str(step))
    plt.close(fig)
    return fileName + str(step) + ".png"


toGifify = []
for i in range(6):
    file = Image.open(createRateOfChangeGraph("change/change", i + 1))
    toGifify.append(file)
toGifify[0].save(
    "change.gif",
    save_all=True,
    append_images=toGifify[1:],
    duration=600,
    loop=0,
)
# for img in toGifify:
#     print((img.verify()))
