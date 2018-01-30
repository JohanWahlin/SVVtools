# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:34:17 2017

@author: johwah
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 13:39:00 2017

@author: johwah
"""
import pandas as pd
import numpy as np
import fnmatch
import os
import codecs
import datetime



def parse_dau(filename,add_geometry=False):
        def trial(a):
            if a==None:
                return(0)
            else:
                return(a)
        data=[]
        file = codecs.open(filename, 'rb', 'cp1252')
        i = 0
        for nextline in file:
            i += 1     
            if i==1:
                line=nextline #Each line has the starting point of a line. The end point is found on next line. This is why we need to lines throughout the function
            else:
                line_columns=line.split(';') 
                code=line_columns[0] #reads the first column of the file, used to determine what to read and how

                if code =='DAU': #identifies file as DAU
                    pass#The start of a DAU file. Not much to do with this, as long as we feed the function with proper dau-files
                elif code == '0001': #indentifies beginning of file
                    pass#print('BOF')
                elif code == '931100': #identifies a VINTERMAN header containing vehicle_id. Vinterman headers can show up on any line in a file.
                    vehicle_id=line_columns[3][0:-2] #vehicle ID is found in the 4th column of a VINTERMAN header
                    header_date=line_columns[1]
                    header_time=line_columns[2]
                elif code == '931105' or code == '931106' or code == '931107' or code == '931108':  # These are different versions of the DAU format, and should be parsed differently
                    line = line.replace(',','.')
                    line = line.strip()
                    line = line.replace('INF','')
                    nextline = nextline.replace(',','.')
                    nextline=nextline.strip()
                    stat=line_columns[3]  #extract the measurement status. If 'begin' it is the first line of a "measurement". If 'end' it is the last line, and thereby the end point of a "measurement"
                    splitted_nextline=nextline.split(';') #extracts the length of the following line
                    
                    #data comes as "stretches" along the road. Starting point of a stretch is given in current line, 
                    #and the ending point in next line. Lines with an 'end' status, are end points of stretches and have no values to collect from next line. 
                    # In some cases the 'end' status is not reported, in such cases we check that the following line actually contains data (longer than 28 columns).
                    # If not, we threat the current line as the end-point
                    if (stat!='End' and len(splitted_nextline)>28): 
                        ''' Different read-patterns depending on the elrapp dau data version'''
                        if code =='931105':
                            (code, date, time, status,lat,lon,dist,speed,dist_m_spreder_torr,sprederbredde_torr,
                             dosering_torr,prc_vatstoff_tillsatt,teo_mengde_torrstoff,tot_bruk_vatstoff,torr_spreder_bruk_bool,
                             plog_nede_bool,sprederbredde_vat,dosering_vat,teo_mengde_vatstoff,dist_m_spreder_vat,
                             vat_spreder_bruk_bool,spredesymmetri,forventet_bruk_torr,forventet_bruk_vat,saltrester,
                             material_type,friktion,vegtemp,lufttemp,luftfukt, vegforhold,vaerforhold,skydekke,
                             sensorer_paskrudd, vegref)=[(x if x!='' else None) for x in line.split(';')]
                            
                            # Finds the end-point of this row (start point in next row)
                            splitted_nextline=nextline.split(';')
                            next_vegref=splitted_nextline[34]
                            next_dist=splitted_nextline[6]
                            
                            hovel_nede_bool=None
                            midskjer_nede_bool=None
                            sideplog_bruk_bool=None
                            mengd_torrt_veiesys=None
                            mengd_vatt_veiesys=None
                        
                        if code =='931106':
                            (code, date, time, status,lat,lon,dist,speed,dist_m_spreder_torr,sprederbredde_torr,
                             dosering_torr,prc_vatstoff_tillsatt,teo_mengde_torrstoff,tot_bruk_vatstoff,torr_spreder_bruk_bool,
                             plog_nede_bool,sprederbredde_vat,dosering_vat,teo_mengde_vatstoff,dist_m_spreder_vat,
                             vat_spreder_bruk_bool,spredesymmetri,forventet_bruk_torr,forventet_bruk_vat,saltrester,
                             material_type,friktion,vegtemp,lufttemp,luftfukt, vegforhold,vaerforhold,skydekke,
                             sensorer_paskrudd, vegref,hovel_nede_bool)=[(x if x!='' else None) for x in line.split(';')]
                            
                            # Finds the end-point of this row (start point in next row)
                            splitted_nextline=nextline.split(';')
                            next_vegref=splitted_nextline[34]
                            next_dist=splitted_nextline[6]
                            
                            midskjer_nede_bool=None
                            sideplog_bruk_bool=None
                            mengd_torrt_veiesys=None
                            mengd_vatt_veiesys=None
                    
                        if code =='931107':
                            (code, date, time, status,lat,lon,dist,speed,dist_m_spreder_torr,sprederbredde_torr,
                             dosering_torr,prc_vatstoff_tillsatt,teo_mengde_torrstoff,tot_bruk_vatstoff,torr_spreder_bruk_bool,
                             plog_nede_bool,sprederbredde_vat,dosering_vat,teo_mengde_vatstoff,dist_m_spreder_vat,
                             vat_spreder_bruk_bool,spredesymmetri,forventet_bruk_torr,forventet_bruk_vat,saltrester,
                             material_type,friktion,vegtemp,lufttemp,luftfukt,vegforhold,vaerforhold,skydekke,
                             sensorer_paskrudd, vegref,hovel_nede_bool,midskjer_nede_bool,
                             sideplog_bruk_bool)=[(x if x!='' else None) for x in line.split(';')]
                            
                            # Finds the end-point of this row (start point in next row)
                            splitted_nextline=nextline.split(';')
                            next_vegref=splitted_nextline[34]
                            next_dist=splitted_nextline[6]
                            
                            mengd_torrt_veiesys=None
                            mengd_vatt_veiesys=None
                            #print('Allt OK så långt')
                            
                        if code =='931108':
                            (code, date, time, status,lat,lon,dist,speed,dist_m_spreder_torr,sprederbredde_torr,
                             dosering_torr,prc_vatstoff_tillsatt,teo_mengde_torrstoff,tot_bruk_vatstoff,torr_spreder_bruk_bool,
                             plog_nede_bool,sprederbredde_vat,dosering_vat,teo_mengde_vatstoff,dist_m_spreder_vat,
                             vat_spreder_bruk_bool,spredesymmetri,forventet_bruk_torr,forventet_bruk_vat,saltrester,
                             material_type,friktion,vegtemp,lufttemp,luftfukt,vegforhold,vaerforhold,skydekke,
                             sensorer_paskrudd, vegref,hovel_nede_bool,midskjer_nede_bool,sideplog_bruk_bool,
                             mengd_torrt_veiesys,mengd_vatt_veiesys)=[(x if x!='' else None) for x in line.split(';')]
                            
                        # Finds the end-point of this row (start point in next row) and calculates segment distance
                        splitted_nextline=nextline.split(';')
                        next_date = splitted_nextline[1]
                        next_time = splitted_nextline[2]
                        next_vegref=splitted_nextline[34]
                        next_dist=splitted_nextline[6]
                        segm_length=float(next_dist)-float(dist)
                        next_lat=splitted_nextline[4]
                        next_lon=splitted_nextline[5]
                        next_teo_salt_dry=splitted_nextline[12]
                        next_teo_salt_wet=splitted_nextline[18]
                        next_timestamp=next_date[0:4]+'-'+next_date[4:6]+'-'+next_date[6:] +' '+next_time[0:2]+':'+next_time[2:4]+':'+next_time[4:]
                        #print(next_timestamp)
                    
                        '''Read data is then treated the same way, and written to db in the same way'''
                        if material_type != None:
                            material_type=float(material_type)
                        if plog_nede_bool != None:
                            if float(plog_nede_bool) not in [0,1,'0','1']:
                                plog_nede_bool=None
                        if torr_spreder_bruk_bool != None:
                            if float(torr_spreder_bruk_bool) not in [0,1]:
                                torr_spreder_bruk_bool=None
                        if vat_spreder_bruk_bool != None:
                            if float(vat_spreder_bruk_bool) not in [0,1]:
                                vat_spreder_bruk_bool=None
                        if hovel_nede_bool != None:
                            if float(hovel_nede_bool) not in [0,1]:
                                hovel_nede_bool=None
                        if midskjer_nede_bool != None:
                            if float(midskjer_nede_bool) not in [0,1]:
                                midskjer_nede_bool=None
                        if sideplog_bruk_bool != None:
                            if float(sideplog_bruk_bool) not in [0,1]:
                                sideplog_bruk_bool=None
                        
                        timestamp = date[0:4]+'-'+date[4:6]+'-'+date[6:] +' '+time[0:2]+':'+time[2:4]+':'+time[4:] #date and time into sql timestamp
                        header_timestamp = header_date[0:4]+'-'+header_date[4:6]+'-'+header_date[6:] +' '+header_time[0:2]+':'+header_time[2:4]+':'+header_time[4:]
                        lat=float(lat)*180/np.pi #lat from radians to decimal degrees
                        lon=float(lon)*180/np.pi #lon from radians to decimal degrees
                        next_lat=float(next_lat)*180/np.pi #lat from radians to decimal degrees
                        next_lon=float(next_lon)*180/np.pi #lon from radians to decimal degrees
                        #print(timestamp)
                        seg_time=datetime.datetime.strptime(next_timestamp,'%Y-%m-%d %H:%M:%S')-datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S') # in deltatime
                        seg_time=seg_time.total_seconds() #segment time in seconds
                        
                        #try:
                            #seg_dry=(float(dosering_torr)*float(sprederbredde_torr)/100*segm_length*1000)/1000 #kg
                        #    seg_dry=
                        #except:
                        #    seg_dry=None
                        #try:
                        #    seg_solution=(float(dosering_vat)*float(sprederbredde_vat)/100*segm_length*1000)/1000 #liter
                        #except:
                        #    seg_solution=None
                        try:
                            seg_teodry_amount=float(next_teo_salt_dry)-float(teo_mengde_torrstoff)
                        except:
                            seg_teodry_amount=None

                        try:
                            seg_teowet_amount=float(next_teo_salt_wet)-float(teo_mengde_vatstoff)
                        except:   
                            seg_teowet_amount=None

                        if seg_teowet_amount!=None:
                            if np.isnan(seg_teowet_amount):
                                print([filename,timestamp, status,sprederbredde_torr,dosering_torr,teo_mengde_torrstoff,torr_spreder_bruk_bool,
                                                                             sprederbredde_vat,dosering_vat,teo_mengde_vatstoff,vat_spreder_bruk_bool,
                                                                             material_type,mengd_torrt_veiesys,mengd_vatt_veiesys,segm_length,seg_time,seg_dry_salt,seg_solution,seg_teodrysalt,seg_teowetsalt])
                        

                                
                        if segm_length>0:
                            if trial(seg_teodry_amount)/segm_length>500 or trial(seg_teowet_amount)/segm_length>200:
                                flag=1.0
                            else:
                                flag=0.0
                        else:
                            flag=2.0
                        
                        
                        '''append data to list'''
                        data.append([filename,header_timestamp,vehicle_id,code, timestamp, status,lat,lon,next_lat, next_lon,speed,sprederbredde_torr,
                                                                         dosering_torr,prc_vatstoff_tillsatt,torr_spreder_bruk_bool,
                                                                         plog_nede_bool,sprederbredde_vat,dosering_vat,
                                                                         vat_spreder_bruk_bool,spredesymmetri,material_type, vegref,next_vegref,hovel_nede_bool,midskjer_nede_bool,sideplog_bruk_bool,
                                                                         mengd_torrt_veiesys,mengd_vatt_veiesys,segm_length,seg_time,seg_teodry_amount,seg_teowet_amount,flag])

                    else: #if line status=end, then those parameters will not be connected to anything, and hence we won't need it.
                        pass
                elif code == '0002':
                    pass#print('EOF')
                else:
                    pass

                
                #conn.commit()
                
                line=nextline
        df=pd.DataFrame(data,columns=['filename','header_time','vehicleID','DAUKod','Tid','start_stop','start_lat','start_lon','end_lat','end_lon',
                                    'Hastighet','Sprederbredde_Torr','Spredermengde_Torr','Befuktning_torrstoff_prc','TorrsprederAktiv','PlogAktiv',
                                    'Sprederbredde_Vat','Spredermengde_Vat','VatsprederAktiv','Spredesymmetri','MaterialType_kode','from_vegref',
                                    'to_vegref','graderblade_active','midtskjaer_active','sideplog_active','dry_amount_weightsys','wet_amount_weightsys',
                                    'segment_length','SegmentTime','Segment_TheoDrySalt','Segment_TheoSolution','Flag'])	
        
        pd.set_option('use_inf_as_na', True)
        #df[df.isnull()]=np.nan
        df=df.where(pd.notnull(df), None)
        #df.replace([np.inf, -np.inf],None, inplace=True)
        #df.replace([np.nan],None, inplace=True)
        #df.fillna(value=ara, inplace=True)
        return(df)
