import json, os
import requests
from os import path
from os import listdir
from os.path import isfile, join
from string import Template
import time
import warnings
from PIL import Image

#disable bomwarning warning
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

#DOWNLOAD
DOWNLOAD = 0

#VERBOSE mode
VERBOSE = 1 #show console status

# if you want thumbnails as covers (using local files)
USETHUMBNAILS = 0

# if you want to use original external urls for covers
USEEXTERNALCOVER = 0

#thumbnail resolutions
THUMBNAILMAX_X = 400
THUMBNAILMAX_Y = 400

MOVIEURLFILENAME = "movies-latest.json"
SERIESFILENAME = "series-latest.json"

MOVIECOVERURLORIGINALPREFIX = '-original' #used as ttXXXXXX-original.json for each movie

ORIGINALDIRECTORY = 'original/'
HTMLHTMLCOVERDIRECTORY = 'html/covers/'
JSONDIRECTORY = 'json/'
HTMLDIRECTORY = 'html/'

HTML_FILE = HTMLDIRECTORY + 'index-' + time.strftime("%Y%m%d") + '.html'

if VERBOSE: print('Trying in to create HTMLDIRECTORY: ' + HTMLDIRECTORY)

#check if directory HTML exist
if os.path.isdir(HTMLDIRECTORY):
    if VERBOSE: print ("directory exist " + HTMLDIRECTORY)
else:
    #create directory
    os.mkdir(HTMLDIRECTORY)

if os.path.isdir(ORIGINALDIRECTORY):
    if VERBOSE: print ("directory exist " + ORIGINALDIRECTORY)
else:
    os.mkdir(ORIGINALDIRECTORY)

if os.path.isdir(HTMLHTMLCOVERDIRECTORY):
    if VERBOSE: print ("directory exist " + HTMLHTMLCOVERDIRECTORY)
else:
    os.mkdir(HTMLHTMLCOVERDIRECTORY)
    
if os.path.isdir(JSONDIRECTORY):
    if VERBOSE: print ("directory exist " + JSONDIRECTORY)
else:
    os.mkdir(JSONDIRECTORY)

    
#your https://imdb-api.com/ api id, gets your there
#there is a free one for 100 request a day
apiid = 'k_lir8ah97'

if DOWNLOAD:
    if VERBOSE: print('Skipping DOWNLOAD of new json files')
else:
    #os.system('rm *.json')
    
    urlmovies = 'https://vidsrc.me/movies/latest/page-1.json'
    urlseries = 'https://vidsrc.me/episodes/latest/page-1.json'

    rmovies = requests.get(urlmovies, allow_redirects=True)
    open(MOVIEURLFILENAME, 'wb').write(rmovies.content)

    rseries = requests.get(urlseries, allow_redirects=True)
    open(SERIESFILENAME, 'wb').write(rseries.content)

#using wget (not using it)
#os.system('rm *.json')
#os.system('wget -O movies-latest.json https://vidsrc.me/movies/latest/page-1.json&> /dev/null 2>&1')
#os.system('wget -O series-latest.json https://vidsrc.me/episodes/latest/page-1.json&> /dev/null 2>&1')






with open(MOVIEURLFILENAME, 'r') as f:
    json_movies = json.load(f)

with open(SERIESFILENAME, 'r') as f:
    json_series = json.load(f)
    
#if VERBOSE: print( distros_dict)

#if VERBOSE: print(json.dumps(json_movies, indent = 4, sort_keys=True))

if VERBOSE: print(' Number of Pages:  ' + str(json_movies['pages']))
if VERBOSE: print('Number of Series: ' + str(json_series['pages']))

# Load the json data into a variable
#storedata = json.loads(json_movies)

# Iterate the for loop to if VERBOSE: print the data with key
#for val in storedata:
#  if VERBOSE: print("%s: %s" % (val, storedata[val]))

