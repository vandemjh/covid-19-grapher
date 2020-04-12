import datetime

# Inserts 'what' between startString and endString in file, replacing whatever is there
def findAndReplace(file, what, startString, endString):
    with open(file, "r") as toRead:
        index = str(toRead.read())
    with open(file, "w") as toWrite:
        start = index.find(startString) + len(startString)
        end = index.find(endString)
        toWrite.write(
            index[0:start] + "\n" + str(what) + index[end : len(index)] + "\n"
        )


# Used to declutter x axis of the matplotlib plots
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


# Returns cases for country as { "date" : cases on that date }
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
            toGet = str(year) + "-" + str(month) + "-" + str(day)
            if toGet in toIterate[country]:
                toReturn.update({country: toIterate[country][toGet]})
            else:
                try:
                    toGet = getDateInStringForm(toGet, -1)
                    toReturn.update({country: toIterate[country][toGet]})
                except:  # Default to yesterdays data (time zone issues on server)
                    toGet = getDateInStringForm(toGet, -1)
                    toReturn.update({country: toIterate[country][toGet]})
    return toReturn


# Return days formatted for json (negative days are in the past)
def getDateInStringForm(startDate, daysToChange):
    sentDate = startDate.split("-")
    toCalculate = datetime.datetime(
        int(sentDate[0]), int(sentDate[1]), int(sentDate[2])
    )
    changed = toCalculate + datetime.timedelta(days=daysToChange)
    return str(changed.year) + "-" + str(changed.month) + "-" + str(changed.day)


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


# Returns the rate of change (average of dayAverage days) of all countries over all dates as { country : { "date" : average rate of change from dayAverage days ago } }
def getChangeInInfected(timeseries, dayAverage):
    if dayAverage == 0:
        return getCasesByCountry(timeseries)
    toReturn = {}
    timeseries = getCasesByCountry(timeseries)
    for country in timeseries:
        for day in timeseries[country]:
            # for i in range(dayAverage):
            end = timeseries[country][day]
            try:
                start = timeseries[country][
                    getDateInStringForm(day, -1 * dayAverage)
                ]
            except:  # Day is too far in the past
                start = 0
            if not country in toReturn:
                toReturn.update({country: {day: (end - start) / dayAverage}})
            else:
                toReturn[country].update({day: (end - start) / dayAverage})

    return toReturn
