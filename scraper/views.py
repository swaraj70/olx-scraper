import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

BASE_OLX_URL = 'https://www.olx.in/items/q-{}'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_OLX_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'EIR5N'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='_2tW1I').text
        post_url = post.find('a').get('href')

        if post.find(class_='_89yzn'):
            post_price = post.find(class_='_89yzn').text
        else:
            post_price = 'N/A'

        if post.find(class_='_2grx4'):
            post_image_url = post.a.figure.img['src']
            print(post_image_url)
        else:
            post_image_url = 'https://www.olx.in/apple-touch-icon.png'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    context = {
        'search' : search,
        'final_postings': final_postings,
    }
    return render(request, 'scraper/new_search.html', context)