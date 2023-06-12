from django.core import serializers
import requests
from deal_search.models import Branch, Posting

def _auth_header(auth_token):
    return { "Authorization": f"Bearer {auth_token}" }

def _post_json(url, auth_token, json):
    return requests.post(headers=_auth_header(auth_token), url=url, json=json)

def post_branches(url, auth_token):
    json = serializers.serialize('json', Branch.objects.all())

    return _post_json(url=url, auth_token=auth_token, json=json)

def post_postings(url, auth_token):
    json = serializers.serialize('json', Posting.objects.all())

    return _post_json(url=url, auth_token=auth_token, json=json)
