import numpy
# import seaborn
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn import metrics

# Purely linear
def regress(xIn, yIn):
    X_train, X_test, y_train, y_test = train_test_split(numpy.array(xIn).reshape(-1,1), numpy.array(yIn), test_size=0.2, random_state=0)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
        # orderedPairs = numpy.column_stack((xIn, yIn))
        # regressor = LinearRegression()
        # regressor.fit(orderedPairs, xIn)
    # Returns as an array of arrays because there can be many coefficients
    return[regressor.coef_, regressor.intercept_]

# Returns polyfit
def multipleRegress(xIn, yIn):
    return numpy.polyfit(xIn, yIn, 5)

def predict(dates, cases, numPredictions=100):
    trend = multipleRegress(list(range(len(dates))), list(cases))
    trendpoly = numpy.poly1d(trend)
    toReturn = []
    for i in range(numPredictions):
        toReturn.append(numpy.polyval(trendpoly, i))
    return toReturn
