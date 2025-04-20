import json

def read_in_file(fName):
	with open(fName, 'r') as f:
		data = f.read()
		return json.loads(data)

def write_to_file(fName, table):
	with open(fName, 'w') as f:
            json.dump(table, f, indent=4)

table_country = read_in_file("config.json")

def edit_table_country(id, last):
	table_country[id]["last"] = last
	write_to_file("config.json", table_country)



