# Import statements:
import json
from commonfloor import ScrapeCommonfloorListing

# Reading url queries:
with open("url_queries.json") as url_queries_file:
    url_queries = json.load(url_queries_file)

