from django.shortcuts import render, get_object_or_404
from deal_search.models import Provider

def index(request, provider):   
    PROVIDERS = {
        "mediamarkt": "MM",
        "saturn": "SAT"
    }

    identifier = PROVIDERS.get(provider)

    provider_query = get_object_or_404(Provider, identifier=identifier)
    branches_query = provider_query.branch_set
  
    return render(
       request,
       "deals/index.html",
       {
           "branches": branches_query.all()
       } 
    )