# -*- coding: utf-8 -*-
from weibo import APIClient
from re import split
import urllib,urllib2,httplib
 
APP_KEY = '377217891' #youre app key 
APP_SECRET = '723905a68a35ca6e2f30016230337e8f' #youre app secret  
CALLBACK_URL = 'http://6.helloelmer.sinaapp.com/callback'
ACCOUNT = 'ffxhina@163.com'#your email address
PASSWORD = 'longyang22'     #your pw
 
#for getting the authorize url
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()

#for getting the code contained in the callback url
def get_code():
    conn = httplib.HTTPSConnection('api.weibo.com')
    postdata = urllib.urlencode     ({'client_id':APP_KEY,'response_type':'code','redirect_uri':CALLBACK_URL,'action':'submit','userId':ACCOUNT,'passwd':PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
    conn.request('POST','/oauth2/authorize',postdata,{'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
    res = conn.getresponse()
    location = res.getheader('location')
#    print "*********"
    print 'header', res.msg.headers
#    print 'msg===========',res.msg
#    print 'status===========',res.status
#    print 'reason===========',res.reason
#    print 'version===========',res.version
#    print type(location), location
    code = location.split('=')[1]
    conn.close()
    return code
    

def gplus2sina(post):
    code = get_code()
    r = client.request_access_token(code)
    client.set_access_token(r.access_token, r.expires_in)

    fd = urllib2.urlopen("https://lh3.googleusercontent.com/-5urJEjOvvCQ/AAAAAAAAAAI/AAAAAAAAAAA/c0awZpY5R7w/s48-c-k/photo.jpg")
    #fd = urllib2.urlopen("http://reg.163.com/gaiban/images/logo.png")
    response = client.upload.statuses__upload(status=u'Python Sina microblog for OAuth 2.0 testing',visible="2",pic=fd)
    fd.close()

#if __name__ == '__main__':
#    gplus2sina(None)




