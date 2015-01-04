import re

####################################################################################################

PREFIX = "/video/laracasts"

NAME = "Laracasts"

MAIN_URL = "https://laracasts.com"

HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
}

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():

    # Setup the default breadcrumb title for the plugin
    ObjectContainer.title1 = NAME


# This main function will setup the displayed items.
# Initialize the plugin
@handler(PREFIX, NAME)
def MainMenu():
    oc = ObjectContainer()

    oc.add(DirectoryObject(key=Callback(Latest), title="Latest Screencasts"))
    oc.add(DirectoryObject(key=Callback(Series), title="Series"))

    return oc


@route(PREFIX + '/latest')
def Latest():
    html = getHTMLforPage('latest')
    items = html.xpath("//h3[contains(@class, 'lesson-block-title')]")

    oc = ObjectContainer()

    for item in items:
        title = item.xpath("a/@title")[0]
        url = item.xpath("a/@href")[0]
        oc.add(VideoClipObject(url=url, title=title, summary=""))

    return oc

@route(PREFIX + '/series')
def Series():
    html = getHTMLforPage('series')
    items = html.xpath("//div[contains(@class, 'lesson-block-inner')]")

    oc = ObjectContainer()

    for item in items:
        title = item.xpath("h3//a/@title")[0]
        url = item.xpath("h3//a/@href")[0]
        episode = url.replace("https://laracasts.com/series/", "")

        seriesImage =  "http:" + re.search(r"url(.[/]+(.[a-zA-Z0-9./-]+))", item.xpath("@style")[0]).group(0).replace('url(', '')

        Log(seriesImage)

        oc.add(DirectoryObject(key=Callback(Episodes, episode = episode), title=title, art=seriesImage))

    return oc


@route(PREFIX + '/series/episode')
def Episodes(episode = None):
    html = getHTMLforPage('series/' + episode)
    items = html.xpath("//td[contains(@class, 'episode-title')]")

    oc = ObjectContainer()

    for item in items:
        title = item.xpath("a/text()")[0]
        url = item.xpath("a/@href")[0]

        Log(title)

        oc.add(VideoClipObject(url=MAIN_URL + url, title=title, summary=""))

    return oc    



def getHTMLforPage(pageLink = None):
    return HTML.ElementFromURL(MAIN_URL +"/"+ pageLink, cacheTime=0, headers=HTTP_HEADERS)
