function camera() {
    navigator.webkitGetUserMedia({video:true},getStream,noStream)
}