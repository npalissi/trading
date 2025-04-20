import requests
import json
from datetime import datetime, timezone
import zoneinfo
import time

def format_time(time):
	if (time.find(".") == -1):
		time += ".000"
	while(len(time.split(".")[-1]) != 3):
		time += "0"
	return (time)

def get_inter_time(time):
	time = format_time(time)
	pub_date = datetime.fromisoformat(time).replace(tzinfo=None)
	now_data = datetime.now()
	time_diff = now_data - pub_date
	diff_minutes = int(time_diff.total_seconds() // 60) - 120
	return (diff_minutes)

url = "https://tradingeconomics.com/ws/stream.ashx"


headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# print(json.dumps(data, indent=4))
def sort_table_new(country):
	table_sort = {}
	params = {
	"start": 0,
	"size": 20,
	"c": country,
	}
	while(1):
		response = requests.get(url, params=params, headers=headers)
		if response.status_code != 200:
			print(f"Error: {response.status_code}")
			print(f"Response: {response.text}")
			return ({})
		data = response.json()
		for new in data:
			time = get_inter_time(new["date"])
			if (time > 24 * 60 * 2):
				return (table_sort)
			table_sort[new["ID"]] = {"title": new["title"], "desc" : new["description"], "time_in_min": time}
		params["start"] += 30
	time.sleep(1)


def get_last_news(country):
	params = {
		"start": 0,
		"size": 1,
		"c": country,
	}
	response = requests.get(url, params=params, headers=headers)
	if (response.status_code != 200):
		return (0)
	return (response.json()[0]["ID"])

			
	




