import json, os
import requests
from os import path
from os import listdir
from os.path import isfile, join
from string import Template
import time



#debug
debug = 1

filemovies = "movies-latest.json"
fileseries = "series-latest.json"

movieextendedprefix = '-extended' #used as ttXXXXXX-extended.json for each movie

extendeddirectory = 'extended/'
coverdirectory = 'html/covers/'
jsondirectory = 'json/'
htmldirectory = 'html/'

html_file = htmldirectory + 'index-' + time.strftime("%Y%m%d-%H%M%S") + '.html'

#check if directories exist
if os.path.isdir(htmldirectory):
    print ("directory exist " + htmldirectory)
else:
    os.mkdir(htmldirectory)

if os.path.isdir(extendeddirectory):
    print ("directory exist " + extendeddirectory)
else:
    os.mkdir(extendeddirectory)

if os.path.isdir(coverdirectory):
    print ("directory exist " + coverdirectory)
else:
    os.mkdir(coverdirectory)
    
if os.path.isdir(jsondirectory):
    print ("directory exist " + jsondirectory)
else:
    os.mkdir(jsondirectory)

	
#your https://imdb-api.com/ api id, gets your there
#there is a free one for 100 request a day
apiid = 'k_XXXXXX'

if debug:

    #os.system('rm *.json')
    
    urlmovies = 'https://vidsrc.me/movies/latest/page-1.json'
    urlseries = 'https://vidsrc.me/episodes/latest/page-1.json'

    rmovies = requests.get(urlmovies, allow_redirects=True)
    open(filemovies, 'wb').write(rmovies.content)

    rseries = requests.get(urlseries, allow_redirects=True)
    open(fileseries, 'wb').write(rseries.content)

#using wget (not using it)
#os.system('rm *.json')
#os.system('wget -O movies-latest.json https://vidsrc.me/movies/latest/page-1.json&> /dev/null 2>&1')
#os.system('wget -O series-latest.json https://vidsrc.me/episodes/latest/page-1.json&> /dev/null 2>&1')






with open(filemovies, 'r') as f:
    json_movies = json.load(f)

with open(fileseries, 'r') as f:
    json_series = json.load(f)
    
#print( distros_dict)

#print(json.dumps(json_movies, indent = 4, sort_keys=True))

print(json_movies['pages'])
print(json_series['pages'])

# Load the json data into a variable
#storedata = json.loads(json_movies)

# Iterate the for loop to print the data with key
#for val in storedata:
#  print("%s: %s" % (val, storedata[val]))

for result in json_movies['result']:
    print
    if debug:
        individualmoviejson = extendeddirectory + result['imdb_id'] + movieextendedprefix + '.json'
        if path.exists(individualmoviejson):
            print ("file exist " + individualmoviejson)
        else:
            print ("Creating new " + individualmoviejson)
            resultdicttostring = json.dumps(result)
            open(individualmoviejson, 'wb').write(resultdicttostring)

    print(result['imdb_id'])
    ttid_string = result['imdb_id']
    print(result['title'])
    print(result['quality'])
    print(result['embed_url'])
    
    #get poster and more
    htmlfilename = htmldirectory + ttid_string + '.html'
    jsonfilename = jsondirectory + ttid_string + '.json'
    coverfilename = coverdirectory + ttid_string + '.jpg'
    
    movie_url = 'https://imdb-api.com/API/Search/' + apiid + '/' + ttid_string
    print(movie_url)
    #request data
    
    #hold request for now, since i only have 100 per day
    if debug:
        if path.exists(jsonfilename):
            print ("file exist " + jsonfilename)
        else:
            print ("Creating new " + jsonfilename)
            rmovie_json = requests.get(movie_url, allow_redirects=True)
            open(jsonfilename, 'wb').write(rmovie_json.content)
    
    #prepare json var
    with open(jsonfilename, 'r') as f:
        json_movie = json.load(f)
    
    #make loop in json file
    for movie_json_result in json_movie['results']:
        print(movie_json_result['image'])
        movie_cover = movie_json_result['image']
        if debug:
            if path.exists(coverfilename):
                print ("file exist " + coverfilename)
            else:
                print ("Creating new " + coverfilename)
                get_cover = requests.get(movie_cover, allow_redirects=True)
                open(coverfilename, 'wb').write(get_cover.content)
    
    print
    

# ok time to make my huge html
#
# get loop for each 'extended/*.json' file and procced
onlyfiles = listdir(extendeddirectory)

mycounter = 0 #counter to display a table 4 times per row
htmlsource = ""

for json_ext_file in onlyfiles:
    print('Opening: ' + extendeddirectory + json_ext_file)

    with open(extendeddirectory + json_ext_file, 'r') as f:
        json_movie = json.load(f)

    imdb_id = json_movie['imdb_id'].encode('utf-8')
    title = json_movie['title'].encode('utf-8')
    embed_url = json_movie['embed_url'].encode('utf-8')
    quality = json_movie['quality'].encode('utf-8')
    
    # now time to process other json in json/
    
    jsonfilename = jsondirectory + imdb_id + '.json'
    coverfilename = 'covers/' + imdb_id + '.jpg'
    
    print('Opening ' + jsonfilename)
    
    #prepare json var
    with open(jsonfilename, 'r') as f:
        json_movie = json.load(f)
    
    #make loop in json file
    for movie_json_result in json_movie['results']:
        orig_title = movie_json_result['title']
        orig_cover_url = movie_json_result['image']
        local_cover_url = coverfilename
        orig_description = movie_json_result['description']
    
    #time to display data in table
    if mycounter == 0:
        htmlsource += """
<table border="1" style="border-collapse: collapse; width: 100%;">
 <tbody>
  <tr>
"""
    htmlsource += """ 
   <td style="width: 25%;">
    <a href="{embed_url}">{orig_title}&nbsp;{orig_description}&nbsp;({quality})
     <img src="{local_cover_url}" alt="{orig_title}" width="320px" height="320px"/>
    </a>
   </td>
""".format(embed_url=embed_url, quality=quality ,orig_description=orig_description,local_cover_url=local_cover_url, orig_title=orig_title)
    mycounter = mycounter + 1
    if mycounter>3:
        mycounter = 0
        htmlsource += """
  </tr>
 </tbody>
</table>
"""


htmlsource += """
  </tr>
 </tbody>
</table>
"""       
print(htmlsource)
print('writing html_file: ' + html_file)
open(html_file, 'wb').write(htmlsource)

