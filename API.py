"""
This is a program for real-time quotation of FX.

"""

import requests
import json
import datetime



"""a function used to get rate via API. It returns the rate or -1 if not found"""
def get_rate(user_input):
	link = "https://www.freeforexapi.com/api/live?pairs="+user_input
	response = requests.get(link)
	result = json.loads(response.text)
	print("making response: "+ str(datetime.datetime.now()))
	if result['code'] == 200:
		return result['rates'][user_input]['rate']

	if result['code'] != 200:
		return -1

"""A function to implement cross rate calculation"""
def cross_rate(firsthalf, secondhalf):
	rate_one = get_rate("USD"+firsthalf)
	rate_two = get_rate("USD"+secondhalf)
	if rate_one < 0 or rate_two < 0:
		final_rate = -1
	else:
		final_rate = rate_two / rate_one
	return final_rate

"""get_result function. Main function to implement the get_rate process."""
def get_result(user_input):
	if user_input == '':
		return "input cannot be empty!"

	if user_input.isdigit():
		return "please input currency pair in letter"

	result = get_rate(user_input)

	firsthalf, secondhalf = user_input[:3], user_input[3:]

	if firsthalf == "USD":
		result = get_rate(user_input)

	elif secondhalf == "USD":
		result = 1/get_rate(secondhalf+firsthalf)

	else:
		result = cross_rate(firsthalf, secondhalf)


	result = round(result, 6)
	print(result)
	return result

if __name__ == '__main__':
	while True:
		print("Please enter any currency pair below or enter 'q' to quit")
		my_input = input(":")
		if my_input == 'q':
			print("Thanks for using our service. Bye!")
			break
		else:
			output = get_result(my_input)
			print(str(my_input)+": "+str(output))