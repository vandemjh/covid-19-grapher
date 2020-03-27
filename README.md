# COVID 19 Fatality/New Case Predictor
https://vandemjh.github.io/covid-19-grapher/

Using past trends, this COVID-19 grapher predicts how many fatalities are expected on a day, for a certain time, and total fatality count.

## Action Status
![Python application](https://github.com/vandemjh/covid-19-grapher/workflows/Python%20application/badge.svg?branch=master)
![Formatted](https://github.com/vandemjh/covid-19-grapher/workflows/.github/workflows/format.yml/badge.svg)

## To Do
* Put estimated fatalities not just cases over time
* Calcualte rate of growth at that certain time
* Allow user to input time, have valid ranges (before 1-22, or before first reported case, after current date, which is date of graph), just correspond to y axis (number of cases), if in the future, input x into rate of growth based on time calculated by time from now
* Add style sheet to make custom bootstrap
# More Suggestions (3/25)
* Use a script to change order of country by which one has more death
* Change the output of pygraph that says from from 6:7, say 6-7PM EST, also put weekday and enumate country as well so people from other countries don't get confused
## Requirements
* As a public health official, I want to be able to estimate how many new cases/fatalities of COVID-19 I should expected that way I can better prepare to treat an influx of patients.
* As a government official, I want to guage the potential loss due to COVID-19 so I can develop policies accordingly.
* As a user, I want to be able to see estimated cases by day, week, and month, so I can get a broader gauge of these numbers.
* As a user, I want to be able to see estimated new cases up until a day, so I can get a guage of the total impact of COVID-19.
* As a user, I want to look at regional estimates, so I can understand the disease in my area.

## Limitations To Consider
* Underreporting of cases
* Lack of Testing
* Need to update from data continously

