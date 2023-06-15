from django.shortcuts import render, redirect, get_object_or_404
from deal_search.models import Provider
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request, provider):   
    PROVIDERS = {
        "mediamarkt": "MM",
        "saturn": "SAT"
    }
 
    city = str(request.GET.get('city') or "")
    identifier = PROVIDERS.get(provider)
    provider_query = get_object_or_404(Provider, identifier=identifier)
    branches_query = provider_query.branch_set
    paginator = Paginator(branches_query.filter(name__icontains=city), 20)
    page = request.GET.get('page') or 1
    
    try:
      paginated_branches = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
      return redirect("deals_index", provider=provider)   
    
    return render(
      request,
      "deals/index.html",
      {
          "branches": paginated_branches,
          "provider": provider
      } 
    )
