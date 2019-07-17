from django.shortcuts import render, redirect
import requests, json


# Function Based View
def home(request):
    if request.method == "GET":
        response = requests.get("https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1")
        quotes = response.json()

        for dict_item in quotes:
            for key, value in dict_item.items():
                if key == 'content':
                    dict_item[key] = value.replace("<p>", "").replace("</p>", "")

    return render(request, 'quotes/home.html', {'quotes': quotes})

# Class Based View

# class QuoteHomeView(ListView):
#     model = Quote
#     template_name = 'quotes/home.html'
#     context_object_name = 'quotes'
