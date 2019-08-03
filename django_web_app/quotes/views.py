from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models.query import EmptyQuerySet
from quotes.models import Quote, Like, Favourite
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib import messages
import requests, json, html
from urllib.parse import urlencode

from .models import Quote
from .custom_modules.support_func import parse_content

@login_required
def home(request):
    """
    Displays list of generated quotes from quotesondesign.
    """
    if request.method == "GET":
        posts = request.GET.get('posts', 4)
        page = request.GET.get('page', 1)
        
        response = requests.get("https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=30")
        data = response.json()

        quotes = []

        for dict_item in data:

            quote = Quote()

            quote.content = list(map(lambda d: parse_content(d), 
            [value for key, value in dict_item.items() if key == "content"]))[0]

            quote.author = dict_item['title']

            check = Quote.objects.filter(content=quote.content).all()   # returns Queryset if quote content exists

            if not check:
                quote.save()
            else:
                quote.id = check.values("id")[0]['id']  # If in database, store existing quote id into object sent for template rendering
                
                q = Quote.objects.get(id=quote.id)  # fetches quote from database
                quote.no_user_likes = q.like_set.all().count()  # generate number of user likes for particular quote
                quote.no_user_favourites = q.favourite_set.all().count()  # generate number of user likes for particular quote

                quote.check_liked = check.values("check_liked")[0]["check_liked"] # check if quote has been liked by logged in user
                quote.check_favourited = check.values("check_favourited")[0]["check_favourited"] # check if quote has been favourited by logged in user

            quotes.append(quote)
        
        # Paginate quotes
        quote_paginator = Paginator(quotes, posts)
        
        try:
            quotes = quote_paginator.get_page(page)
        except PageNotAnInteger:
            quotes = quote_paginator.page(1)
        except EmptyPage:
            quotes = quote_paginator.page(page.num_pages)
        
        return render(request, 'quotes/home.html', {
            'quotes': quotes, 'posts': posts, 'page': page, 'max_posts':list(range(3, 6))})
            
    
    elif request.method == "POST":
        # URL queries are always fetched via GET, not POST; request.POST.get() is only for retrieving from request.body
        posts = request.GET.get('posts', 4)
        page = request.GET.get('page', 1)

        if request.user is not AnonymousUser and isinstance(request.POST.get('submit_user_like'), str):

            quote_id = request.POST.get("submit_user_like") 
            like_obj, created = Like.objects.get_or_create(user=request.user, quote_id = quote_id) # Creates Like entry in table quotes_like. Outputs (Like object, boolean on whether created)
            quote = Quote.objects.get(id=quote_id)

            if (not created) and (quote.check_liked == True): # if (already in database) and (already liked by user)
                quote.check_liked = False
                quote.save()
                Like.objects.filter(quote=quote_id).delete()
                messages.success(request, "Unliked!")
            else:
                quote.check_liked = True
                quote.save()
                messages.success(request, "Liked!")
        
        elif request.user is not AnonymousUser and isinstance(request.POST.get('submit_user_favourite'), str):
            
            quote_id = request.POST.get("submit_user_favourite")
            fav_obj, created = Favourite.objects.get_or_create(user=request.user, quote_id = request.POST.get('submit_user_favourite'))
            quote = Quote.objects.get(id=quote_id)

            if (not created) and (quote.check_favourited==True): # if (already in database) and (already liked by user)
                quote.check_favourited = False
                quote.save()
                Favourite.objects.filter(quote=quote_id).delete()
                messages.success(request, "Removed from favourites!")
            else:
                quote.check_favourited = True
                quote.save()
                messages.success(request, "Favourited!")
        
        # Build redirect string back to 'quotes-home' with 'posts' and 'page' url query
        base_url = reverse('quotes-home')
        query_string = urlencode({'page':page})
        url = '{}?{}'.format(base_url, query_string)

        return redirect(url)

@login_required
def favourites(request):
    if request.method == "GET":
        """
        Shows list of favourited quotes by user
        """
        posts = request.GET.get('posts', 4)
        page = request.GET.get('page', 1)

        # Filter user favourites from Favourites table
        quotes = Favourite.objects.filter(user=request.user).all()
        # Get a list of Quote objects from Quotes table that match id
        quotes = list(map(lambda quote_id: Quote.objects.get(id=quote_id), [quote.quote_id for quote in quotes]))
        
        if quotes:
            quotes_paginator = Paginator(quotes, posts)

            try:
                quotes = quotes_paginator.get_page(page)
            except PageNotAnInteger:
                quotes = quotes_paginator.page(1)
            except EmptyPage:
                quotes = quotes_paginator.page(page.num_pages)

        return render(request, 'quotes/favourites.html', {
            'quotes': quotes, 
            'posts': posts,
            'page':page,
            'max_posts': list(range(3, 6))
            })
    
    elif request.method == "POST":

        posts = request.GET.get('posts', 4)
        page = request.GET.get('page', 1)
        
        if isinstance(request.POST.get('submit_user_favourite'), str):
            
            quote_id = request.POST.get("submit_user_favourite")
            fav_obj, created = Favourite.objects.get_or_create(user=request.user, quote_id = request.POST.get('submit_user_favourite'))
            quote = Quote.objects.get(id=quote_id)

            if (not created) and (quote.check_favourited==True):
                quote.check_favourited = False
                quote.save()
                Favourite.objects.filter(quote=quote_id).delete()
                messages.success(request, "Removed from favourites!")
            else:
                quote.check_favourited = True
                quote.save()
                messages.success(request, "Favourited!")
        
        # To catch exception when all quotes on 1st page deleted
        if not page:
            page = 1

        base_url = reverse('quotes-fav')
        query_string = urlencode({'page':page})
        url = '{}?{}'.format(base_url, query_string)

        return redirect(url)