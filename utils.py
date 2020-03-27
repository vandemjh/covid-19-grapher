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
            toGet = (
                str(dateTime.year) + "-" + str(dateTime.month) + "-" + str(dateTime.day)
            )
            if toGet in toIterate[country]:
                toReturn.update({country: toIterate[country][toGet]})
            else:
                day = dateTime.day - 1
                month = dateTime.month
                year = dateTime.year
                try:
                    toGet = (
                        str(year if day > 0 and month > 0 else year - 1)
                        + "-"
                        + str(month if day > 0 else month - 1)
                        + "-"
                        + str(day if day > 0 else 1)
                    )
                    toReturn.update({country: toIterate[country][toGet]})
                except:  # Default to yesterdays data
                    toReturn.update({country: toIterate[country][toGet]})
    # for country in toIterate:
    #     for day in toIterate[country]:
    #         if (not country in toReturn):
    #             toReturn.update({country : toIterate[country][day]})
    #         else:
    #             toReturn[country] += toIterate[country][day]
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
