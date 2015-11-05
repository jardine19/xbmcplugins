import xbmcaddon, util, urllib2, string, json, datetime
addon = xbmcaddon.Addon('plugin.video.eetv')

def showLiveTV():
	ipaddress = addon.getSetting("ipaddress")
	if ipaddress == '':
		xbmc.executebuiltin('XBMC.Notification(Info:,"IP Address Not Set",3000,'+addon.getAddonInfo('icon')+')')
	else:
		playlist = "http://" + ipaddress + "/Live/Channels/getList?tvOnly=0&avoidHD=0&allowHidden=0&fields=name,id,zap,isDVB,hidden,rank,isHD,logo"
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
			util.notify('plugin.video.eetv', 'Could not open URL %s to create menu' % (url))	
	pass
def playRecording(params):
	ipaddress = addon.getSetting("ipaddress")
	recording = "http://" + ipaddress + "/PVR/Records/session?recordId=" + str(params['id'])
	response = urllib2.urlopen(recording)
	if response and response.getcode() == 200:
		ticket = json.loads(response.read())
		if ticket.has_key('pcLockReason'):
			util.notify('plugin.video.eetv',"Unable to Play " + ticket['pcLockReason'])
		else:
			url = "http://" + ipaddress + "/PVR/Records/getVideo?sessionId=" + ticket['id']
			params['url'] = url
			params['label'] = params['label']
			params['thumb'] = params['icon']
			util.playEE(params)
	else:
		util.notify('plugin.video.eetv', 'Could not Get Playback Token' % (url))	
	pass
def showRecordings(show_series):
	ipaddress = addon.getSetting("ipaddress")
	if ipaddress == '':
		xbmc.executebuiltin('XBMC.Notification(Info:,"IP Address Not Set",3000,'+addon.getAddonInfo('icon')+')')
	else:
		recordings = "http://" + ipaddress + "/PVR/Records/getList?type=regular&avoidHD=0&tvOnly=0"
		try:
			response = urllib2.urlopen(recordings)
			if response and response.getcode() == 200:
				path = addon.getAddonInfo('path')
				recordings = json.loads(response.read())
				recordings_array = []
				known_series = {}
				# Need to sort by event.name
				for rec in recordings:
					if rec['event'].has_key('serieId'):
						series_id = rec['event']['serieId']
					else:
						series_id = "n/a"
					if series_id == show_series or (series_id == 'n/a' and show_series == 'no'):
						# Showing the series I wish to show, or the episode was not in a series, therefore we want to show the episode
						params={'playrecording':1}
						params['id'] = rec['id']
						if rec['event'].has_key('icon'):
							params['icon'] = rec['event']['icon']
						else:
							params['icon'] = "DefaultVideo.png"
						
						if rec['event'].has_key('description'):
							params['plot'] = rec['event']['description']
						else:
							params['plot'] = ""
						params['label'] = rec['event']['name']
						start = datetime.datetime.fromtimestamp(rec['event']['startTime'])
						start = start.strftime("%d/%m/%Y %H:%M")
						params['label'] = params['label'] + " : " + start
						start = datetime.datetime.fromtimestamp(rec['event']['startTime'])
						start = start.strftime("%Y-%m-%d %H:%M")
						params['sort_label'] = params['label'] + " : " + start
						recordings_array.append(params)
					elif known_series.has_key(series_id) == False and show_series == 'no':
						# Showing a placeholder to the series menu
						params={'recordings':series_id}
						params['id'] = rec['id']
						if rec['event'].has_key('icon'):
							params['icon'] = rec['event']['icon']
						else:
							params['icon'] = "DefaultVideo.png"
						
						if rec['event'].has_key('description'):
							params['plot'] = rec['event']['description']
						else:
							params['plot'] = ""
						params['label'] = rec['event']['name'] + " >> "
						params['sort_label'] = params['label']
						recordings_array.append(params)
						known_series[series_id] = True

				recordings_array.sort(key=lambda x: x['sort_label'], reverse=False)
				for rec in recordings_array:
					print rec['label'] + " : " + rec['sort_label']
					if rec.has_key('recordings'):
						isFolder = True
					else:
						isFolder = False
					util.addMenuItem(rec['label'], util.makeLink(rec), rec['icon'], rec['icon'], isFolder, rec['plot'])
				util.endListing()
			else:
				xbmc.executebuiltin('XBMC.Notification(Info:,"Is the EE Box Turned On?",3000,'+addon.getAddonInfo('icon')+')')
		except urllib2.HTTPError as e:
			reply = e.read()
			if reply.find('Error 503'):
				xbmc.executebuiltin('XBMC.Notification(Info:,"Looks like your EE box is in standby",3000,'+addon.getAddonInfo('icon')+')')
			else:
				xbmc.executebuiltin('XBMC.Notification(Info:,"Error : ' + reply + '",10000,'+addon.getAddonInfo('icon')+')')
			#xbmc.executebuiltin('XBMC.Notification(Info:,"HTTP ERROR Is the EE Box Turned On?",3000,'+addon.getAddonInfo('icon')+')')
			
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
	
	util.addArqiva("JSTV 1 (Promo)",'http://stream.arqiva.tv/vod/JSTV-1/jstv_promo_01.ts','/thumbs/jstv1.png')
	util.addArqiva("JSTV 2 (Promo)",'http://stream.arqiva.tv/vod/JSTV-2/jstv_promo_01.ts','/thumbs/jstv2.png')
	util.addArqiva("kykNET (Promo)",'http://stream.arqiva.tv/vod/KYKNET-MAIN/kykmain_promo_01.ts','/thumbs/kyknet.png')
	util.addArqiva("kykNET Musiek (Promo)",'http://stream.arqiva.tv/vod/KYKNET-MUZ/kykmuz_promo_01.ts','/thumbs/kyknetmusiek.png')
	util.addArqiva("abn",'http://stream.arqiva.tv/abntv','/thumbs/abn.png')
	util.addArqiva("Passion",'http://stream.arqiva.tv/passion','/thumbs/passion.png')
	util.addArqiva("Showcase",'http://stream.arqiva.tv/showcase','/thumbs/showcase.png')
	
	
	util.endListing()
	pass
def showMainMenu():
	params={'livetv':1,'foo':'bar'}
	link = util.makeLink(params)
	util.addMenuItem('Live TV', link, 'DefaultVideo.png', 'DefaultVideo.png', True)

	params={'arqivamenu':1}
	link = util.makeLink(params)
	util.addMenuItem('Arqiva Connect', link, 'DefaultVideo.png', 'DefaultVideo.png', True)
	params={'recordings':'no'}
	link = util.makeLink(params)
	util.addMenuItem('Recordings', link, 'DefaultVideo.png', 'DefaultVideo.png', True)
	util.endListing()
	pass

	
parameters = util.parseParameters()
if 'play' in parameters:
	playVideo(parameters['play'])
elif 'arqiva' in parameters:
	util.playArqiva(parameters)
elif 'recordings' in parameters:
	showRecordings(parameters['recordings'])
elif 'livetv' in parameters:
	showLiveTV()
elif 'playlivetv' in parameters:
	util.playEE(parameters)
elif 'playrecording' in parameters:
	playRecording(parameters)
elif 'programme' in parameters:
	listEpisodes(parameters['tag'])
elif 'episode' in parameters:
	playEpisode(parameters['id'],parameters['thumb'])
elif 'arqivamenu' in parameters:
	showArqivaMenu()
else:
	showMainMenu()