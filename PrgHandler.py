#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 12:27:52 2018

@author: jacobpelletier
"""
import http.server
import requests
from urllib.parse import unquote, parse_qs
import os
import threading
from socketserver import ThreadingMixIn

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
    
memory = {}

form = '''<!DOCTYPE html>
<title>Bookmark Server</title>
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

    if "{}".format(field) not in params:
        response(400)
        header('Content-type', 'text/plain; charset=utf-8')
        end_headers
        write("Missing form fields!".encode())
        return
    else:
        return
    

class PrgHandler(http.server.BaseHTTPRequestHandler): #Shortener 
    
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

        roast = params["roast"][0]
        size = params["size"][0]
        time = params["time"][0]
        age = params["age"][0]
        smoker = params["smoker"][0]
        hourstosleep = params["hourstosleep"][0]
  
        finalans = CaffCalc(roast, size, time, age, smoker, hourstosleep)
            
        try:
            if finalans.verify_roast():
                # This URI is good!  Remember it under the specified name.
                memory["Roast"] = roast
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This URI is good!  Remember it under the specified name.
            memory["Roast"] = "Error in roast data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:   
            if finalans.verify_size():
                # This URI is good!  Remember it under the specified name.
                memory["Size"] = size
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This URI is good!  Remember it under the specified name.
            memory["Size"] = "Error in size data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:
            if finalans.verify_time():
                # This URI is good!  Remember it under the specified name.
                memory["Time"] = time
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This URI is good!  Remember it under the specified name.
            memory["Time"] = "Error in time data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:  
            if finalans.verify_age():
                if int(finalans.getage()) > 12:
                    # This URI is good!  Remember it under the specified name.
                    memory["Age"] = age
                    
                else:
                    memory["Age"] = age+'  !!!'
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This URI is good!  Remember it under the specified name.
            memory["Age"] = "Error in age data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:
            if finalans.verify_smoker():
                # This URI is good!  Remember it under the specified name.
                memory["Smoker"] = smoker
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This URI is good!  Remember it under the specified name.
            memory["Smoker"] = "Error in smoker data."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:  
            if isinstance(int(finalans.currentdose()), int):
                
                if int(finalans.currentdose()) == 0:
                    memory["Current Dose"] = "Error in data collection."
                else:
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
                # This URI is good!  Remember it under the specified name.
                memory["Hours till sleep"] = hourstosleep
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This URI is good!  Remember it under the specified name.
            memory["Hours to sleep"] = "Error in data collection."

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        try:   
            if finalans.verify_hourstosleep():
                # This URI is good!  Remember it under the specified name.
                memory["Should you have more coffee?"] = finalans.futuredose()
    
                # Serve a redirect to the form.
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
        except:
            # This URI is good!  Remember it under the specified name.
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
    
