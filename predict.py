import numpy

# import seaborn
# import pandas
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn import metrics


def regress(xIn, yIn):
    # print(numpy.array(xIn).reshape(-1, 1))
    X_train, X_test, y_train, y_test = train_test_split(
        numpy.array(xIn).reshape(-1, 1),
        numpy.array(yIn),
        test_size=0.2,
        random_state=0,
    )
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    # orderedPairs = numpy.column_stack((xIn, yIn))
    # regressor = LinearRegression()
    # regressor.fit(orderedPairs, xIn)
    # Returns as an array of arrays because there can be many coefficients
    # coeff_df = pandas.DataFrame(regressor.coef_, xIn.columns, columns=['Coefficient'])
    # coeff_df
    return [regressor.coef_, regressor.intercept_]


# Returns polyfit
def multipleRegress(xIn, yIn):
    return numpy.polyfit(xIn, yIn, 5)


def predict(dates, cases, numPredictions=100):
    trend = multipleRegress(list(range(len(dates))), list(cases))
    trendpoly = numpy.poly1d(trend)
    toReturn = []
    for i in range(numPredictions + 1):
        toReturn.append(
            0
            if numpy.polyval(trendpoly, i) < 0
            else numpy.polyval(trendpoly, i)
        )
    return toReturn


# def dateArray()
