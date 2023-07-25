from http.server import BaseHTTPRequestHandler
import json
from urllib import parse
import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup


class handler(BaseHTTPRequestHandler):
    def search(self, query):
        # Replace with your subscription key.
        subscription_key = os.environ.get('BINGSEARCH_API')
        # endpoint = os.environ.get('BINGSEARCH_ENDPOINT')
        endpoint = "https://api.bing.microsoft.com/v7.0/search"

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
            return search_results["webPages"]["value"][0:3]
        except Exception as ex:
            raise ex
            
    def web_scrape(self, url):
        # do something
        # url = "https://www.fairprice.com.sg/product/kinder-bueno-chocolate-wafer-bar-milk-43g-303793"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # class that corresponds to the product description in the webpage
        results = soup.find_all("div", class_="sc-10zw1uf-16 kZweZH")
        # results_soup = BeautifulSoup(results, "html.parser")
        # class that corresponds to ingreident list
        # ingredients = soup.find("h2", title="Ingredients")
        div_elements = soup.find_all("div", class_="sc-3zvnd-0 bCYQcy")
        # Loop through the div elements to find the one containing the h2 with "Ingredients"
        target_div = None
        for div_element in div_elements:
            h2_element = div_element.find("h2", title="Ingredients")
            if h2_element:
                target_div = div_element
                break
        if target_div != None:
            formatted_target_div = target_div.prettify()
            return formatted_target_div
        else:
            return "No details"

    def do_GET(self):
        print("init")
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if "query" in dic:
            # construct search query to narrow options to singapore supermarkets only
            # ensure that search results url's include fairprice website and at the product details page
            query = str(dic["query"])
            search_query = "site:https://www.fairprice.com.sg/product " + query
            results = self.search(search_query)
            formatted_results = ""
            for result in results:
                ingredients = self.web_scrape(result["url"])
                formatted_results += "Name: " + result["name"] + "\nIngredients in HTML form:\n" + ingredients + "\nURL to product details: " + result["url"] + "\n\n"
            # final format should be "Products available: " + list of product information
            message = {"results":  formatted_results}
        else:
            message = {"results":  "Enter a query"}
        
        response_json = json.dumps(message)
        self.wfile.write(response_json.encode())  # Encode the JSON response