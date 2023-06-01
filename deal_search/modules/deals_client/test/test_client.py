import unittest
import responses
import json
import sys

sys.path.append("..")
import client


class TestClient(unittest.TestCase):

  @responses.activate
  def test_results_present(self):
    fixture_1 = json.loads(open("fixtures/response_200_1.json", "r").read())
    fixture_2 = json.loads(open("fixtures/response_200_2.json", "r").read())


    responses.add(
      responses.GET,
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=100&offset=0&text=testitem",
      json=fixture_1,
      status=200)
    
    responses.add(
      responses.GET,
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=100&offset=100&text=testitem",
      json=fixture_2,
      status=200)

    mm = client.Provider('MM')
    query = client.DealsQuery({"text": "testitem"})
    search = client.DealSearch(mm, query)
    self.assertEqual(len(search.postings()), 200)
    self.assertEqual(search.cheapest()[0].price, 169.0)

  @responses.activate
  def test_fetch_product_name(self):
    single_item_fixture = json.loads(open("fixtures/response_200_single_item.json", "r").read())

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
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=100&offset=0&text=testitem-not-found",
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
      "https://www.mediamarkt.de/de/data/fundgrube/api/postings?limit=100&offset=0&text=error",
      json='',
      status=422)
    
    mm = client.Provider('MM')
    query = client.DealsQuery({"text": "error"})
    search = client.DealSearch(mm, query)
    self.assertEqual(len(search.postings()), 0)

# Run the tests
if __name__ == '__main__':
  unittest.main()
