# ![WikiCFP Logo](http://www.wikicfp.com/cfp/images/wikicfplogo-90.png) Conferences World Map
Crawling the WikiCFP and displays a map
--------

## What is it for?

You can use the [WikiCFP Conference Search](http://www.wikicfp.com/cfp/allcfp), but it is a list. I think it is much more interesting to see a map, where conferences happening.

![iEEE Conference World Map](https://github.com/balzer82/iEEEConferenceWorldMap/blob/master/iEEE-Conferences-2014-Worldmap.png?raw=true)


## How to use it?

``` python iEEECrawler.py ```

Probably it is better to use the .ipynb (iPython Notebook), because I am using it and probably I forgot to update the .py

## What is it doin'?

1. search iEEE Conference Database
2. extract all infos from website
3. ask Google for location of the adress (Geoencoding)
4. save [.kml file (for Google Earth)](https://raw.github.com/balzer82/iEEEConferenceWorldMap/master/iEEE-Conferences.kml)
5. create World map, US Map and Europe Map

![IEEE European Conferences](https://github.com/balzer82/iEEEConferenceWorldMap/blob/master/iEEE-Conferences-2014-Europe.png?raw=true)

![IEEE US Conferences](https://github.com/balzer82/iEEEConferenceWorldMap/blob/master/iEEE-Conferences-2014-USA.png?raw=true)


## Dependencies

1. Matplotlib (for Rendering)
2. Basemap (for Map)
4. Requests (for URL requests)
5. BeatuifulSoup (for HTML parsing)
6. numpy (for array)
7. time (for timeout for Google API)
8. simplekml (for kml)
