from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models.query import EmptyQuerySet
from quotes.models import Quote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib import messages
import requests, json, html
from urllib.parse import urlencode

from .models import Quote

@login_required
def home(request):
    if request.method == "GET":
        posts = request.GET.get('posts', 4)
        page = request.GET.get('page', 1)
        
        response = requests.get("https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=30")
        data = response.json()

        quotes = []

        for dict_item in data:
            for key, value in dict_item.items():
                if key == 'content':
                    dict_item[key] = value.replace("<p>", "").replace("</p>", "").replace("<br />", "")
                    # Replace numeric character references
                    dict_item[key] = html.unescape(dict_item[key])
                
            quote = Quote()
            quote.author = dict_item['title']
            quote.content = dict_item['content']

            # returns Queryset if quote content exists
            check = Quote.objects.filter(content=quote.content).all()

            if not check:
                # If not in database
                print("Saving to database...")
                quote.save()
            else:
                # If in database, store existing quote id into object sent for template rendering
                quote.id = check.values("id")[0]['id']
            
            quotes.append(quote)
        
        # Paginate quotes
        quote_paginator = Paginator(quotes, posts)
        
        try:
            quotes = quote_paginator.get_page(page)
        except PageNotAnInteger:
            quotes = quote_paginator.page(1)
        except EmptyPage:
            quotes = quote_paginator.page(page.num_pages)
        
        # Debugging
        print("page=" + str(page))
        print("posts=" + str(posts))
        
        return render(request, 'quotes/home.html', {'quotes': quotes, 'posts': posts, 'page': page, 'max_posts':list(range(3, 6))})
            
    
    elif request.method == "POST":
        # URL queries are always fetched via GET, not POST
        # request.POST.get() is only for retrieving from request.body
        posts = request.GET.get('posts', 4)
        page = request.GET.get('page', 1)

        if request.user is not AnonymousUser and isinstance(request.POST.get('submit_user_like'), str):
            # Fetch quote liked from existing database
            quote_liked = get_object_or_404(Quote, id=request.POST.get('submit_user_like'))
             
            # Add user to user_liked field of quote
            quote_liked.user_liked.add(request.user)
            
            messages.success(request, "Liked!")
        elif request.user is not AnonymousUser and isinstance(request.POST.get('submit_user_favourite'), str):
            # Fetch quote from existing database
            quote_favourited = get_object_or_404(Quote, id=request.POST.get('submit_user_favourite'))
             
            # Add user to user_favourited field of quote
            quote_favourited.user_favourited.add(request.user)
            
            messages.success(request, "Favourited!")
        
        # Build redirect string back to 'quotes-home' with 'posts' and 'page' url query
        base_url = reverse('quotes-home')
        query_string = urlencode({'page':page})
        url = '{}?{}'.format(base_url, query_string)

        return redirect(url)