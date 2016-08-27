import xbmcaddon, util, urllib2, string, json

addon = xbmcaddon.Addon('plugin.video.nottstv')


#util.playMedia(addon.getAddonInfo('name'),addon.getAddonInfo('icon'),'http://c.brightcove.com/services/mobile/streaming/index/rendition.m3u8?assetId=4135572682001')
def playEpisode(id,thumb):
    url = "http://api.brightcove.com/services/library?command=find_video_by_id&video_id=" + id + "&video_fields=name,length,iosrenditions&token=1N4JCL3KisuyvNlDIPdrJGpatQ1dVXuaCRtD88vFyCqx6Va1G_yGtg..&sort_by=encodingRate:asc"
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        videolinks = json.loads(content)
        util.playMedia(videolinks['name'],thumb,videolinks['IOSRenditions'][0]['url'])
    else:
        util.showError('plugin.video.nottstv', 'Could not open URL %s to create menu' % (url))	
    pass
def getTaggedEpisodes(tag):
    if tag == "now%20and%20then":
        url = "http://api.brightcove.com/services/library?command=search_videos&token=1N4JCL3KisuyvNlDIPdrJGpatQ1dVXuaCRtD88vFyCqx6Va1G_yGtg..&video_fields=id,name,videoStillURL,tags&sort_by=start_date:desc&any=custom_fields:" + tag
    elif tag == "channel%208%20debate":
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
        util.showError('plugin.video.nottstv', 'Could not open URL %s to create menu' % (url))	
    pass

def playVideo(params):
    pass
def listEpisodes(tag):
    getTaggedEpisodes(tag.replace("-","%20").replace("/",""))
    pass

def buildMenu():
    path = addon.getAddonInfo('path')
    params={'programme':1}
    params['label']= "Notts TV News Reports"
    params['tag']="news"
    link = util.makeLink(params)
    util.addMenuItem(params['label'], link, 'news.png', path + '/images/news.png', True)
    util.addMenuItem("The 6:30 Show", util.makeLink({'programme':1,'tag':'the-630-show'}), None, path + '/images/630show.png', True)
    util.addMenuItem("Notts TV Debate", util.makeLink({'programme':1,'tag':'notts-tv-debate'}), None, path + '/images/8debate.png', True)
    util.addMenuItem("Sports Week", util.makeLink({'programme':1,'tag':'sports-week'}), None, path + '/images/sportsweek.png', True)
    util.addMenuItem("City of Football", util.makeLink({'programme':1,'tag':'city-of-football'}), None, path + '/images/cityoffootball.png', True)
    util.addMenuItem("Day in the Life", util.makeLink({'programme':1,'tag':'day-in-the-life'}), None, path + '/images/dayinthelife.png', True)
    util.addMenuItem("Digital Nation", util.makeLink({'programme':1,'tag':'digital-nation'}), None, path + '/images/digitalnation.png', True)
    util.addMenuItem("F-Stop", util.makeLink({'programme':1,'tag':'f-stop'}), None, path + '/images/fstop.png', True)
    util.addMenuItem("Inside Industry Week", util.makeLink({'programme':1,'tag':'inside-industry-week'}), None, path + '/images/insideindustry.png', True)
    util.addMenuItem("Noise Floor", util.makeLink({'programme':1,'tag':'noise-floor'}), None, path + '/images/noisefloor.png', True)
    util.addMenuItem("Nottingham Now and Then", util.makeLink({'programme':1,'tag':'nottingham-now-and-then'}), None, path + '/images/nowandthen.png', True)
    util.addMenuItem("Sketch Up", util.makeLink({'programme':1,'tag':'sketch-up'}), None, path + '/images/sketchup.png', True)
    util.addMenuItem("Sounding Out", util.makeLink({'programme':1,'tag':'sounding-out'}), None, path + '/images/soundingout.png', True)
    util.addMenuItem("The Boot Room - Fan Zone", util.makeLink({'programme':1,'tag':'the-boot-room-fan-zone'}), None, path + '/images/bootroom.png', True)
    util.addMenuItem("The Boot Room - Pro Zone", util.makeLink({'programme':1,'tag':'the-boot-room-pro-zone'}), None, path + '/images/bootroom.png', True)
    util.addMenuItem("The Locker Room", util.makeLink({'programme':1,'tag':'the-locker-room'}), None, path + '/images/lockerroom.png', True)
    util.addMenuItem("Working Week", util.makeLink({'programme':1,'tag':'working-week'}), None, path + '/images/workingweek.png', True)
    util.addCategory('>> Current Affairs','current-affairs')
    util.addCategory('>> Entertainment','entertainment')
    util.addCategory('>> Lifestyle','lifestyle')
    util.addCategory('>> Sport','sport',path + '/images/sport.jpg')
    util.addCategory('>> Music','music')
    util.addCategory('>> Specials','specials')
    util.endListing()

    #else:
    #    util.showError('plugin.video.nottstv', 'Could not open URL %s to create menu' % (url))	
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


