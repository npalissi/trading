from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

promp_system = promp = """	Tu es un expert en analyse macroéconomique et en trading Forex. 
	Ton rôle est d'analyser les annonces économiques (indicateurs, décisions de banques centrales, événements géopolitiques, etc.) 
	et de prédire leurs impacts sur les paires de devises du pays concerné.
	tu dois donner les paires qui vont être impactées par l'annonce si elles vont monter ou descendre avec des flèches
	et une explication de ton raisonnement. tu vas avoir un multitude d'annonce et tu dois les analyser une par une.
	les annonces les plus ressentes sont les plus importantes et tu dois les analyser en premier.
	tu dois faire un rapport en lier toute les annonces entre elles et en expliquant les impacts de chaque annonce sur le marché.
	les annonces sont en anglais mais tu dois repondre en français.
	Réponds toujours en texte brut, sans aucun formatage (pas de markdown, italique, gras, listes, etc.)
	les annonces sont sous le format suivant :
	- titre de l'annonce
	- description de l'annonce
	- temps en minute depuis l'annonce
	puis les annonces sont separer par des tirets"""

def create_prompt(table):
	
	promp_usr = "voici les annonces des 5 dernier jours\n"
	for key in table:
		# print(table[key])
		promp_usr += "------------------------------------\n"
		promp_usr += f" - titre : {table[key]['title']}\n - description : {table[key]['desc']}\n - temps : {table[key]['time_in_min']} mins\n"
	return ([
		{"role" : "system", "content" : promp_system},
		{"role" : "user", "content" : promp_usr}
	])

def save_rapport(promps, rapport):
	date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	file_name = f"rapport_{date_now}.json"
	with open(file_name, "w") as file:
		file.write(json.dumps({"prompt" : {"user" : promps[1]['content'], "system" : promps[0]['content']}, "rapport" : rapport}, indent=4))

def get_rapport(table):
	message = create_prompt(table)
	# print("prompt creer avec succes")
	client = OpenAI(
		base_url="https://api.deepseek.com/v1", 
		api_key=os.getenv("API_KEY"), 
	)
	response = client.chat.completions.create(
		model="deepseek-chat",  
		messages=message,
		temperature=0.7,
		stream=False,
	)
	rapport = response.choices[0].message.content
	print(rapport)
	save_rapport(message, rapport)
	print("rapport sauvegarder avec succes")
	return (rapport)
	