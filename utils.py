
def skipOver(dates, skipSize):
    toReturn = []
    for date in list(dates):
        if (list(dates).index(date) % skipSize == 0):
            toReturn.append(date[5:len(date)])
        else:
            toReturn.append("")
    return toReturn
