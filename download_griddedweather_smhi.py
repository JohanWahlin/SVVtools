# -*- coding: utf-8 -*-
def download_griddedweather_smhi(from_datetime, to_datetime, prod, download_folder=''):
    '''a funciton to download dridded weather data from SMHI open data. For details about the data,
    see https://opendata.smhi.se/apidocs/grid/index.html. Dates should be in datetime format'''
    import requests
    import untangle
    import datetime
    #if type(from_datetime) is not datetime.datetime 
    
    def prod2num(prod):
        switcher={'MESAN':'4',
                 'AROME':'5',
                 'MESAN-A':'6'}
        return switcher[prod]
    base_url='http://opendata-download-grid-archive.smhi.se/feed/'
    #Finds all dates between start and end times
    dates=[]
    t_iter=from_datetime.date()
    while t_iter<=to_datetime.date():
        dates.append(t_iter)
        t_iter+=datetime.timedelta(days=1)
    #Builds request urls, make the request and reads filenames from response 
    dtype=prod2num(prod) #MESAN-A
downdownloaded_files=[]
    for d in dates:
        req_url=base_url+dtype+'/'+str(d.year)+'/'+str(d.month)+'/'+str(d.day)
        r=requests.get(req_url)
        cont=untangle.parse(r.content.decode("utf-8"))
        links={}
        for i in range(len(cont.feed.entry)):
            mod_time=datetime.datetime.strptime(cont.feed.entry[i].title.cdata[0:-3].strip(),'%Y-%m-%d %H:%M')
            if mod_time>=from_datetime and mod_time<=to_datetime:
                links[mod_time]=cont.feed.entry[i].id.cdata
                #print(mod_time)
        for date in links:
            req_file=requests.get(links[date],stream=True)
            filename=download_folder+prod+'_'+datetime.datetime.strftime(date,'%Y%m%d_%H%M')+'.grib' 
            open(filename, 'wb').write(req_file.content)
            downloaded_files.append(filename)
    return(downloaded_files)
            
