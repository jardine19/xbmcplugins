import xbmcaddon, util, urllib2, string, json

addon = xbmcaddon.Addon('plugin.video.eetv')


#util.playMedia(addon.getAddonInfo('name'),addon.getAddonInfo('icon'),'http://c.brightcove.com/services/mobile/streaming/index/rendition.m3u8?assetId=4135572682001')
def playEpisode(id,thumb):
    url = "http://api.brightcove.com/services/library?command=find_video_by_id&video_id=" + id + "&video_fields=name,length,iosrenditions&token=1N4JCL3KisuyvNlDIPdrJGpatQ1dVXuaCRtD88vFyCqx6Va1G_yGtg..&sort_by=encodingRate:asc"
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        videolinks = json.loads(content)
        util.playMedia(videolinks['name'],thumb,videolinks['IOSRenditions'][0]['url'])
    else:
        util.showError('plugin.video.eetv', 'Could not open URL %s to create menu' % (url))	
    pass
def getTaggedEpisodes(tag):
    if tag == "now%20and%20then":
        url = "http://api.brightcove.com/services/library?command=search_videos&token=1N4JCL3KisuyvNlDIPdrJGpatQ1dVXuaCRtD88vFyCqx6Va1G_yGtg..&video_fields=id,name,videoStillURL,tags&sort_by=start_date:desc&any=custom_fields:" + tag
    else:
        url = "http://api.brightcove.com/services/library?command=search_videos&token=1N4JCL3KisuyvNlDIPdrJGpatQ1dVXuaCRtD88vFyCqx6Va1G_yGtg..&video_fields=id,name,videoStillURL,tags&sort_by=start_date:desc&all=tag:" + tag
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        episodes = json.loads(content)
        for episode in episodes['items']:
            params={'episode':1}
            params['label']= episode['name']
            params['id']= episode['id']
            params['thumb']=episode['videoStillURL']
            thumb = episode['videoStillURL']
            link = util.makeLink(params)
            util.addMenuItem(params['label'], link, thumb, thumb, False)
        util.endListing()
    else:
        util.showError('plugin.video.eetv', 'Could not open URL %s to create menu' % (url))	
    pass

def playVideo(params):
    pass
def listEpisodes(tag):
    getTaggedEpisodes(tag.replace("-","%20").replace("/",""))
    pass

def buildMenu():
    url = "http://nottstv.com/programmes/"
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        params={'programme':1}
        params['label']= "EE TV"
        params['tag']="news"
        link = util.makeLink(params)
        util.addMenuItem(params['label'], link, 'DefaultVideo.png', 'DefaultVideo.png', True)
        programmes = util.extractAll(content, 'http://nottstv.com/programmes/','</a>')
        for programmelist in programmes:
            if "jQuery" in programmelist: continue
            programme = programmelist.split('">')
            if programme[1] == "Programmes": continue
            params={'programme':1}
            params['label']=programme[1]
            params['tag']=programme[0]
            link = util.makeLink(params)
            util.addMenuItem(params['label'], link, 'DefaultVideo.png', 'DefaultVideo.png', True)
        util.addCategory('>> Current Affairs','current-affairs')
        util.addCategory('>> Entertainment','entertainment')
        util.addCategory('>> Lifestyle','lifestyle')
        util.addCategory('>> Sport','sport')
        util.addCategory('>> Music','music')
        util.addCategory('>> Specials','specials')
        util.endListing()

    else:
        util.showError('plugin.video.eetv', 'Could not open URL %s to create menu' % (url))	
    pass

    
parameters = util.parseParameters()
if 'play' in parameters:
    playVideo(parameters['play'])
elif 'programme' in parameters:
    listEpisodes(parameters['tag'])
elif 'episode' in parameters:
    playEpisode(parameters['id'],parameters['thumb'])
else:
    buildMenu()


