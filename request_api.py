from openai import OpenAI
from openai import OpenAIError

from dotenv import load_dotenv
from datetime import datetime
import os
import json
from config import table_country

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
	je veux que tu fasse une reponse avec le format suivant a exctement comme ca 
	- payes impacté (nom de paire)
	- 1 . titre de l'annonce
		impacte sur les paire
		reson
	puis faire sur les annonces les plus impactantes
	- conclusion
	    impacte final sur les paires en disant le direction + un fleche
        exmple : xxx/xxx ↑ (hausse ....)
	voici les annonces sont separer par des tirets"""

def create_prompt(table, state):
	
	promp_usr = f"voici les annonces des 5 dernier jours des{state}\n"
	for key in table:
		# print(table[key])
		promp_usr += "------------------------------------\n"
		promp_usr += f" - titre : {table[key]['title']}\n - description : {table[key]['desc']}\n - temps : {table[key]['time_in_min']} mins\n"
	return ([
		{"role" : "system", "content" : promp_system},
		{"role" : "user", "content" : promp_usr}
	])

import os

def save_rapport(promps, rapport, id):
    date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"report/{id}/rapport_{date_now}.json"
    
    # Création du dossier si nécessaire
    os.makedirs(f"report/{id}", exist_ok=True)
    
    # Écriture du rapport dans le fichier JSON
    with open(file_name, "w") as file:
        file.write(json.dumps({"prompt": {"user": promps[1]['content'], "system": promps[0]['content']}, "rapport": rapport}, indent=4))

def get_rapport(table, id):
    try:
        # Création du prompt
        message = create_prompt(table, table_country[id]["country"])
        
        # Initialisation du client OpenAI
        client = OpenAI(
            base_url="https://api.deepseek.com/v1", 
            api_key=os.getenv("API_KEY"), 
        )
        
        # Appel à l'API OpenAI
        response = client.chat.completions.create(
            model="deepseek-chat",  
            messages=message,
            temperature=0.7,
            stream=False,
        )
        
        # Extraction du contenu du rapport
        rapport = response.choices[0].message.content
        
        # Sauvegarde du rapport
        save_rapport(message, rapport, id)
        print("Rapport sauvegardé avec succès")
        return rapport

    except KeyError as e:
        print(f"Erreur : Clé manquante dans table_country ou table : {e}")
        return "Erreur : Clé manquante dans les données."

    except OpenAIError as e:
        print(f"Erreur avec l'API OpenAI : {e}")
        return "Erreur : Impossible de générer le rapport avec l'API OpenAI."

    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau lors de l'appel à l'API OpenAI : {e}")
        return "Erreur : Problème de connexion réseau."

    except Exception as e:
        print(f"Erreur inattendue dans get_rapport : {e}")
        return "Erreur : Une erreur inattendue est survenue."