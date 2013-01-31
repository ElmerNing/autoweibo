import httplib, urllib, urllib2, time, datetime, logging
from weibo import APIClient
import conf

logging.basicConfig(filename='myapp.log',format='%(asctime)s %(message)s',level=logging.INFO)
logger = logging.getLogger( __name__ )

def get_code(url):
    """ get access token code """
    #simulator login
    conn = httplib.HTTPSConnection('api.weibo.com')
    postdata = urllib.urlencode     ({'client_id':conf.APP_KEY,'response_type':'code','redirect_uri':conf.CALLBACK_URL,'action':'submit','userId':conf.ACCOUNT,'passwd':conf.PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
    conn.request('POST','/oauth2/authorize',postdata, {'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
    res = conn.getresponse()
    location = res.getheader('location')
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

def public_posts(posts):
    client = get_auth_client()
    for post in posts:
        try:
            if post["image"] == "":
                client.post.statuses__update(status = post["text"].strip(), visible="2")
            else:
                if (post["text"] == ""):
                    continue
                client.upload.statuses__upload(status = post["text"],visible="2", pic=urllib2.urlopen(post["image"]))
            logger.info("post suc")
            logger.info(post)
        except Exception,e:
            logger.info("post error:" + str(e))
            logger.info(post)
        finally:
            time.sleep(5)
            
def all2sina():
    posts = []
    if conf.GPLUS_ENABLE:
        from gplus_post import gplus_post
        try:
            post = gplus_post()
            posts += post
        except e:
            logger.info("gplus error:" + str(e))

    public_posts(posts)


if __name__ == '__main__':
    all2sina()