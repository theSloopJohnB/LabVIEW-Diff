import requests
import json

USER = 'theSloopJohnB'
PW = 'PW_GOES_HERE'


myauth = requests.auth.HTTPBasicAuth(USER, PW)

# Get comments for an issue / PR (represented same way for our purposes)
pr = requests.get('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments')

# post a comment on an issue
body = json.dumps({"body":"automatic ![capture](https://cloud.githubusercontent.com/assets/26978265/26067300/5ac6aa44-395f-11e7-851b-52610704b360.PNG)"})
r = requests.post('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments',data=body, auth=myauth)
