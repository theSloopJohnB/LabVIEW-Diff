#!/usr/bin/env python3

import requests
import json
import base64
import os
import datetime

with open('/mnt/c/token.txt', 'r') as text:
    token = text.read().strip()
HEADERS={'Authorization': 'token %s' % token}

# encode a file into base64
def read_picture(file_name):
    with open(file_name, 'rb') as text:
        return base64.b64encode(text.read()).decode()

def post_file(file_data, folder, file_name):
    # put encoded data into json request
    new_file_data = json.dumps({"message": "commit message", "content":file_data})

    # post a picture to a repo
    # TODO this will need to be in its own folder based on the PR coming in.
    url = 'https://api.github.com/repos/theSloopJohnB/thesloopjohnb/contents/%s/%s' % (folder, file_name)
    
    r=requests.put(url, data=new_file_data, headers=HEADERS)
    print ('Post file response code: %s' % r.status_code)
    return r.json()['content']['download_url']

# post a comment on an issue
def post_comment_to_pr(urlPicPairs, pullRequestInfo, prNumber):
    formatString = "### %s: ![capture](%s)\n\n"
    body = """Bleep bloop!

LabVIEW Diff Robot here with some diffs served up hot for your pull request.

Notice something funny? Help fix me on [my GitHub repo.](https://github.com/theSloopJohnB/LabVIEW-Diff)


"""
    for pair in urlPicPairs:
        body += formatString % pair

    org, repo, _ = pullRequestInfo.split('/')
    url = "https://api.github.com/repos/%s/%s/issues/%s" % (org, repo, prNumber)
    data = json.dumps({"body":body})
    r = requests.post(url, data=data, headers=HEADERS)
    print ('Post comment response code: %s' % r.status_code)

def post_pics_to_pr(localPicfileDirectory, pullRequestInfo, prNumber):
    pics = [f for f in os.listdir(localPicfileDirectory) if f.endswith(".png")]
    folder = pullRequestInfo + '/' + datetime.datetime.now().strftime('%Y-%m-%d/%H:%M:%S')
    picUrls = []
    for pic in pics:
        picData = read_picture(os.path.join(localPicfileDirectory, pic))
        picUrl = post_file(picData, folder, os.path.split(pic)[1])
        picUrls.append((pic, picUrl))

    post_comment_to_pr(picUrls, pullRequestInfo, prNumber) 

if __name__ == '__main__':
    post_pics_to_pr("/mnt/c/jenkins/workspace/AF_IntegrationTesting_PR-13-SO24U2UAYXRUW3RRNDZGD3O6R5BBCUQW7IGERBC35TL5X4YWF44A/diff_dir", "LabVIEW-DCAF/IntegrationTesting/PR-13", "13")
