import rule

#sina
APP_KEY = '377217891' #youre app key 
APP_SECRET = '723905a68a35ca6e2f30016230337e8f' #youre app secret  
CALLBACK_URL = 'http://6.helloelmer.sinaapp.com/callback'
ACCOUNT = 'ffxhina@163.com'#your email address
PASSWORD = 'longyang22'     #your pw

#gplus
GPLUS_ENABLE = True

GPLUS_URLS = (
    "https://plus.google.com/communities/112204979951069292983",
)

GPLUS_RULES = {
    "comments" : rule.bigger_than(4),
    "forward" : rule.bigger_than(7),
    "plus" : rule.bigger_than(10),
}