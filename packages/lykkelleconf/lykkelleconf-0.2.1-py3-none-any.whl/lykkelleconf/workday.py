#!/usr/bin/env python
# coding: utf-8
#successfully tested. ready to be deployed in Prod
#successfully deployed in Prod. this is the final version
# In[41]:


#finds the last workday from date assigned-1
import datetime as dt
import sys
import numpy as np
import pandas_market_calendars as mcal
class workday:
    date=None
    whol=None
    holilist=[]
#fucntion to store the list of holiays
    def holidays():
        us=mcal.get_calendar('NYSE')
        uk=mcal.get_calendar('LSE')
        eurex=mcal.get_calendar('EUREX')
        us_h=us.holidays()
        uk_h=uk.holidays()
        eurex_h=eurex.holidays()
        us_hol=np.asarray(us_h.holidays)
        uk_hol=np.asarray(uk_h.holidays)
        eurex_hol=np.asarray(eurex_h.holidays)
        hol=[us_hol,uk_hol,eurex_hol]
        holilist=[]
        for i in range (len(hol)):
            myhol=hol[i]
            #print(myhol[0:30])
            for j in range (len(myhol)):#len(myhol)
                edate=myhol[j]
                if int(edate.item().year)==int(dt.date.today().strftime("%Y")):
                    eday=edate.item().day
                    emonth=edate.item().month
                    ehol=str(eday)+"-"+str(emonth)
                    if ehol in holilist:
                        pass
                    else:
                        holilist.append(ehol)
                else:
                    pass;
        return holilist
#function to get the workday
    def __init__(self,date):
        #find the latest workday from input date
        #print("entry variable:",date)
        mlist=[6,7]
        # holilist=workday.holidays()
        try:
            datew=dt.datetime.strptime(date,'%Y-%m-%d').date()
        except ValueError:
            print("The date is wrong. Check format or date entry:",date)
            sys.exit(1)
        # print(datew)
        wday=datew.strftime("%d")
        # print(wday)
        wday = wday.lstrip('0')
        wmonth=datew.strftime("%m")
        wmonth = wmonth.lstrip('0')
        whol=wday+"-"+wmonth
        workday.whol=whol
        wd=datew.isoweekday()
        #print("workday:",wd)
        #print(mlist)
        #print(holilist)
        if (int(wd) in mlist):#or str(whol) in holilist
            recurs=1
        else:
            recurs=0
        #print("recurs:",recurs)
        if recurs==1:
            datew=datew-dt.timedelta(days=1)
            workday.date=datew
            #workday.holilist=holilist
            workday(str(datew))
        else:
            workday.whol=str(whol)
            #print("whole value:",whol,"value stored in self:",workday.whol)
            workday.date=str(datew)
            #workday.holilist=holilist

    def sdate(self):
        return self.date
    # def hlist(self):
    #     return self.holilist
    def hol(self):
        return self.whol






