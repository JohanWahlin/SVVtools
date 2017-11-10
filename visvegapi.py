import requests

def make_request(req,proxy):
	r=requests.get(req,proxies=proxy)
	return(r)




def road_along_route(start_lat, start_lon, end_lat, end_lon, datum,road_category='',roadnum='',road_status='', topology_level=''):
	base_url='http://visveginfo-static.opentns.org/RoadInfoService/'
	function='GetRoadDataAlongRouteBetweenLocations?'

	#build requetss for manatory parameters
	from_to='startEasting='+str(start_lon)+'&startNorthing='+str(start_lat)+'&endEasting='+str(end_lon)+'&endNorthing='+str(end_lon)
	when='&viewDate='+datum

	#requests for optional parameters
	if topology_level:
		topolevel='&TopologyLevel='+topology_level
	else:
		topolevel=''
	if roadnum:
		vegnum='&SearchRoadNumber='+roadnum
	else:
		vegnum=''
	if road_category:
		vegkat='&SearchRoadCategories='+road_category
	else:
		vegkat=''
	if road_status:
		vegstatus='&SearchRoadCategories='+road_status
	else:
		vegstatus=''    

	#complete request:
	req=base_url+function+from_to+when+vegkat+vegnum+vegstatus+topolevel
	
	proxy={'http':'http://proxy.vegvesen.no:8080'} #when inside firewall
	# Send request to visveg-api:
	data=make_request(req,proxy)
	return(data)