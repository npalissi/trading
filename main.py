import request_api
import scraping
import requests
from request_api import get_rapport
from config import table_country, edit_table_country
import time


def start(id):
	table = scraping.sort_table_new(table_country[id]["country"])
	if (len(table) == 0):
		print(f"{id} Aucune news recuperer")
		return
	print(f"{id} : annonce recuperer avec succes : {len(table)}")
	promp = get_rapport(table, id )
	params = {
		"chat_id": "-1002502518878",
		"text": promp,
		"message_thread_id" : table_country[id]["chanelid"],
	}
	response = requests.get("https://api.telegram.org/bot7329383527:AAEXfN9pe2eVsVL9S9xjB_Ke7AkDekmClmk/sendMessage?", params=params)

	if response.status_code == 200:
		print("Message sent successfully")
	print(response.text)


def run_run_periodically(interval_minutes):
	while(True):
		for country in table_country:
			last = scraping.get_last_news(table_country[country]["country"])
			if table_country[country]["last"] == last:
				print(f"{country} pas de nouvelle annonce")
				continue
			start(country)
			edit_table_country(country, last)
			print(f"{country} derniere annnonce sauvegarder : {last}")
		time.sleep(interval_minutes * 60)

run_run_periodically(10)