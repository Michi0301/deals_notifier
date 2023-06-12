from unittest import TestCase
import responses
import json
import sys
import os
from deal_search.modules.deals_client import client

class TestClient(TestCase):
  @responses.activate
  def test_results_present(self):
    
    fixture_1 = json.loads(open(os.path.join(os.path.dirname(__file__), "fixtures", "response_200_1.json"), "r").read())
    fixture_2 = json.loads(open(os.path.join(os.path.dirname(__file__), "fixtures", "response_200_2.json"), "r").read())


    responses.add(
      responses.GET,
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=99&offset=0&text=testitem",
      json=fixture_1,
      status=200)
    
    responses.add(
      responses.GET,
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=99&offset=100&text=testitem",
      json=fixture_2,
      status=200)

    mm = client.Provider('MM')
    query = client.DealsQuery({"text": "testitem"})
    search = client.DealSearch(mm, query)
    self.assertEqual(len(search.postings()), 200)
    self.assertEqual(search.cheapest()[0].price, 169.0)

  @responses.activate
  def test_fetch_product_name(self):
    single_item_fixture = json.loads(open(os.path.join(os.path.dirname(__file__), "fixtures", "response_200_single_item.json"), "r").read())

    responses.add(
      responses.GET,
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=1&offset=0&text=2764537",
      json=single_item_fixture,
      status=200)
    
    mm = client.Provider('MM')
    found_name = client.DealSearch.fetch_product_name(mm, "2764537")
    expected_name = "APPLE Watch SE (GPS) 40mm Smartwatch Aluminium Fluorelastomer, 130 - 200 mm, Armband: Mitternacht, Gehäuse: Space Grau"
    self.assertEqual(found_name, expected_name)

  @responses.activate
  def test_results_not_present(self):
    response = json.loads('{"categories":[],"brands":[],"outlets":[],"text":[{"id":"search","name":"sdasdas","count":1}],"postings":[],"morePostingsAvailable":false}')

    responses.add(
      responses.GET,
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=99&offset=0&text=testitem-not-found",
      json=response,
      status=200)
    
    mm = client.Provider('MM')
    query = client.DealsQuery({"text": "testitem-not-found"})
    search = client.DealSearch(mm, query)
    self.assertEqual(len(search.postings()), 0)


  @responses.activate
  def test_results_not_200(self):
    responses.add(
      responses.GET,
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=99&offset=0&text=error",
      json='',
      status=422)
    
    mm = client.Provider('MM')
    query = client.DealsQuery({"text": "error"})
    search = client.DealSearch(mm, query)
    self.assertEqual(len(search.postings()), 0)

  @responses.activate
  def test_branch_search(self):
    branches_fixture = json.loads(open(os.path.join(os.path.dirname(__file__), "fixtures", "response_200_branch_search.json"), "r").read())
    responses.add(
     responses.GET,
     "https://www.mediamarkt.de/api/v1/graphql?variables=%7B%22limit%22:%2010,%20%22zipCodeOrCity%22:%20%2285298%22%7D&extensions=%7B%22persistedQuery%22:%20%7B%22version%22:%201,%20%22sha256Hash%22:%20%2232e9f9493e3a218eb17a48fc6c68fea0bec636ae3b5e188dee94ef9879cf405d%22%7D,%20%22pwa%22:%20%7B%22salesLine%22:%20%22Media%22,%20%22country%22:%20%22DE%22,%20%22language%22:%20%22de%22,%20%22globalLoyaltyProgram%22:%20true,%20%22fifaUserCreation%22:%20true%7D%7D",
     json=branches_fixture,
     status=200)

    mm = client.Provider('MM')
    search = client.BranchSearch(mm, "85298", limit=10)
    self.assertEqual(len(search.fetch_branches()), 10)
