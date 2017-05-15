import requests
import json

USER = 'theSloopJohnB'
PW = 'PW_GOES_HERE'


MY_AUTH = requests.auth.HTTPBasicAuth(USER, PW)

# Get comments for an issue / PR (represented same way for our purposes)
pr = requests.get('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments')

# encode a file into base64
def read_picture(file_name):
    with open(file_name, 'rb') as text:
        return base64.b64encode(text.read())

def post_file(file_data, file_name):
    # put encoded data into json request
    new_file_data = json.dumps({"message": "commit message", "content":file_data.decode()})

    # post a picture to a repo
    r=requests.put('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/contents/%s' % file_name, data=new_file_data, auth=MY_AUTH)
    return r.json()['content']['download_url']

# post a comment on an issue
def post_comment(url, message, picture):
    body = json.dumps({"body":"%s ![capture](%s)" % (message, picture)})
    r = requests.post('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments',data=body, auth=MY_AUTH)

def main():
    file_name = 'TEMP.txt'
    encoded_file = read_picture(file_name)
    file_url = post_file(encoded_file, file_name)
    pullRequest = 'https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments'
    post_comment(pullRequest, 'Picture', file_url)
