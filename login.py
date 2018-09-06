import urllib
import facebook
import webapp2
from webapp2_extras import sessions

facebook_APP_ID = 'xxxxxxxxxxx'
facebook_APP_SECRET = 'xxxxxxxxxxxxxxxxxxxxxx'
facebook_graphUrl = 'https://graph.facebook.com/v2.8'
facebook_redirectUri = 'http://gold-circlet-160109.appspot.com/login/'
facebook_requestCode = 'https://www.facebook.com/v2.8/dialog/oauth?'
urllib.urlencode(
                    {'client_id':facebook_ID,
                     'redirect_uri':facebook_redirectUri,
                     'scope':'public_profile, email, user_friends'})


def retrieve_access_token(code):
   args = {'redirect_uri': facebook_redirectUri,
        'client_id': facebook_ID,
        'client_secret': facebook_secret,
        'code': code}
   access_token = urllib.urlopen(facebook_graphUrl + "/oauth/access_token?" + urllib.urlencode(args)).read()
   access_token = urlparse.parse_qs(access_token)
   return access_token['access_token'][0]

def get_graph_api(token):
   if isinstance(token, dict):
        return facebook.GraphAPI(token['access_token'])
   else:
        return facebook.GraphAPI(token)

class BaseHandler(webapp2.RequestHandler):
   def dispatch(self):
       self.session_store = sessions.get_store(request=self.request)
       try:
           webapp2.RequestHandler.dispatch(self)
       finally:
           self.session_store.save_sessions(self.response)

   @webapp2.cached_property
   def session(self):
       return self.session_store.get_session()

class FBLogin(BaseHandler):
    def get(self):
        code = self.request.get('code')
    if self.request.get("code"):
            access_tk = retrieve_access_token(code)
            facebookObject = get_graph_api(access_tk)
            facebookObject = facebookObject.get_object('me')
            self.session["ECommerceUser"] = dict(
                        idSocial = facebookObject['id'],
                        image='http://graph.facebook.com/'+facebookObject['id']+'/picture?type=square',
                        username=last_name[0] + " " + last_name[1],
                        loginMethod=loginMethod
                        )
            self.redirect("/")
    else:
        self.redirect(facebook_requestCode)