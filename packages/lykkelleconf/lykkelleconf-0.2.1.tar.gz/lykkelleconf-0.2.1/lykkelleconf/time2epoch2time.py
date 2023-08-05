#!/usr/bin/env python
# coding: utf-8
#dev complete and imported
#test complete and ready to be imported to prod. This is the final version
#prod deployed. this is the final version
# In[21]:


import time
import datetime

class epochtime:

#also add a class to it so it's easily computable or better still make it a module and import
    def date2epoch(date):
        hiredate= date
        pattern = '%d-%m-%Y'
        try:
            epoch = int(time.mktime(time.strptime(hiredate, pattern)))
            return epoch
        except ValueError:
            print("date format is not DD-MM-YYYY.moving to next item")
        except OverflowError:
            print("date format is before 1900.moving to next item")
    def epoch2date(epoch):
        try:
            ndate=datetime.date.fromtimestamp(epoch).strftime('%d-%m-%Y')
        except ValueError:
            print("epoch is wrong. moving to next item")
        except TypeError:
            print("encountered Type error as epoch returned was NULL")
        return ndate
    def epoch2dateeod(epoch):
        try:
            ndate=datetime.date.fromtimestamp(epoch).strftime('%Y-%m-%d')
        except ValueError:
            print("epoch is wrong. moving to next item")
            ndate = None
        except TypeError:
            print("encountered Type error as epoch returned was NULL")
            ndate = None
        return ndate
    def date2epocheod(date):
        hiredate= date
        pattern = '%Y-%m-%d'
        try:
            epoch = int(time.mktime(time.strptime(hiredate, pattern)))
            return epoch
        except ValueError:
            print("date format is not YYYY-MM-DD.moving to next item")
            ndate = None
        except OverflowError:
            print("date format is before 1900.moving to next item")
            ndate = None




