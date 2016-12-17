from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from services import Services
from news.models import Story
from news.forms import SearchForm
#from el_pagination.views import AjaxListView

def index(request):
    page = request.GET.get('page')
    if page==None:
        page=1
    else: 
        page=int(page)
    if page<1 or page>50:
        page=1
    serv = Services()
    queryset = serv.get_topstories(page)
    #queryset = Story.objects.all()
    #paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    context = {
        'title': 'HackerNews Clone',
        'top_stories': queryset,
        'page_number': page,
        'page_prev': page-1,
        'page_next': page+1
    }
    return render(request, 'index.html', context)
    #return HttpResponse("Hello, world. You're at the polls index.")

def search(request):
    if request.method == "POST":
        #Get the posted form
        searchForm = SearchForm(request.POST)
        page=1
        if searchForm.is_valid():
            search_text = searchForm.cleaned_data['search_text']
        else:
            return index(request)
        queryset = Story.objects.filter(title__icontains=search_text)
        context = {
            'title': 'HackerNews Clone Search',
            'top_stories': queryset,
            'page_number': page,
            'page_prev': 0,
            'page_next': 51
        }
        return render(request, 'search.html', context)

        #return HttpResponse("Hello, world. You're at the polls index.")
