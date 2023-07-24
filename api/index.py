from http.server import BaseHTTPRequestHandler
import json
from urllib import parse
import os
from pprint import pprint
import requests


class handler(BaseHTTPRequestHandler):
    def search(self, query):
        # Replace with your subscription key.
        subscription_key = os.environ.get('BINGSEARCH_API')
        # endpoint = os.environ.get('BINGSEARCH_ENDPOINT')
        endpoint = "https://api.bing.microsoft.com/v7.0/search"

        print(subscription_key)
        print(endpoint)

        # Construct a request
        mkt = 'en-US'
        params = { 'q': query, 'mkt': mkt }
        headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
        # Call the API
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()

            # print("Headers:")
            # print(response.headers)

            # print("JSON Response:")
            # pprint(response.json())

            # can modify number of search results to return based on the speed of web scraping
            return search_results["webPages"]["value"][0:4]
        except Exception as ex:
            raise ex
            
    def web_scrape(self, results):
        # do something
        return

    def do_GET(self):
        print("init")
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if "query" in dic:
            # construct search query to narrow options to singapore supermarkets only
            search_query = "ntuc fairprice" + dic["query"] 
            results = self.search(search_query)
            for result in results:
                print(result["name"])
                print(result["url"])

            # final format should be "Products available: " + list of product information
            message = {"results":  results[0]["name"]}
        else:
            message = {"results":  "Enter a query"}
        
        response_json = json.dumps(message)
        self.wfile.write(response_json.encode())  # Encode the JSON response