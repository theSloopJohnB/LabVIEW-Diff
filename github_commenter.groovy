#!/usr/local/bin/groovy
import groovy.json.JsonOutput

MY_TOKEN = "token 75f58314809e604603d1d0c46d756fb6cbad1d5e"
 
// encode a file into base64
def encode_file(file_name) {
    return file_name.text.bytes.encodeBase64().toString()
}

def post(url, payload){
    // // POST
    println (url)
    def post = new URL(url).openConnection();
    post.setRequestMethod("POST")
    post.setDoOutput(true)
    post.setRequestProperty("Content-Type", "application/json")
    post.setRequestProperty("Authorization", MY_TOKEN)
    post.getOutputStream().write(payload.getBytes("UTF-8"))
    def postRC = post.getResponseCode()
    println(postRC);
    def response = post.content.getText()
    println(response)
    return response
}

// put encoded data into json request
def post_file(fileToPost){
    data = encode_file(fileToPost)
    // TODO: tie commits to PRs - maybe unique folder too
    new_file_data = JsonOutput.toJson([message: "Adding file for diff viewer", content:data])
    //post a picture to a repo
    // files might have invalid chars for urls such as spaces
    encodedFileName = java.net.URLEncoder.encode(fileToPost.name, 'UTF-8')
    r = post("https://api.github.com/repos/theSloopJohnB/thesloopjohnb/contents/${encodedFileName}", new_file_data)
    return r.json()['content']['download_url']
}

// post a comment on an issue
def post_comment(url, message, picture){
    //body = json.dumps({"body":"%s ![capture](%s)" % (message, picture)})
    r = requests.post('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments',data=body, auth=MY_AUTH)
}

def post_pics_to_github(dirOfPics, githubPr){
    //println(new File(dirOfPics).eachFile({it -> println(it.name)}))
    pics = new File(dirOfPics).listFiles().findAll { it.name.endsWith '.png' }
    fileUrls = pics.each {
        post_file it
    } 
    // encoded_file = read_picture(file_name)
    // file_url = post_file(encoded_file, file_name)
    // pullRequest = 'https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments'
    // post_comment(pullRequest, 'Picture', file_url)
}

println('Starting')
post_pics_to_github("/mnt/c/jenkins/workspace/AF_IntegrationTesting_PR-13-SO24U2UAYXRUW3RRNDZGD3O6R5BBCUQW7IGERBC35TL5X4YWF44A/diff_dir", "TEMP")

// POST
// MY_AUTH = requests.auth.HTTPBasicAuth(USER, PW)
// // Get comments for an issue / PR (represented same way for our purposes)
// def pr = httpRequest validResponseCodes: "200,500", url: 'https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments'
// def get = new URL('https://api.github.com/repos/theSloopJohnB/thesloopjohnb/issues/4/comments').openConnection();
// def getRC = get.getResponseCode();

// println("Status: "+ getRC)
// println("Message: "+ get.getInputStream().getText());
// def pic = read_picture('upload.png')


