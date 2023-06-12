from django.test import TestCase
from deal_search.models import Branch, Provider, Posting
from deal_search.modules.sync.sender import post_branches, post_postings
import responses

class TestSync(TestCase):
  def setUp(self):
    self.url = "https://sync-dest.com/"

  @responses.activate
  def test_sync(self):
    rsp1 = responses.Response(
      method="POST",
      url=self.url,
      headers={"Content-Type": "application/json"},
      status=201
    )
    responses.add(rsp1)

    self.assertEqual(post_branches(self.url, self.token).status_code, 201)
    self.assertEqual(post_postings(self.url, self.token).status_code, 201)