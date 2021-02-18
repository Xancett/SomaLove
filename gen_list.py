# <imports>
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from os import path
# </imports>

soma = "https://somafm.com/"
stationNames = []
stationURL = []


# Function for getting content
def Simple_Get(url):
    try: # Try to open the url for the content
        with closing(get(url, stream=True)) as resp:
            return resp.content
    except RequestException as e: # Return None if there was an error
        log_error('Error during request')
        return None

# Function to get the names of all stations
def GetStations(url):
    pageRequest = Simple_Get(url)
    page = BeautifulSoup(pageRequest, 'html.parser')
    for i, li in enumerate(page.select('li')):
        childTag = li.find('h3')
        if childTag:
            stationNames.append(childTag.text)
        childTag = li.find('a')
        if childTag:
            stationURL.append(childTag.get('href'))

# Function to get the links of all stations
def GetLinks(station):
    stationLinks = []
    pageRequest = Simple_Get(soma + station + 'directstreamlinks.html')
    page = BeautifulSoup(pageRequest, 'html.parser')
    for i, li in enumerate(page.select('p')):
        if (len(li.attrs) > 0):
            if ('Direct Server (Main)' in li.text):
                link = li.text.split('Direct Server (Main): ')[1]
                stationLinks.append(link)
    return stationLinks

# Function to output to a file
def WriteFiles():
    print("Writing...")
    WriteFile('128-aac')
    WriteFile('128-mp3')
    WriteFile('256-mp3')
    WriteFile('32-aac')
    WriteFile('64-aac')

def WriteFile(audio):
    output = open(audio + '.m3u', "w")
    # Write initial information
    output.write('#EXTM3U' + '\n')
    for i, q in enumerate(stationNames):
        #output.write('#EXTINF:-1, ' + stationNames[i] + '\n')
        stationLinks = GetLinks(stationURL[i])
        for x in stationLinks:
            if audio in x:
                output.write('#EXTINF:-1, ' + stationNames[i] + '\n')
                output.write(x + '\n')
    # Close file
    output.close()

GetStations(soma)
WriteFiles()
print("Completed")