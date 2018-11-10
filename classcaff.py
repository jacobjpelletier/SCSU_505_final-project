#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:38:21 2018

@author: jacobpelletier
"""

class CaffCalc(object):

    
    def __init__(self, roast, size, time, age, smoke, hourstosleep):
        self.roast = roast
        self.size = size
        self.time = time
        self.age = age
        self.smoke = smoke
        self.hourstosleep = hourstosleep
        
    @classmethod
    def aboutcaffcalc(self):
        print('')
       
    def verify_roast(self):
        '''
        for use with html form
        '''
        try:
            if self.roast in ['blonde','medium','dark','other']:
                return True
        except:
            return False


    def verify_size(self):
        '''
        for use with html form
        '''
        try:
            if self.size in ['small','medium','large']:
                return True
        except:
            return False

    def verify_time(self):
        '''
        for use with html form
        '''
        try:
            if int(self.time) in range(0,23):
                return True
        except:
            return False

    def verify_age(self):
        '''
        for use with html form
        '''
        try:
            if int(self.age) in range(0,120):
                return True
        except:
            return False
            
    def verify_smoker(self):
        '''
        for use with html form
        '''
        try:
            if self.smoke in ['True','False']:
                return True
        except:
            return False
        
    def verify_hourstosleep(self):
        '''
        for use with html form
        '''
        try:
            if int(self.hourstosleep) in range(0,23):
                return True
        except:
            return False

    def getlastdose(self):
        return(self.lastdose)
    
    def getlasttime(self):
        return(self.lasttime)
    
    def getage(self):
        return(self.age)
    
    def getsmoke(self):
        return(self.smoke)
    
    def currentdose(self):
        
        ans = 0 
        dose = 0
        multiplier = 1.0
            
        if self.roast in ['blonde','medium','dark',]:
            if self.roast == 'blonde':
                dose = 475
            elif self.roast == 'medium':
                dose = 410
            elif self.roast == 'dark':
                dose = 340
            elif self.roast == 'other':
                dose = 300    
                
        if self.size in ['large','medium','small','none']:
                
            if self.roast in ['blonde','medium','dark']:
                if self.size == 'large':
                    multiplier = 1.00
                elif self.size == 'medium':
                    multiplier = 0.87
                elif self.size == 'small':
                    multiplier = 0.75
            else:
                if self.size == 'large':
                    multiplier = 1.00
                elif self.size == 'medium':
                    multiplier = 0.70
                elif self.size == 'small':
                    multiplier = 0.50
                 
                    
        ans = dose*multiplier
            
        if self.smoke == True:
            ans = ans*.5
        try:
            if int(self.age) >= 65:
                ans = ans*1.333
            elif int(self.age) <= 12:
                ans = 0
            
                return(None)
        except:
            pass
        # calculating expontential decay given dose and time
        ans = int(ans)*((0.5)**(int(self.time)/5))
        
        return int(ans)
    
    def futuredose(self):
        
        dose = (int(self.currentdose())+200)
        
        if self.getsmoke() == True:
            dose *= 0.5
        
        if int(self.getage()) >= 65:
            dose *= 1.33
            
        # calculating expontential decay given dose and time
        ans = int(dose)*((0.5)**(int(self.hourstosleep)/5))
        
        if ans > 175:
            return False
        else:
            return True
        
    def __str__(self):
        return(str(self.currentdose()))
        

    def __add__(self, other):
        return(int(self.currentdose())+(int(other)))
               
    def __sub__(self, other):
        return(int(self.currentdose())-(int(other)))

    def __mul__(self, other):
        return(int(self.currentdose())*(int(other)))
                   
    def __truediv__(self, other):
        return(int(self.currentdose())/(int(other)))

    def __int__(self):
        return(int(self.currentdose()))

    def __lt__(self, other):
        return(int(self.currentdose()) < other)        
        
    def __le__(self, other):
        return(int(self.currentdose()) <= other)
        
    def __eq__(self, other):
        return(int(self.currentdose()) == other)       
        
    def __ne__(self, other):
        return(int(self.currentdose()) != other)
        
    def __ge__(self, other):
        return(int(self.currentdose()) >= other)
        
    def __gt__(self, other):
        return(int(self.currentdose()) > other)
         
       