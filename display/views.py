from django.shortcuts import render

import requests
from bs4 import BeautifulSoup
import googlemaps
import pprint

# Create your views here.
def index(request):
    return render(request,'index.html')

def form(request):
    country = request.POST['country']
    url = 'https://www.worldometers.info/coronavirus/'
    html = requests.post(url)
    purehtml = html.content

    # Souping
    soup = BeautifulSoup(purehtml,'html.parser')
    th = soup.find_all('table' , id='main_table_countries_today')

    #getting all headings
    para_list = []
    for trr in th[0].find_all('tr'):
        for i in trr.find_all('th'):
            para_list.append(i.text)

    # fetching particular country's data
    data_list = []
    bool = False
    for trr in th[0].find_all('tr'):
        for i in trr.find_all('td'):
            if i.text == country or bool:
                bool = True
                data_list.append(i.text)
            else:
                break
        bool = False


    #making dictionaries
    data = dict(zip(para_list,data_list))

    return render(request,'other.html',{'country':data['Country,Other'],'cases':data['TotalCases'],'deaths':data['TotalDeaths'],'perm':data['Tot\xa0Cases/1M pop'],'recovered':data['TotalRecovered']})

def local(request):

    # Getting ip address of user
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')


    # Country and state of user
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()
    local_country = geo_data['country']
    local_state = geo_data['region']
    local_city = geo_data['city']

    latitude = geo_data['latitude']
    longitude = geo_data['longitude']
    latlong = latitude+","+longitude

    # Just for declaration with default values
    confirmcase = 'No data Found'
    deaths = 'No data Found'
    recover = 'No data Found'
    new = 'No data Found'


    # Searching for places with Google maps 

    # Setting up gooogle maps with api key
    api_key = 'AIzaSyARkCNibIqeZsNydraFEU8u5DLQOjoUzmE'
    gmaps = googlemaps.Client(key=api_key)
    result = gmaps.places_nearby(location=latlong, radius=10000, open_now=True, type="grocery_or_supermarket" or "home_goods_store" )

    # Names
    names = []
    names.append(result['results'][0]['name'])
    names.append(result['results'][1]['name'])
    names.append(result['results'][2]['name'])
    names.append(result['results'][3]['name'])

    # Photo reference
    pr = []
    pr.append(result['results'][0]['photos'][0]['photo_reference'])
    pr.append(result['results'][1]['photos'][0]['photo_reference'])
    pr.append(result['results'][2]['photos'][0]['photo_reference'])
    pr.append(result['results'][3]['photos'][0]['photo_reference'])
    
    # image URL
    img = []
    img.append('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+pr[0]+'&key=AIzaSyARkCNibIqeZsNydraFEU8u5DLQOjoUzmE')
    img.append('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+pr[1]+'&key=AIzaSyARkCNibIqeZsNydraFEU8u5DLQOjoUzmE')
    img.append('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+pr[2]+'&key=AIzaSyARkCNibIqeZsNydraFEU8u5DLQOjoUzmE')
    img.append('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+pr[3]+'&key=AIzaSyARkCNibIqeZsNydraFEU8u5DLQOjoUzmE')

    # Vicinity
    v = []
    v.append(result['results'][0]['vicinity'])
    v.append(result['results'][1]['vicinity'])
    v.append(result['results'][2]['vicinity'])
    v.append(result['results'][3]['vicinity'])

    # Getting data of a Country

    if local_country=='India':

        # COUNTRY DATA
        url = 'https://api.covid19india.org/data.json'
        html = requests.get(url).json()
        state = html['statewise']
        ccases = state[0]['confirmed']
        cdeaths = state[0]['deaths']
        cnew = state[0]['deltaconfirmed']
        crecover = state[0]['recovered']

        # STATE DATA
        url = 'https://api.covid19india.org/data.json'
        html = requests.get(url).json()
        state = html['statewise']

        count = 0
        for i in state:
            count += 1
            if i['state'] == local_state:
                break

        confirmcase = html['statewise'][count - 1]['confirmed']
        deaths = html['statewise'][count - 1]['deaths']
        recover = html['statewise'][count - 1]['recovered']
        new = html['statewise'][count - 1]['deltaconfirmed']

        return render(request,'Indian.html',{'state':local_state,'cases':confirmcase,'deaths':deaths,
        'recover':recover,'inc':new, 'country':local_country,'ccases':ccases,'cdeaths':cdeaths,
        'recovered':crecover,'newc':cnew,'b0':names[0], 'b1':names[1], 'b2':names[2], 'b3':names[3]
        ,'img0':img[0],'img1':img[1],'img2':img[2],'img3':img[3], 'add0':v[0], 'add1':v[1], 'add2':v[2], 'add3':v[3] })


    else:

    # url declared and fetching from url
        url = 'https://www.worldometers.info/coronavirus/'
        html = requests.post(url)
        purehtml = html.content

        # Souping
        soup = BeautifulSoup(purehtml,'html.parser')
        th = soup.find_all('table' , id='main_table_countries_today')

        #getting all headings
        para_list = []
        for trr in th[0].find_all('tr'):
            for i in trr.find_all('th'):
                para_list.append(i.text)

        # fetching particular country's data
        data_list = []
        bool = False
        for trr in th[0].find_all('tr'):
            for i in trr.find_all('td'):
                if i.text == local_country or bool:
                    bool = True
                    data_list.append(i.text)
                else:
                    break
            bool = False


        #making dictionaries
        data = dict(zip(para_list,data_list))

        return render(request,'Indian.html',{'state':local_state,'cases':confirmcase,'deaths':deaths,
        'recover':recover,'recovered':data['TotalRecovered'],'inc':new,'country':local_country,
        'ccases':data['TotalCases'],'deaths':data['TotalDeaths'],'newc':data['NewCases']})
