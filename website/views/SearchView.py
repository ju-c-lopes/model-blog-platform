from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from website.forms.SearchForm import SearchForm
from website.models.PostModel import Post

def search_posts(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query', '')
    results = []
    
    if query:
        # Search in title, text, and author name
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(text__icontains=query) | 
            Q(author__author_name__icontains=query)
        ).order_by('-published_date')
    
    # Pagination
    paginator = Paginator(results, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'form': form,
        'query': query,
        'posts': posts,
        'results_count': results.count() if query else 0,
    }
    
    return render(request, 'search/search_results.html', context)