for result in json_movies['result']:
    if VERBOSE: print("processing: " + json.dumps(result))
    
    individualmoviejson = ORIGINALDIRECTORY + result['imdb_id'] + MOVIECOVERURLORIGINALPREFIX + '.json'
    
    if path.exists(individualmoviejson):
        if VERBOSE:
            print ("file exist " + individualmoviejson)
    else:
        if VERBOSE: print ("Creating new " + individualmoviejson)
        resultdicttostring = json.dumps(result)

        #open(SERIESFILENAME, 'wb').write(rseries.content)
        #open(jsonfilename, 'wb').write(rmovie_json.content)

        open(individualmoviejson, 'w+').write(resultdicttostring)

    if VERBOSE: print('imdb_id: ' + result['imdb_id'])
    
    ttid_string = result['imdb_id']
    
    if VERBOSE: print('  Title: ' + result['title'])
    if VERBOSE: print('Quality: ' + result['quality'])
    if VERBOSE: print('embed_url: ' + result['embed_url'])
    
    #get poster and more
    htmlfilename = HTMLDIRECTORY + ttid_string + '.html'
    jsonfilename = JSONDIRECTORY + ttid_string + '.json'
    coverfilename = HTMLHTMLCOVERDIRECTORY + ttid_string + '.jpg'
    coverfilenameThumbnail = HTMLHTMLCOVERDIRECTORY + ttid_string + '-thumbnail.jpg'
    
    movie_url = 'https://imdb-api.com/API/Search/' + apiid + '/' + ttid_string
    if VERBOSE: print('Processing Search URL: ' + movie_url)
    #request data
    
    #hold request for now, since i only have 100 per day
    if path.exists(jsonfilename):
        if VERBOSE: print ("file exist " + jsonfilename)
    else:
        if VERBOSE: print ("Creating new " + jsonfilename)
        rmovie_json = requests.get(movie_url, allow_redirects=True)

        # check if limit has been reach
        #if results['errorMessage']:
        #    print('Error Processing: ' + results['errorMessage'])
        #else:
        print(type(individualmoviejson))
    
        with open(individualmoviejson, 'r') as f:
            try:
                json_movie = json.load(f)
                if VERBOSE: print('Success json.load(' + individualmoviejson + ')')
                #check if is a valid request or error been found
                if isinstance(json_movie['results'], list):
                    #it is, save it
                    if VERBOSE: print('Writing: ' + individualmoviejson)
                    open(individualmoviejson, 'wb').write(rmovie_json.content)
                else:
                    #error found!
                    if VERBOSE: print('Error in ' + individualmoviejson + ': ' + json.dumps(rmovie_json))


            except:
                if VERBOSE: print('Fail json.load(' + individualmoviejson + ')')
                print("TypeError: 'NoneType' object is not iterable")

    #prepare json var
    if VERBOSE: print('\nPreparing: ' + individualmoviejson)
    
    
    #make loop in json file
    if isinstance(json_movie['results'], list):
        for movie_json_result in json_movie['results']:
            try:
                if VERBOSE: print('Processing' + json.dumps(movie_json_result))
                #get cover to local storage
                if VERBOSE: print(movie_json_result['image'])

                movie_cover = movie_json_result['image']
                if path.exists(coverfilename):
                    if VERBOSE: print ("file exist " + coverfilename)
                else:
                    if VERBOSE: print ("Creating new " + coverfilename)
                    get_cover = requests.get(movie_cover, allow_redirects=True)
                    open(coverfilename, 'wb').write(get_cover.content)

                # create a thumbnail
                # creating a object
                if path.exists(coverfilenameThumbnail):
                    if VERBOSE: print ('Thumbnail file exist: ' + coverfilenameThumbnail)
                else:
                    if VERBOSE: print ('Creating new Thumnail file: ' + coverfilenameThumbnail)
                    image = Image.open(coverfilename) 
                    MAX_SIZE = (THUMBNAILMAX_X, THUMBNAILMAX_Y) 

                    image.thumbnail(MAX_SIZE) 
  
                    # creating thumbnail
                    image.save(coverfilenameThumbnail) 
            except TypeError:
                if VERBOSE: print('Fail json.load(' + individualmoviejson + ')')
                print("TypeError: 'NoneType' object is not iterable")
           
            if VERBOSE: print
    else:
        if VERBOSE: print('Fail to create file! ' + individualmoviejson)
    

# ok time to make my huge html
#
# get loop for each 'original/*.json' file and procced
onlyfiles = listdir(ORIGINALDIRECTORY)

mycounter = 0 #counter to display a table 4 times per row
htmlsource = ""

for json_ext_file in onlyfiles:
    if VERBOSE: print('Opening: ' + ORIGINALDIRECTORY + json_ext_file)

    with open(ORIGINALDIRECTORY + json_ext_file, 'r') as f:
        json_movie = json.load(f)

    imdb_id = json_movie['imdb_id']
    title = json_movie['title']
    embed_url = json_movie['embed_url']
    quality = json_movie['quality']
    
    # now time to process other json in json/
    
    jsonfilename = format(JSONDIRECTORY + imdb_id + '.json').encode()
    coverfilename = 'covers/' + imdb_id + '.jpg'
    thumbnail_local_cover_url = 'covers/' + imdb_id + '-thumbnail.jpg'
    
    if VERBOSE:
        #check if jsonfilame is not from unicode to bytes.
        if not isinstance(jsonfilename, bytes):
            jsonfilename = jsonfilename
            
        print(jsonfilename)

    #prepare json var
    with open(jsonfilename, 'r') as f:
        json_movie = json.load(f)
    
    #make loop in json file
    for movie_json_result in json_movie['results']:
        orig_title = movie_json_result['title']
        orig_cover_url = movie_json_result['image']
        local_cover_url = coverfilename
        orig_description = movie_json_result['description']
    
    # check if using local-thumbnail for cover, if does then make local_cover_url = thumbnail_local_cover_url
    if USETHUMBNAILS:
        local_cover_url = thumbnail_local_cover_url
    
    #overwrite covers is USEEXTERNALCOVER with external cover
    if USEEXTERNALCOVER:
        local_cover_url = orig_cover_url
        
        
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
#if VERBOSE: print(htmlsource)
if VERBOSE: print('writing HTML_FILE: ' + HTML_FILE)
open(HTML_FILE, 'wb').write(htmlsource)

print('program end')


