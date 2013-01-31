import httplib, urllib, urllib2, time, datetime
import conf
from weibo import APIClient

def get_code(url):
    """ get access token code """
    #simulator login
    conn = httplib.HTTPSConnection('api.weibo.com')
    postdata = urllib.urlencode     ({'client_id':conf.APP_KEY,'response_type':'code','redirect_uri':conf.CALLBACK_URL,'action':'submit','userId':conf.ACCOUNT,'passwd':conf.PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
    conn.request('POST','/oauth2/authorize',postdata, {'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
    res = conn.getresponse()
    location = res.getheader('location')
    print 'header=========', res.msg.headers
    print 'msg===========',res.msg
    print 'status===========',res.status
    print 'reason===========',res.reason
    print 'version===========',res.version
    #fetch the access token code
    code = location.split('=')[1]
    conn.close()
    return code

def get_auth_client():
    """get a auth weibo api client"""
    client = APIClient(app_key=conf.APP_KEY, app_secret=conf.APP_SECRET, redirect_uri=conf.CALLBACK_URL)
    url = client.get_authorize_url()
    
    code = get_code(url)
    r = client.request_access_token(code)
    client.set_access_token(r.access_token, r.expires_in)

    return client

client = get_auth_client()

def public_posts(posts):
    """ public posts """

    for post in posts:
        try:
            if post["image"] == "":
                client.post.statuses__update(status = post["text"].strip(), visible="2")
            else:
                client.upload.statues__upload(status = post["text"],visible="2", pic=urllib2.urlopen(r"https:"+post["image"]))
            time.sleep(10)
        except Exception,e:
            print "###", datetime.datetime.now(), "###"
            print "error:", e
            print "post:"
            print post
            
def all2sina():
    posts = []

    if conf.GPLUS_ENABLE:
        from gplus_post import gplus_post
        post = gplus_post()
        posts += post
        #print post

    public_posts(posts)


if __name__ == '__main__':
    all2sina()