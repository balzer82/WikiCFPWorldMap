# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# WikiCFP Conferences World Map

# <codecell>

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import simplekml

# <headingcell level=2>

# Convert Address to LatLon

# <codecell>

def address2coord(addr):
    
    result = None
    address = addr
    
    if 'TBD' in addr or 'N/A' in addr:
        print 'No location determined yet.'
        return (u'0.0', u'0.0')
    
    while result is None:
        try:
            url = 'http://maps.googleapis.com/maps/api/geocode/xml'
            payload = {'address': unicode(address), 'sensor': 'true'}
            
            try:
                response = requests.get(url, params=payload)
            except Exception, e:
                print e.message
                return Error(2, "Google", "Google nicht erreichbar.")
        
            if response.status_code != 200:
                print "Can't connect to Google! (status code: " + response.status_code + ")"    
                return Error(response.status_code, "Google", "Google Server nicht erreichbar")
            
            if type(response.content) is unicode:
                soup = BeautifulSoup(response.content.encode('utf8'))
            else:
                soup = BeautifulSoup(response.content)

            
            #print response.content

            if soup.find('status').string == 'OK':
                print('Found Location.')
                result = True
                return (soup.find('lat').string , soup.find('lng').string)
            elif soup.find('status').string == 'OVER_QUERY_LIMIT':
                print 'Google API Query Limit reached. Waiting... (maybe you should renew your IP)'
                time.sleep(5)
            elif soup.find('status').string == 'ZERO_RESULTS':
                print '\n' + unicode(address)
                print "not found!"
                result = True
                return (u'0.0', u'0.0')
            else:
                print '\n' + unicode(address) + '\n'
                print response.url
                print "not found! Giving up..."
                result = True
                return (u'0.0', u'0.0')

        except:
            pass

# <headingcell level=2>

# Crawl the conference search

# <headingcell level=2>

# Extract the Data

# <codecell>

confs={}
confname=[]
confdate=[]
confloc =[]
conflat =[]
conflon =[]
confurl =[]
confdesc=[]
cfpdate =[]
print('Extracting the data from website')

# Daten von iEEE Webseite holen
url='http://www.wikicfp.com/cfp/allcfp'

site = 0
moredata=True

while moredata and site < 10:
    
    site+=1
    # Fire the request
    try:
        print('Requesting Conference Search...')
        data = requests.get(url, params={'page': site})
        print('Done.')
    except Exception, e:
        moredata=False
        print e.message
    if data.status_code != 200:
        print "Can't connect to WikiCFP! (status code: " + response.status_code + ")"        
    
    # Crawl the Data
    soup = BeautifulSoup(data.text)

    
    idx=0
    for content in soup.body.find_all('div', attrs={'class' : 'contsec'}):
        for table in content.find_all('tr', attrs={'bgcolor' : ['#f6f6f6','#e6e6e6']}):
            for infos in table.find_all('td', attrs={'align' : 'left'}):
    
                # Tabelle durchgehen
                if idx==0:
                    # Conference Name
                    confname.append(infos.a.text.strip())
                    confurl.append('http://www.wikicfp.com' + infos.a['href'])
    
                elif idx==1:
                    # Ausführlicher Name
                    confdesc.append(infos.text.strip())
                
                elif idx==2:
                    # Datum
                    confdate.append(infos.text.strip())
                    
                elif idx==3:
                    # Ort
                    location = infos.text.strip()
        
                    print location
                    confloc.append(location) 
                    # Geoencoding
                    lat,lon = address2coord(location)
                    conflat.append(float(lat))
                    conflon.append(float(lon))
                
                elif idx==4:
                    # Call For Papers Deadline
                    cfpdate.append(infos.text.strip())
                    
                else:
                    print(u'Unklar, was das für Daten sind.')
        
    
    
                idx+=1
                if idx==5:
                    idx=0
        

