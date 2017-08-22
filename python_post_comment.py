#!/usr/bin/env python3

import requests
import json
import base64
import os

with open('/mnt/c/token.txt', 'r') as text:
    token = text.read().strip()
HEADERS={'Authorization': 'token %s' % token}

# encode a file into base64
def read_picture(file_name):
    with open(file_name, 'rb') as text:
        return base64.b64encode(text.read()).decode()

def post_file(file_data, file_name):
    # put encoded data into json request
    new_file_data = json.dumps({"message": "commit message", "content":file_data})

    # post a picture to a repo
    # TODO this will need to be in its own folder based on the PR coming in.
    url = 'https://api.github.com/repos/theSloopJohnB/thesloopjohnb/contents/%s' % file_name
    
    r=requests.put(url, data=new_file_data, headers=HEADERS)
    print ('Request Code: %s' % r.status_code)
    print (r.text)
    return r.json()['content']['download_url']

# post a comment on an issue
def post_comment(url, message, picture):
    body = json.dumps({"body":"%s ![capture](%s)" % (message, picture)})
    r = requests.post('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments',data=body, auth=MY_AUTH)

def main(fileDirectory):
    pics = [os.path.join(fileDirectory, f) for f in os.listdir(fileDirectory) if f.endswith(".png")]
    print (pics)
    for pic in pics:
        picData = read_picture(pic)
        picUrl = post_file(picData, os.path.split(pic)[1])
        print (picUrl)  


main("/mnt/c/jenkins/workspace/AF_IntegrationTesting_PR-13-SO24U2UAYXRUW3RRNDZGD3O6R5BBCUQW7IGERBC35TL5X4YWF44A/diff_dir")
