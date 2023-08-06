#!/usr/bin/env python

#
# (c) 2015-2020 caregraf
#

import sys
import urllib.request
import urllib.parse
import io
import ssl
import json
import re
import logging

from rpcutils.brokerRPC import VistARPCConnection, RPCLogger

"""
FMQL Endpoint Indirection - broker or REST and REST can be CSP (which has quirky errors)

TODO: merge in CacheInterface (may distinguish 3 - CSP/REST/BrokerIF
"""
                                
class FMQLRESTIF:
    """
    Indirection between endpoint for query so can go to CSPs etc.
        
    TODO: catch 503 etc in here and return clean ERROR codes
    """
    def __init__(self, fmqlEP, epWord="fmql"):
        self.fmqlEP = fmqlEP
        self.epWord = epWord
        
    def __str__(self):
        return "ENDPOINT: " + self.fmqlEP
        
    def invokeQuery(self, query):
        # rem: using GET and not POST so no encode to ascii too 
        queryURL = "{}?{}".format(self.fmqlEP, urllib.parse.urlencode({self.epWord: query}))
        if re.match("https", queryURL):
            # ignore bad cert - happens on test systems.
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            breply = urllib.request.urlopen(queryURL, context=ctx).read()
        else:
            breply = urllib.request.urlopen(queryURL).read() 
        sreply = breply.decode("utf-8")
        try:
            # Want to preserve order of keys (as FMQL does) 
            jreply = json.loads(sreply) 
            return jreply
        except:
            if re.search(r'FMQL\.CSP', self.fmqlEP): # CSP endpoint
                #
                # Error: <b>Cannot allocate a license</b><br>
                # ErrorNo: <b>5915</b><br>
                # CSP Page: <b>/csp/fmquery/FMQL.CSP</b><br>
                # Namespace: <b>CHCS</b><br>
                #
                if re.search(r'ErrorNo', sreply):
                    error = re.search(r'Error: \<b\>([^\<]+)', sreply).group(1)
                    errorNo = re.search(r'ErrorNo: \<b\>([^\<]+)', sreply).group(1)
                    logging.error("CSP Error Response for query {} - {} - {}".format(query, errorNo, error))
            last500 = sreply[-500:]
            if len(sreply) > 500:
                last500 = "[LAST 500] {}".format(last500)
            logging.error("Problem Response for query {} - {}".format(query, last500))
            raise
            
class FMQLBrokerIF:

    def __init__(self, hostname, port, access, verify, osehraVISTA=False):
        conn = VistARPCConnection(hostname, int(port), access, verify, "CG FMQL QP USER", RPCLogger(), useOSEHRACipher=osehraVISTA)
        conn.connect()
        self.__connection = conn
        self.__epDescr = hostname + ":" + str(port)
        
    def __str__(self):
        return "BROKER ENDPOINT: " + self.__epDescr
        
    def invokeQuery(self, query):
    
        reply = self.__connection.invokeRPC("CG FMQL QP", [query])

        try: 
            # preserve order as FMQL does
            jreply = json.loads(reply)
        except:
            logging.error("Can't make JSON for response to query {} - {}".format(query, reply))
            raise
        
        return jreply

class CacheObjectInterface:
    """
    Utility for talking to FMQL through a Cache Object Interface. Key feature is managing sessions. Cache uses cookies for session identification. Cache limits the number of sessions on a server so it is important to use and reuse the same session.

    If Cache runs out of sessions, it will issue Service Unavailable 503 errors.

    Follows FMQLInterface

    NOTE: though ported to Python3, not yet tested and TODO needs to merge with FMQLIF above or be a clean difference
    """
    def __init__(self, ep):
        # ex/ http://...../FMQL.csp
        self.ep = ep
        self.cookie = ""

    def invokeRPC(self, name, params):
        # to match broker if for now
        return self.invokeQuery(params[0]).read()

    def invokeQuery(self, query):
        queryDict = {"query": query}
        queryurl = self.ep + "?" + urllib.parse.urlencode(queryDict).encode('ascii')
        request = urllib.request.Request(queryurl)
        if self.cookie:
            request.add_header('cookie', self.cookie)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            # 503 "Service Unavailable": The server cannot process the request due to a high load
            raise
        # Always reset the cookie - may be a new one if session idle for > 15 minutes.
        # SET-COOKIE: CSPSESSIONID-SP-57772-UP-csp-fmquery-=0010000100002g3gWldo9l0000fAj6SQgextDm2AmskX7GxQ--; path=/csp/fmquery/;  httpOnly;
        self.cookie = response.info().getheader('Set-Cookie')
        return response

def main():

    assert sys.version_info >= (3, 3)
    
    fmqlIF = FMQLRESTIF("http://localhost:9100/fmqlEP")
    res = fmqlIF.invokeQuery("DESCRIBE 8989_5-1")
    print(res)
    print()

    host = "localhost"
    port = 9330
    access = "QLFM1234"
    verify = "QLFM1234!!"
    connection = VistARPCConnection(host, int(port), access, verify, "CG FMQL QP USER", RPCLogger())
    reply = connection.invokeRPC("CG FMQL QP", ["DESCRIBE 8989_5-1"])
    print(reply)

if __name__ == "__main__":
    main()
