#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 12:27:52 2018

@author: jacobpelletier
"""

import http.server
from urllib.parse import unquote, parse_qs
import os

# Class that performs work on user data
class CaffCalc(object):
    '''
    Initialization with attributes gathered from user input (no setter methods)
    1) use verify_X methods to verify user provided attribute X
    2) getter methods
    3) current dose and future dose calculators
    4) standard operator overloaders

    Object is represented by current dose value
    '''
    
    def __init__(self, roast, size, time, age, smoke, hourstosleep):
        self.roast = roast
        self.size = size
        self.time = time
        self.age = age
        self.smoke = smoke
        self.hourstosleep = hourstosleep
     
    # 1) Verifiers
    def verify_roast(self):
        '''
        for use with user input from html form, returns BOOL
        '''
        try:
            if self.roast in ['blonde','medium','dark','other']:
                return True
        except:
            return False


    def verify_size(self):
        '''
        for use with user input from html form, returns BOOL
        '''
        try:
            if self.size in ['small','medium','large']:
                return True
        except:
            return False

    def verify_time(self):
        '''
        for use with user input from html form, returns BOOL
        '''
        try:
            if int(self.time) in range(0,23):
                return True
        except:
            return False

    def verify_age(self):
        '''
        for use with user input from html form, returns BOOL
        '''
        try:
            if int(self.age) in range(0,120):
                return True
        except:
            return False
            
    def verify_smoker(self):
        '''
        for use with user input from html form, returns BOOL
        '''
        try:
            if self.smoke in ['True','False']:
                return True
        except:
            return False
        
    def verify_hourstosleep(self):
        '''
        for use with user input from html form, returns BOOL
        '''
        try:
            if int(self.hourstosleep) in range(0,23):
                return True
        except:
            return False

    # 2) Getters
    def getlastdose(self):
        return(self.lastdose)
    
    def getlasttime(self):
        return(self.lasttime)
    
    def getage(self):
        return(self.age)
    
    def getsmoke(self):
        return(self.smoke)
    
    # 3) calculator methods
    def currentdose(self):
        '''
        uses verified user input (see verify methods) to calculate 
        caffiene level, and uses hours since that dose (time) to return a value
        for exponential decay.
        '''
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
            ans = ans*.5 # smoker, metabolism of caff faster
        try:
            if int(self.age) >= 65:
                ans = ans*1.333 # older than 65, metabolism of caff is slower
            elif int(self.age) <= 12:
                ans = 0 # 12 and younger shouldnt have caffiene
            
                return(None)
        except:
            pass
        # calculating expontential decay given dose and hours from dose
        ans = int(ans)*((0.5)**(int(self.time)/5))
        
        return int(ans)
    
    def futuredose(self):
        '''
        uses verified user input (see verify methods) to calculate future
        caffiene level, and uses hours until bedtime (hourstosleep) 
        to return a value for exponential decay.
        '''        
        dose = (int(self.currentdose())+200)
        
        if self.getsmoke() == True:
            dose *= 0.5 # smoker, metabolism of caff faster
        
        if int(self.getage()) >= 65:
            dose *= 1.33 # older than 65, metabolism of caff is slower
            
        # calculating expontential decay given dose and hours to sleep
        ans = int(dose)*((0.5)**(int(self.hourstosleep)/5))
        
        # if caffiene level at bedtime is greater than 175mg, sleep is affected
        if ans > 175:
            return False
        else:
            return True
        
    # 4) standard operator overloaders   
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
    
memory = {}

form = '''<!DOCTYPE html>
<title>Caffiene Calculator</title>
<form method="POST">
    <h2>Find Out If You Should Have That Next Cup!</h2>
        <p><b>Introduction: </b>The average person should not drink more than
            400mg of coffee in a day, which translates to four cups of 8oz of
            standard home drip coffee. However, if you buy your coffee from
            commercial chains like Starbucks or Dunkin Donuts, you are likely 
            drinking much more caffinated coffee.</p>
            <h4>Caffiene Content of Starbucks Drinks</h4>
            <table>
                <tr>
                    <th>Roast</th>
                    <th>Tall</th>
                    <th>Grande</th>
                    <th>Venti</th>
                </tr>
                <tr>
                    <td>Dark</td>
                    <td>193mg</td>
                    <td>260mg</td>
                    <td>340mg</td>
                </tr> 
                <tr>
                    <td>Medium</td>
                    <td>235mg</td>
                    <td>310mg</td>
                    <td>410mg</td>
                </tr>     
                <tr>
                    <td>Blonde</td>
                    <td>270mg</td>
                    <td>360mg</td>
                    <td>475mg</td>
                </tr> 
                <tr>
                    <td>Other</td>
                    <td>150mg</td>
                    <td>225mg</td>
                    <td>300mg</td>
                </tr>
            </table>    
    <br>
    <h3>Enter last dose of coffee here. If you had hot coffee, enter roast as
        'blonde', 'medium','dark'. If you had something other than hot coffee,
        enter 'other'.</h3>
        <p>The roast determines how caffinated the coffee is. The lighter the 
           roast, the more the caffiene.</p>
        <label>Last Dose:
            <input name="roast">
        </label>
        <br>
    <h3>Enter size of your last drink. Enter 'large', 'medium', or 'small'.
        </h3>
        <p>Larger sizes contain more caffiene.</p>
        <label>Enter size here:
            <input name="size">
        </label>
        <br>
    <h3>Enter hours since last dose of coffee here. Enter in integer form.</h3>
        <p>Coffee has a half life of around 5 hours.</p>
        <label>Enter hours here:
            <input name="time">
        </label>
        <br>
    <h3>Enter in the form of integer of years.</h3>
        <p>If you are less than 12 years old, then you shouldnt drink coffee. 
           If you are older than 65, then you metabolize cofee 33% slower</p> 
       
        <label>Enter age here:
            <input name="age">
        </label>
        <br>
    <h3>Do you smoke? Enter 'True' if you smoke or 'False' if you do not.</h3>
        <p>Smoking increases the metabolism of coffee by 50%</p>
        <label>Enter smoker status:
            <input name="smoker">
        </label>
        <br>
    <h3>How many hours away is your bedtime? Enter integer hours </h3>
        <p>
        <label>Hours untill bedtime:
            <input name="hourstosleep">
        </label>
        <br>
        <button type="submit">Calculate!</button>
        <br>
</form>
<h3>Note: These conclusions are most accurant if you drink less 400mg of 
    caffiene daily.</h3>
    <p>If the caffiene level calculated at bedtime is greater than 175mg, 
    it will likely delay the time you would like to go to sleep by an hour.
    Thus, 175mg was used to determine if you should (True) or should not (False)
    have more coffee. While you are asked what sort of commercial coffee you
    have had today, the next cup is assumed to contain the average amount of
    caffiene in a commercial cup of coffee (around 200mg)</p>
<pre>
<h2>+--------------Results---------------+</h2>
<h3>
{}
<h3>
<h2>+------------------------------------+</h2>
</pre>
'''


def checkparams(field, params, response, header, end_headers, write):
    '''
    checks integrity of form data, returns error if fields are missing
    '''
    if "{}".format(field) not in params:
        response(400)
        header('Content-type', 'text/plain; charset=utf-8')
        end_headers
        write("Missing form fields!".encode())
        return
    else:
        return
    

class PrgHandler(http.server.BaseHTTPRequestHandler): 
    '''
    python http server module
    docs: https://docs.python.org/3/library/http.server.html
    
    allows for GET, POST, REDIRECT requests
    '''
    def do_GET(self):
        # A GET request will either be for / (the root path) or for /some-name.
        # Strip off the / and we have either empty string or a name.
        name = unquote(self.path[1:])

        if name:
            if name in memory:
                # We know that name! Send a redirect to it.
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()
            else:
                # We don't know that name! Send a 404 error.
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(name).encode())
        else:
            # Root path. Send the form.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # List the known associations in the form.
            known = "\n".join("|      {} : {}".format(key, memory[key])
                              for key in (memory.keys()))
            self.wfile.write(form.format(known).encode())

    def do_POST(self):
        
        # Decode the form data.
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        
        # Check that the user submitted the form fields.
        attributes = ["roast","size","time","age","smoker","hourstosleep"]
        for field in attributes:
            checkparams(field, params, self.send_response, self.send_header, 
                           self.end_headers, self.wfile.write)

        # all fields filled in, gather data from form
        roast = params["roast"][0]
        size = params["size"][0]
        time = params["time"][0]
        age = params["age"][0]
        smoker = params["smoker"][0]
        hourstosleep = params["hourstosleep"][0]
        
        # initialize object for current form 
        finalans = CaffCalc(roast, size, time, age, smoker, hourstosleep)
        
        
        # verify form unput using CaffCalc class methods
        try:
            if finalans.verify_roast():
                # This input is good.  Remember it.
                memory["Roast"] = roast
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This input is no good.  Let the user know.
            memory["Roast"] = "Error in roast data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:   
            if finalans.verify_size():
                # This input is good.  Remember it.
                memory["Size"] = size
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This input is no good.  Let the user know.
            memory["Size"] = "Error in size data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:
            if finalans.verify_time():
                # This input is good.  Remember it.
                memory["Time"] = time
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This input is no good.  Let the user know.
            memory["Time"] = "Error in time data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:  
            if finalans.verify_age():
                # This input is good.  Remember it.
                
                if int(finalans.getage()) > 12:
                    memory["Age"] = age # age greater than 12, ok for coffee
                    
                else:
                    memory["Age"] = age+'  !!!' # too young, let user know
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This input is no good.  Let the user know.
            memory["Age"] = "Error in age data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:
            if finalans.verify_smoker():
                # This input is good.  Remember it.
                memory["Smoker"] = smoker
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This input is no good.  Let the user know.
            memory["Smoker"] = "Error in smoker data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:  
            if isinstance(int(finalans.currentdose()), int):
                # This input is good.  Remember it.
                # 0 means an error occured in required attributes to calculate
                if int(finalans.currentdose()) == 0:
                    memory["Current Dose"] = "Error in data collection."
                else:
                    # This input is good, no errors found.  Remember it. 
                    memory["Current Dose"] = finalans.currentdose()
    
                    # Serve a redirect to the form.
                    self.send_response(303)
                    self.send_header('Location', '/')
                    self.end_headers()            
        except:
            memory["Current Dose"] = "Error in data collection."
            
            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:   
            if finalans.verify_hourstosleep():
                # This input is good.  Remember it.
                memory["Hours till sleep"] = hourstosleep
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This input is no good.  Let the user know.
            memory["Hours to sleep"] = "Error in data collection."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:   
            if finalans.verify_hourstosleep():
                # This input is good.  Remember it.
                memory["Should you have more coffee?"] = finalans.futuredose()
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This input is no good.  Let the user know.
            memory["Should you have more coffee?"] = "Error in data collection."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
if __name__ == '__main__':

    port = int(os.environ.get('PORT', 8000)) # Use PORT if its there
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, PrgHandler)
    httpd.serve_forever()
    
