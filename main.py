import request_api
import scraping


table = scraping.sort_table_new()
print(f"annonce recuperer avec succes : {len(table)}")
promp = request_api.get_rapport(table)
print(promp)
