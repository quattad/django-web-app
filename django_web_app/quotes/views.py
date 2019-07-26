from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models.query import EmptyQuerySet
from quotes.models import Quote
from django.urls import reverse
from django.contrib import messages
import requests, json

from .models import Quote

@login_required
def home(request):
    if request.method == "GET":
        response = requests.get("https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=5")
        data = response.json()
        quotes = []

        for dict_item in data:
            for key, value in dict_item.items():
                if key == 'content':
                    dict_item[key] = value.replace("<p>", "").replace("</p>", "")
                
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
        
        return render(request, 'quotes/home.html', {'quotes': quotes})
            
    
    elif request.method == "POST":
        if request.user is not AnonymousUser: 
            # Fetch quote liked from existing database
            quote_liked = get_object_or_404(Quote, id=request.POST.get('submit_user_like'))
             
            # Add user to user_liked field of quote
            quote_liked.user_liked.add(request.user)
            
            messages.success(request, "Liked!")
            return redirect('quotes-home')
