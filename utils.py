import datetime


def skipOver(dates, skipSize):
    toReturn = []
    for date in list(dates):
        if list(dates).index(date) % skipSize == 0:
            toReturn.append(date[5 : len(date)])
        else:
            toReturn.append("")
    return toReturn


# Returns the total cases per day as { "date" : total cases on that date }
def getTotalCasesByDay(timeseries):
    caseTotals = {}
    for country in timeseries:
        for day in timeseries[country]:
            if not day["date"] in caseTotals:
                caseTotals.update({day["date"]: day["confirmed"]})
            else:
                caseTotals[day["date"]] += day["confirmed"]
    return caseTotals


# Returns the total cases per day for numberOfCountries as { country : { "date" : total cases on that date } }
def getCasesByCountry(timeseries):
    toReturn = {}
    for country in timeseries:
        for day in timeseries[country]:
            if not country in toReturn:
                toReturn.update({country: {day["date"]: day["confirmed"]}})
            else:  # (not day["date"] in toReturn[country]):
                toReturn[country].update({day["date"]: day["confirmed"]})
            # else:
            # toReturn[country[day["date"]]] += day["confirmed"]
    return toReturn


def getCasesForCountry(timeseries, country):
    return getCasesByCountry(timeseries)[country]


# Returns countries as { country : number of cases }
def getCountriesInfectedTotals(timeseries):
    toReturn = {}
    toIterate = getCasesByCountry(timeseries)
    dateTime = datetime.datetime.today()
    for country in toIterate:
        if not country in toReturn:
            day = dateTime.day
            month = dateTime.month
            year = dateTime.year
            toGet = (
                str(year) + "-" + str(month) + "-" + str(day)
            )
            if toGet in toIterate[country]:
                toReturn.update({country: toIterate[country][toGet]})
            else:
                try:
                    toReturn.update({country: toIterate[country][toGet]})
                except:  # Default to yesterdays data (time zone issues on server)
                    yesterday = dateTime - datetime.timedelta(days = 1)
                    toGet = (
                        str(yesterday.year)
                        + "-"
                        + str(yesterday.month)
                        + "-"
                        + str(yesterday.day)
                    )
                    toReturn.update({country: toIterate[country][toGet]})
    return toReturn


# Returns top maxCountries most infected countries as { country : number of cases }
def getTopCountriesInfected(timeseries, maxCountries):
    toReturn = {}
    toPop = getCountriesInfectedTotals(timeseries)
    for i in range(maxCountries):
        nextTop = max(toPop, key=toPop.get)
        numInfected = toPop[nextTop]
        toReturn.update({nextTop: numInfected})
        toPop.pop(nextTop)
    return toReturn
