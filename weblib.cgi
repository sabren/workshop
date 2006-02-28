#!/usr/bin/python2.4
"""
weblib.cgi : a wrapper script for weblib
inspired by http://www.webtechniques.com/archives/1998/02/kuchling/

USAGE (Apache):
   Action application/python-script /cgi-bin/weblib.cgi
   AddType application/python-script .py
"""
#import sys
#sys.stderr = sys.stdout
#print "content-type: text/plain"
#print

## CONFIGURATION ############################
## use this to add custom lib directories:

import sys
#sys.path = [".", "/home/sabren/lib/workshop"] + sys.path

#############################################

import cgi
import os
import os.path
import string
import StringIO

    
def fixWin32BinaryIssue():
    if sys.platform=="win32":
        import msvcrt
        msvcrt.setmode(sys.__stdin__.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.__stdout__.fileno(), os.O_BINARY)

if __name__=="__main__":

    try:  
        import weblib
        fixWin32BinaryIssue()
        
        path, filename = os.path.split(os.environ["PATH_TRANSLATED"])
        os.chdir(path)
        script = open(filename)
        
        req = weblib.RequestBuilder().build()
        eng = weblib.Engine(script, req)       
        eng.run()

        out = weblib.OutputDecorator(eng)
        sys.stdout.write(out.getHeaders())
        sys.stdout.write(out.getBody())
        
        if eng.hadProblem() and eng.globals["SITE_MAIL"]:
            out.sendError()

    except Exception, e:
        print "content-type: text/plain\n"
        cgi.print_exception()
