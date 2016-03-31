#!/usr/bin/env python
import fitbit
import checkTokens

#This is the Fitbit URL to use for the API call
FitbitURL = "https://api.fitbit.com/1/user/-/profile.json"

#Declare these global variables that we'll use for the access and refresh tokens
AccessToken = ""
RefreshToken = ""

APICallOK = False
attempts = 0
try:
	while not APICallOK:
		#Make the API call
		AccessToken, RefreshToken = checkTokens.ReadTokens()
		APICallOK, APIResponse = checkTokens.MakeAPICall(FitbitURL, AccessToken, RefreshToken)
		
		attempts += 1
		if attempts > 4:
			raise ValueError("Stopping after 5 failed attempts.")
			break
	
	#Create authorised client and grab step count from one day of steps
	authd_client = fitbit.Fitbit(checkTokens.consumer_key, checkTokens.consumer_secret, oauth2=True, access_token=AccessToken, refresh_token=RefreshToken)
	timeSeriesSteps = authd_client.time_series('activities/steps',period='1d')
	print "steps: " + timeSeriesSteps['activities-steps'][0]['value']
except ValueError as err:
	print err