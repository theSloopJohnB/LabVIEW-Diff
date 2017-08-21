def call(lv_version){
    echo 'Running LabVIEW diff build between origin/master and this commit' 
    diffDir = '${WORKSPACE}\\diff_dir'
    mkdir diffDir
    bat 'git difftool -x="labview-cli --kill --lv-ver ${lv_version} C:\\Users\\nitest\\Documents\\GitHub\\LabVIEW-Diff\\Main.vi -- \"$LOCAL\" \"$REMOTE\" ${diffDir}" origin/master ${GIT_COMMIT}'
}
