#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import re
import urllib
import time

class MainHandler(webapp2.RequestHandler):
    def get(self):
        fil = open('homepage.html')
        
        for line in fil:
            self.response.write( line )
       
        fil.close()
        

class Parser( webapp2.RequestHandler ):
    def post(self):
        page_url = self.request.get('page_url')
        file_format = self.request.get('file_format')
        
        reg_exp = '''="([^=\s]+?\.{})'''.format(file_format)
        
        page_name = page_url
            
        folder_name = page_name.split('/')
        if len( folder_name ) > 3 :
            folder_name = '/'.join( folder_name[:-1] )
        else:
            folder_name = page_name
        
    
        self.response.out.write('<html><body>')
        
        try:
            page = urllib.urlopen( page_name )
            page_content = ''
            
            while True:
                recieved = page.read(5000)
                if len( recieved ) <= 1:
                    break
                page_content += recieved
                time.sleep(0.1)
            
            links = re.findall( reg_exp, page_content )

            if len( links ) > 0:
                self.response.out.write('Here are your links.<br><br>')
                for link in links:
                    if ':url' in link:
                        link = link.split(':url(')[-1] 
                        
                    if not link.startswith( folder_name ) and not link.startswith('http://') :
                        if not link.startswith('http://') and not link.startswith('//'):
                            link = folder_name + '/' + link.lstrip('/')
                        
                    self.response.out.write( '<a href="' )
                    self.response.write( link + '">' )
                    self.response.write(link)
                    self.response.write('</a>')
                    self.response.out.write('<br><br>')
            else:
                self.response.out.write('No links found <br>')  
        except:
            self.response.write( 'You messed up. Try the following:' )
            self.response.write( '<ul>' )
            self.response.write( '<li>Remove the "." from format</li>' )
            self.response.write( '</ul>' )
            
        self.response.out.write('''
        <button onclick="window.history.back();"> Done </button>
        ''')
       
        self.response.out.write('</body></html>')
 
    


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/parser', Parser)
], debug=True)