confs = zip(confname,confdate,conflat,conflon,confloc,confurl,confdesc,cfpdate)
print('Done.')

# Print the Table           
#for i in range(len(confname)):
#    print('%s findet am %s in %s statt.\n' % (confname[i], confdate[i], confloc[i]))

# <headingcell level=2>

# Clean Data and create KML

# <codecell>

kml = simplekml.Kml()
# Konferenzen löschen, für die kein Ort gefunden wurden
lon=[]
lat=[]
print('Creating .kml file.')
for i in range(len(confs)):
    if confs[i][3] == 0.0:
        pass
    else:
        # KML
        pnt=kml.newpoint(name=confs[i][0], coords=[(confs[i][3],confs[i][2])])
        desct = confs[i][6]
        desct += '\nfrom ' + confs[i][1]
        desct += '\nin ' + confs[i][4] + '.'
        desct += '\n\nCFP deadline: ' + confs[i][7]
        desct += '\n\nInfos: ' + confs[i][5]
        pnt.description = desct
        
        # List for Map
        lon.append(confs[i][3])
        lat.append(confs[i][2])

kml.save("WikiCFP-Conferences.kml")
print('Done.')
print('%s of %s conference venues without place.' % (len(confs)-len(lat),len(confs)))
if (len(confs)-len(lat)) == 0:
    print 'Perfect.'
elif (len(confs)-len(lat)) > 5:
    print 'Maybe you should check your Data'

# <headingcell level=2>

# Render the Map

# <headingcell level=3>

# World

# <codecell>

# Thanks to this great tutorial:
# http://peak5390.wordpress.com/2012/12/08/mapping-global-earthquake-activity-a-matplotlib-basemap-tutorial/

map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=0)
map.drawcoastlines()
map.drawcountries()
#map.fillcontinents(color = 'gray')
map.bluemarble()
map.drawmapboundary()
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

x,y = map(lon, lat)
map.plot(x, y, 'ro', markersize=6)
plt.title('WikiCFP Conferences 2014 Worldmap')
plt.savefig('WikiCFP-Conferences-2014-Worldmap.png', bbox_inches='tight', dpi=300, transparent=True)
#plt.show()
plt.close()

# <headingcell level=3>

# Europe

# <codecell>

m = Basemap(llcrnrlon=-14.0,llcrnrlat=32.0,urcrnrlon=44.4,urcrnrlat=55.3,
            resolution='i',projection='stere',lon_0=10.0,lat_0=54.7)

m.drawcoastlines()
m.fillcontinents(color='gray')
# draw parallels and meridians.
#m.drawparallels(np.arange(-40,61.,2.))
#m.drawmeridians(np.arange(0.,43.,2.))
m.drawmapboundary()
m.drawcountries()

x,y = m(lon, lat)
m.plot(x, y, 'ro', markersize=6)


plt.title("European WikiCFP Conferences 2014")
plt.savefig('WikiCFP-Conferences-2014-Europe.png', bbox_inches='tight', dpi=300, transparent=True)

#plt.show()
plt.close()

# <headingcell level=3>

# USA

# <codecell>

mus = Basemap(llcrnrlon=-125.0,llcrnrlat=20.0,urcrnrlon=-60.0,urcrnrlat=51.4,
            resolution='i',projection='stere',lon_0=-95.0,lat_0=35.0)

mus.drawcoastlines()
mus.fillcontinents(color='gray')
# draw parallels and meridians.
#m.drawparallels(np.arange(-40,61.,2.))
#m.drawmeridians(np.arange(0.,43.,2.))
mus.drawmapboundary()
mus.drawcountries()
mus.drawstates()

x,y = mus(lon, lat)
mus.plot(x, y, 'ro', markersize=6)


plt.title("US WikiCFP Conferences 2014")
plt.savefig('WikiCFP-Conferences-2014-USA.png', bbox_inches='tight', dpi=300, transparent=True)

#plt.show()
plt.close()

# <codecell>

print('Done.')

