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

#debug
debug = 0

#verbose mode
verbose = 1 #show console status

# if you want thumbnails as covers (using local files)
UseThumbnails = 1

# if you want to use original external urls for covers
UseExternalCover = 0

#thumbnail resolutions
thumbnailmaxX = 400
thumbnailmaxY = 400

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
    if verbose: print ("directory exist " + htmldirectory)
else:
    os.mkdir(htmldirectory)

if os.path.isdir(extendeddirectory):
    if verbose: print ("directory exist " + extendeddirectory)
else:
    os.mkdir(extendeddirectory)

if os.path.isdir(coverdirectory):
    if verbose: print ("directory exist " + coverdirectory)
else:
    os.mkdir(coverdirectory)
    
if os.path.isdir(jsondirectory):
    if verbose: print ("directory exist " + jsondirectory)
else:
    os.mkdir(jsondirectory)

    
#your https://imdb-api.com/ api id, gets your there
#there is a free one for 100 request a day
apiid = 'k_XXXXX'

if debug:
    if verbose: print('Skipping download of new json files')
else:
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
    
#if verbose: print( distros_dict)

#if verbose: print(json.dumps(json_movies, indent = 4, sort_keys=True))

if verbose: print(' Number of Pages:  ' + str(json_movies['pages']))
if verbose: print('Number of Series: ' + str(json_series['pages']))

# Load the json data into a variable
#storedata = json.loads(json_movies)

# Iterate the for loop to if verbose: print the data with key
#for val in storedata:
#  if verbose: print("%s: %s" % (val, storedata[val]))

for result in json_movies['result']:
    if verbose: print("processing: " + json.dumps(result))
    
    individualmoviejson = extendeddirectory + result['imdb_id'] + movieextendedprefix + '.json'
    
    if path.exists(individualmoviejson):
        if verbose:
            print ("file exist " + individualmoviejson)
    else:
        if verbose: print ("Creating new " + individualmoviejson)
        resultdicttostring = json.dumps(result)

        #open(fileseries, 'wb').write(rseries.content)
        #open(jsonfilename, 'wb').write(rmovie_json.content)

        open(individualmoviejson, 'w+').write(resultdicttostring)

    if verbose: print('imdb_id: ' + result['imdb_id'])
    
    ttid_string = result['imdb_id']
    
    if verbose: print('  Title: ' + result['title'])
    if verbose: print('Quality: ' + result['quality'])
    if verbose: print('embed_url: ' + result['embed_url'])
    
    #get poster and more
    htmlfilename = htmldirectory + ttid_string + '.html'
    jsonfilename = jsondirectory + ttid_string + '.json'
    coverfilename = coverdirectory + ttid_string + '.jpg'
    coverfilenameThumbnail = coverdirectory + ttid_string + '-thumbnail.jpg'
    
    movie_url = 'https://imdb-api.com/API/Search/' + apiid + '/' + ttid_string
    if verbose: print('Processing Search URL: ' + movie_url)
    #request data
    
    #hold request for now, since i only have 100 per day
    if path.exists(jsonfilename):
        if verbose: print ("file exist " + jsonfilename)
    else:
        if verbose: print ("Creating new " + jsonfilename)
        rmovie_json = requests.get(movie_url, allow_redirects=True)

        # check if limit has been reach
        #if results['errorMessage']:
        #    print('Error Processing: ' + results['errorMessage'])
        #else:
        print(type(individualmoviejson))
    
        with open(individualmoviejson, 'r') as f:
            try:
                json_movie = json.load(f)
                if verbose: print('Success json.load(' + individualmoviejson + ')')
                #check if is a valid request or error been found
                if isinstance(json_movie['results'], list):
                    #it is, save it
                    open(individualmoviejson, 'wb').write(rmovie_json.content)
                else:
                    #error found!
                    if verbose: print('Error in ' + individualmoviejson + ': ' + json.dumps(rmovie_json))


            except:
                if verbose: print('Fail json.load(' + individualmoviejson + ')')
                print("TypeError: 'NoneType' object is not iterable")

    #prepare json var
    if verbose: print('\nPreparing: ' + individualmoviejson)
    
    
    #make loop in json file
    if isinstance(json_movie['results'], list):
        for movie_json_result in json_movie['results']:
            try:
                if verbose: print('Processing' + json.dumps(movie_json_result))
                #get cover to local storage
                if verbose: print(movie_json_result['image'])

                movie_cover = movie_json_result['image']
                if path.exists(coverfilename):
                    if verbose: print ("file exist " + coverfilename)
                else:
                    if verbose: print ("Creating new " + coverfilename)
                    get_cover = requests.get(movie_cover, allow_redirects=True)
                    open(coverfilename, 'wb').write(get_cover.content)

                # create a thumbnail
                # creating a object
                if path.exists(coverfilenameThumbnail):
                    if verbose: print ('Thumbnail file exist: ' + coverfilenameThumbnail)
                else:
                    if verbose: print ('Creating new Thumnail file: ' + coverfilenameThumbnail)
                    image = Image.open(coverfilename) 
                    MAX_SIZE = (thumbnailmaxX, thumbnailmaxY) 

                    image.thumbnail(MAX_SIZE) 
  
                    # creating thumbnail
                    image.save(coverfilenameThumbnail) 
            except TypeError:
                if verbose: print('Fail json.load(' + individualmoviejson + ')')
                print("TypeError: 'NoneType' object is not iterable")
           
            if verbose: print
    else:
        if verbose: print('Fail to create file! ' + individualmoviejson)
    

# ok time to make my huge html
#
# get loop for each 'extended/*.json' file and procced
onlyfiles = listdir(extendeddirectory)

mycounter = 0 #counter to display a table 4 times per row
htmlsource = ""

for json_ext_file in onlyfiles:
    if verbose: print('Opening: ' + extendeddirectory + json_ext_file)

    with open(extendeddirectory + json_ext_file, 'r') as f:
        json_movie = json.load(f)

    imdb_id = json_movie['imdb_id']
    title = json_movie['title']
    embed_url = json_movie['embed_url']
    quality = json_movie['quality']
    
    # now time to process other json in json/
    
    jsonfilename = format(jsondirectory + imdb_id + '.json').encode()
    coverfilename = 'covers/' + imdb_id + '.jpg'
    thumbnail_local_cover_url = 'covers/' + imdb_id + '-thumbnail.jpg'
    
    if verbose:
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
    if UseThumbnails:
        local_cover_url = thumbnail_local_cover_url
    
    #overwrite covers is UseExternalCover with external cover
    if UseExternalCover:
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
#if verbose: print(htmlsource)
if verbose: print('writing html_file: ' + html_file)
open(html_file, 'wb').write(htmlsource)

print('program end')


