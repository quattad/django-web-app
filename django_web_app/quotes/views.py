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
                    dict_item[key] = html.unescape(dict_item[key])  # Replace numeric character references
                
            quote = Quote()
            quote.author = dict_item['title']
            quote.content = dict_item['content']

            check = Quote.objects.filter(content=quote.content).all()   # returns Queryset if quote content exists

            if not check:
                print("Saving to database...") # If not in database
                quote.save()
            else:
                quote.id = check.values("id")[0]['id']  # If in database, store existing quote id into object sent for template rendering
                
                q = Quote.objects.get(content=quote.content)  # fetches quote from database
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