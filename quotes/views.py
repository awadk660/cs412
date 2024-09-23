# quotes/views.py
# description: write view functions to handle URL requests for the quotes app

from django.shortcuts import render
import random

quotes = ["Many of life's failures are people who did not realize how close they were to success when they gave up.",
          "Vision without execution is hallucination.",
          "I haven't failed. I've just found 10,000 ways that won't work."]

images = ["https://cdn.britannica.com/44/19444-050-1DA32C1C/replica-Thomas-A-Edison-lightbulb-1925.jpg",
          "https://www.thelightbulb.co.uk/wp-content/uploads/2021/11/thomas-edison-1.jpg",
          "https://images.squarespace-cdn.com/content/v1/5ae3ecc5266c0741c7685ac7/1649696986236-4DEQM213IKDN417BR5WA/LM%2BArticle%2BGraphic%2BThomas%2BEdison%2B02.jpg?format=750w"]

def home(request):
    RandomInt = random.randint(0,len(quotes)-1)
    context = {
        "quote": quotes[RandomInt],
        "image": images[RandomInt],
    }
    template_name = 'quotes/quote.html'
    return render(request, template_name, context)

def show_all(request):
    template_name = 'quotes/show_all.html'
    context = {
        "quotes": quotes,
        "images": images,
    }
    return render(request, template_name, context)

def about(request):
    template_name = 'quotes/about.html'
    return render(request, template_name)