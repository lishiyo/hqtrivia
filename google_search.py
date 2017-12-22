import pprint
from googleapiclient.discovery import build

# load config
import json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

CUSTOM_SEARCH_API_KEY = data["GOOGLE"]["CUSTOM_SEARCH_API_KEY"]
CUSTOM_SEARCH_ENGINE_ID = data["GOOGLE"]["CUSTOM_SEARCH_ENGINE_ID"]

def run_query_all(question, answers):
    """
    Returns array of tuples with the query and total num of search results for it 
    """
    results = []
    for answer in answers:
        if (answer.startswith('"')):
            query = question + " " + answer
        else:
            query = question + ' "' + answer + '"'
        results.append((answer, search(query)))
    return (question, results)

def search(query):
    service = build("customsearch", "v1", developerKey=CUSTOM_SEARCH_API_KEY)
    res = service.cse().list(
        q=query,
        cx=CUSTOM_SEARCH_ENGINE_ID,
    ).execute()
    return res['searchInformation']['formattedTotalResults']

if __name__ == '__main__':
    search('lectures')
