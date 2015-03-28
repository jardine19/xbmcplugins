import xbmcaddon, util, urllib2, string, json
addon = xbmcaddon.Addon('plugin.video.eetv')

def showLiveTV():
    print "Show Live TV"
    ipaddress = addon.getSetting("ipaddress")
    playlist = "http://" + ipaddress + "/Live/Channels/getList?tvOnly=0&avoidHD=0&allowHidden=0&fields=name,id,zap,isDVB,hidden,rank,isHD,logo";
    print "Playlist at " + playlist
    response = urllib2.urlopen(playlist)
    if response and response.getcode() == 200:
        channels = json.loads(response.read())
        for channel in channels:
            if channel['hidden'] == False and (channel['zap'] < 225 or channel['zap'] > 300):
                params={'playlivetv':1}
                params['label']= str(channel['zap']) + ' ' + channel['name']
                params['url']= "http://" + ipaddress + "/Live/Channels/get?channelId=" + channel['id']
                params['id'] = channel['id']
                if channel.has_key('logo') == True:
                    params['thumb']= channel['logo']
                else:
                    params['thumb']= "http://" + ipaddress + "/Live/Channels/getLogo?zap=" + str(channel['zap'])
                params['zap']= channel['zap']
                thumb = params['thumb']
                util.addMenuItem(params['label'], util.makeLink(params), thumb, thumb, False)
        util.endListing()
    else:
        util.showError('plugin.video.nottstv', 'Could not open URL %s to create menu' % (url))	
    pass
def showRecordings():
    pass
def showArqivaMenu():
    util.addArqiva("CCTV News","http://stream.arqiva.tv/cctv-news",'thumbs/cctv_news.png')
    util.addArqiva("CCTV-4","http://stream.arqiva.tv/cctv-4",'/thumbs/cctv-4.png')
    util.addArqiva("CCTV-9 Documentary","http://stream.arqiva.tv/cctv-9",'/thumbs/cctv-9.png')
    util.addArqiva("Chatbox","http://stream.arqiva.tv/chatbox",'/thumbs/chat_box.png')
    util.addArqiva("Gay Network","http://stream.arqiva.tv/gaynet",'/thumbs/gay_network.png')
    util.addArqiva("Motors TV","http://stream.arqiva.tv/motorstv",'/thumbs/motors_tv_uk.png')
    util.addArqiva("QVC Beauty","http://stream.arqiva.tv/qvc-beau",'/thumbs/qvc_beauty.png')
    util.addArqiva("QVC Extra","http://stream.arqiva.tv/qvc-extra",'/thumbs/qvc_extra.png')
    util.addArqiva("QVC Plus","http://stream.arqiva.tv/qvc-plus",'/thumbs/qvc.png')
    util.addArqiva("QVC Style","http://stream.arqiva.tv/qvc-style",'/thumbs/qvc_style.png')
    util.addArqiva("Racing UK (Preview)","http://stream.arqiva.tv/racinguk",'/thumbs/racing_uk.png')
    util.addArqiva("RT Doc","http://stream.arqiva.tv/rt-doc",'/thumbs/rtd.png')
    util.addArqiva("SBN TV (Sonlife)","http://stream.arqiva.tv/sbntvuk",'/thumbs/sonlife.png')
    util.addArqiva("Vintage TV",'http://stream.arqiva.tv/vintagetv','/thumbs/vintage_tv.png')
    util.endListing()
    pass
def showMainMenu():
    params={'livetv':1,'foo':'bar'}
    link = util.makeLink(params)
    util.addMenuItem('Live TV.', link, 'DefaultVideo.png', 'DefaultVideo.png', True)

    params={'arqivamenu':1}
    link = util.makeLink(params)
    util.addMenuItem('Arqiva Connect', link, 'DefaultVideo.png', 'DefaultVideo.png', True)
    params={'recordings':1}
    link = util.makeLink(params)
    util.addMenuItem('Recordings', link, 'DefaultVideo.png', 'DefaultVideo.png', True)
    util.endListing()
    pass

    
parameters = util.parseParameters()
print "Running"
print parameters
if 'play' in parameters:
    playVideo(parameters['play'])
elif 'arqiva' in parameters:
    util.playArqiva(parameters)
elif 'recordings' in parameters:
    showRecordings(parameters)
elif 'livetv' in parameters:
    showLiveTV()
elif 'playlivetv' in parameters:
    util.playEE(parameters)
elif 'programme' in parameters:
    listEpisodes(parameters['tag'])
elif 'episode' in parameters:
    playEpisode(parameters['id'],parameters['thumb'])
elif 'arqivamenu' in parameters:
    showArqivaMenu()
else:
    showMainMenu()