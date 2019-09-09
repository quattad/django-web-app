import html

def parse_content(input_string):
    """
    Custom parsing to
    1) remove strings <p>, </p> and <br />
    2) convert 
    """
    return html.unescape(input_string.replace("<p>", "").replace("</p>", "").replace("<br />", ""))

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def quotes_paginator(input_quotes, input_posts, input_current_page):
    """
    Creates quotes paginator where input_quotes is an iterable (i.e. list) of quote objects and
    input_posts is int for desired number of posts per page. 
    Runs try, except logic and returns quote for template rendering
    """

    paginator = Paginator(input_quotes, input_posts)
    
    try:
        quotes = paginator.get_page(input_current_page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(input_current_page.num_pages)

    return quotes