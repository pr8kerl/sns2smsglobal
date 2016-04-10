from __future__ import print_function

import httplib, urllib
import hmac
import hashlib
import base64
import time
import random
import string
import json

#
# SMSGlobalAPIWrapper
# @au80thor: Huy Dinh <huy.dinh@smsglobal.com>
#
class Wrapper (object):

    TYPE_JSON = "application/json"
    TYPE_XML = "application/xml"
    TYPE_YAML = "application/x-yaml"
    TYPE_CSV = "text/csv"
    TYPE_MSGPACK = "application/x-msgpack"

    def __init__(self, key, secret, protocol = "https", host = "api.smsglobal.com", port = 443, apiVersion = "v1", extraData = "", debug = False, type = TYPE_CSV):
        self.key = key.strip()
        self.secret = secret.strip()
        self.protocol = protocol.lower()
        self.host = host.strip()
        self.port = port
        self.apiVersion = apiVersion
        self.extraData = extraData
        self.debug = debug
        self.type = type

    def get(self, action, id = None):
        return self.connect("GET", action, id)

    def post(self, action, id = None, body = None):
        return self.connect("POST", action, id, body)

    def delete(self, action, id = None):
        return self.connect("DELETE", action, id)

    def connect(self, method, action, id = None, body = None):
        action = "/%s/%s/" % (self.apiVersion, action)
        if (id != None) and (id != ''):
            action = "/%s/%s/id/%s/" % (self.apiVersion, action, id)

        # Set up request metadata
        if method not in ["GET", "POST", "DELETE", "OPTIONS", "PATCH"]:
            method = "GET"

        if method in [ "POST" ]:
            headers = {"Authorization" : self.get_authorisation_http_header(method, action), "User-Agent" : "SMS Python Client", "Accept": self.type, "Content-Type" : 'application/json' }
        else:
            headers = {"Authorization" : self.get_authorisation_http_header(method, action), "User-Agent" : "SMS Python Client", "Accept": self.type}

        # HTTP transportation
        http = httplib.HTTPSConnection(self.host, self.port)

        if self.debug:
            http.set_debuglevel(1)


        # do it!
        http.request(method, action, body, headers)
        response = http.getresponse()

        answer = json.dumps({ "status": response.status, "response": response.read() })
        return answer


    def get_authorisation_http_header(self, method, action):
        algorithm = "sha256"

        # Get current Time
        timestamp = int(time.time())

        # Random String
        nonce = hashlib.md5(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(36))).hexdigest()

        # Hence
        raw_str = "%s\n%s\n%s\n%s\n%s\n%d\n%s\n" % (timestamp, nonce, method, action, self.host, self.port, self.extraData)

        # Encryptions
        hash = hmac.new(self.secret, raw_str, hashlib.sha256).digest()
        hash = base64.b64encode(hash);
        mac = "MAC id=\"%s\",ts=\"%s\",nonce=\"%s\",mac=\"%s\"" % (self.key, timestamp, nonce, hash)

        return mac


