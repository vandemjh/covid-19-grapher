
def skipOver(dates, skipSize):
    toReturn = []
    for date in list(dates):
        if (list(dates).index(date) % skipSize == 0):
            toReturn.append(date[5:len(date)])
        else:
            toReturn.append("")
    return toReturn

# Returns the total cases per day as { "date" : total cases on that date }
def getTotalCasesByDay(timeseries):
    caseTotals = {}
    for country in timeseries:
        for day in timeseries[country]:
            if (not day["date"] in caseTotals):
                caseTotals.update({day["date"] : day["confirmed"]})
            else:
                caseTotals[day["date"]] += day["confirmed"]
    return caseTotals

# Returns the total cases per day for numberOfCountries as { country : [ "date" : total cases on that date ] }
def getTopCasesByCountry(timeseries, numberOfCountries):
    toReturn = {}
    for country in timeseries:
        for day in timeseries[country]:
            if (not day["date"] in toReturn):
                toReturn.update({day["date"] : day["confirmed"]})
            else:
                toReturn[day["date"]] += day["confirmed"]
    return toReturn

# Returns countries as { country : number of cases }
def getCountriesInfectedTotals(timeseries):
    toReturn = {}
    for country in timeseries:
        for day in timeseries[country]:
            if (not country in toReturn):
                toReturn.update({country : day["confirmed"]})
            else:
                toReturn[country] += day["confirmed"]
    return toReturn

# Returns top maxCountries most infected countries as { country : number of cases }
def getTopCountriesInfected(timeseries, maxCountries):
    toReturn = {}
    toPop = getCountriesInfectedTotals(timeseries)
    for i in range(maxCountries):
        nextTop = (max(toPop, key=toPop.get))
        numInfected = toPop[nextTop]
        toReturn.update({nextTop : toPop.pop(nextTop)})
    return toReturn
