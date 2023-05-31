PROVIDERS = {
    "MM": "https://www.mediamarkt.de",
    "SAT": "https://saturn.de"
}

API_PATH = "/de/data/fundgrube/api/postings"
WEB_PATH = "/de/data/fundgrube"

""""
Filtering via url params:
ouletIds=1,2,3
brands=SONY
categorieIds=CAT_DE_MM_202
"""

# Supported providers: 'MM', 'SAT'
class Provider:
    def __init__(self, identifier) -> None:
        self.identifier = identifier

    def api_url(self):
        return PROVIDERS[self.identifier] + API_PATH
    
    def web_url(self):
        return PROVIDERS[self.identifier] + WEB_PATH

from urllib.parse import urlencode
class Query:
    def __init__(self, query_opts_dict):
        defaults = {
            "limit": 100,
            "offset": 0
        }
        self.query_opts = defaults | query_opts_dict

    def build(self):
        return f"?{urlencode(self.query_opts)}"

class ResultDict:
    def __init__(self, postings) -> None:
        self.postings = postings
    
    def cheapest(self, number=1):
        self.postings.sort(key=lambda x: float(x.get('price')))
        return self.postings[:number]
    
from dataclasses import dataclass

@dataclass
class Posting:
    id: int
    text: str
    pim_id: int
    price: float
    price_old: float
    shipping_cost: float
    shipping_type: str
    name: str
    brand_id: int
    brand_name: str
    outlet_id: int
    outlet_name: str
    discount_in_percent: int
    top_level_catalog_id: str
    original_url: str
    provider: Provider

    @classmethod
    def from_params(cls, provider, posting_params):
        return cls(id = posting_params["posting_id"],
            text = posting_params["posting_text"],
            pim_id = posting_params["pim_id"],
            price = float(posting_params["price"]),
            price_old = 0 if posting_params["price_old"] == '' else float(posting_params["price_old"]),
            shipping_cost =0 if posting_params["shipping_cost"] == '' else float(posting_params["shipping_cost"]),
            shipping_type = posting_params["shipping_type"],
            name =  posting_params["name"],
            brand_id = posting_params["brand"]["id"],
            brand_name = posting_params["brand"]["name"],
            outlet_id = posting_params["outlet"]["id"],
            outlet_name = posting_params["outlet"]["name"],
            discount_in_percent = posting_params["discount_in_percent"],
            top_level_catalog_id = posting_params["top_level_catalog_id"],
            original_url = posting_params["original_url"][0],
            provider = provider)
    
    def fundgrube_url(self):
        return self.provider.web_url() + "?" + f"text={self.pim_id}" + f"&outletIds={self.outlet_id}"
        


import requests
from requests.adapters import HTTPAdapter, Retry
from functools import cache
class FundgrubeSearch:
    BLANK_RESULT = {
               "categories": [],
               "brands": [],
               "outlets": [],
               "postings": [],
               "morePostingsAvailable": False
            }

    def __init__(self, provider, query):
        self.provider = provider
        self.query = query

    def fetch(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "*/*"
        }

        session = requests.Session()
        session.headers = headers
        session.mount('https://', HTTPAdapter(max_retries=Retry(total=3)))

        print(f"Requesting: {self.build_url()}")

        response = session.get(self.build_url(), headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return self.BLANK_RESULT
    
    def build_url(self):
        return self.provider.api_url() + self.query.build()
    
    @cache
    def search_cached(self):
        return self.fetch()
    
    def categories(self):
        return self.search_cached()["categories"]
    
    def brands(self):
        return self.search_cached()["brands"]
    
    def outlets(self):
        return self.search_cached()["outlets"]
    
    @cache
    def postings(self):
        postings = self.search_cached()["postings"]
        more_postings_available = self.search_cached()["morePostingsAvailable"]
        offset = self.query.query_opts["offset"] + len(postings)

        if more_postings_available == True:
            while more_postings_available == True:
                new_query = Query(self.query.query_opts | { "offset": offset })
                new_search = FundgrubeSearch(self.provider, new_query).fetch()
                new_postings = new_search["postings"]
                postings.extend(new_postings)
                offset = offset + len(new_postings)
                more_postings_available = new_search["morePostingsAvailable"]

        posting_objects = []
        
        for posting_params in postings:
            posting_objects.append(Posting.from_params(self.provider, posting_params))
        
        return posting_objects

    def cheapest(self, number=1):
        postings_list = self.postings()
        postings_list.sort(key=lambda x: float(x.price))

        return postings_list[:number]

    def unique_pim_ids_with_name(self):
        self.postings
        unique = set([i.pim_id for i in self.postings()])

        pimids_with_name = {}
        for id in unique:
            pimids_with_name[id] = [x.name for x in self.postings() if x.pim_id == id][0]      

        return pimids_with_name
