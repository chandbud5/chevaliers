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
    
    # TO RUN ON LOCAL MACHINE COMMENT 51-55 and on 59 put your ip in place of 'ip' (in string)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')


    # Country and state of user
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/'+ip+'.json'
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
    api_key = 'AIzaSyAtfrvMgyBTPyLVy7aw3X91G4yGvzA2hFk'
    gmaps = googlemaps.Client(key=api_key)
    result = gmaps.places_nearby(location=latlong, radius=10000, open_now=True, type="hospital")

    # Photo reference
    names = []
    img = []
    v = []
    for i in range(0,4):

        names.append(result['results'][i]['name'])
        v.append(result['results'][i]['vicinity'])

        if 'photos' in result['results'][i].keys():
            pr = result['results'][i]['photos'][0]['photo_reference']
            img.append('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+pr+'&key=AIzaSyARkCNibIqeZsNydraFEU8u5DLQOjoUzmE')

        else :
            img.append(result['results'][i]['icon'])

    print(img)
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
