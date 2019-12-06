//alert("hello");
//document.getElementById("contents").innerHTML += "skdjflasf";


var source = new EventSource('/tweets');

var data = [];

source.addEventListener('message', function(e) {
    obj = JSON.parse(e.data);
    tempData = {};
    tempData.tweet = obj.text;
    tempData.username = obj.user.name;
    tempData.screen_name = obj.user.screen_name;
    tempData.profile_pic = obj.user.profile_image_url_https;

    document.getElementById("contents").innerHTML = "<div class=\"row\"><div class=\"col-sm-12 strip\"><script src=\"..\/static\/stream.js\"> <\/script><img src=" + tempData.profile_pic + " \/><strong>" + tempData.username + "<\/strong><span class=\"light\"> @" + tempData.screen_name + " - <\/span><br>" + tempData.tweet + "<\/div><\/div>" + document.getElementById("contents").innerHTML;
    // add code to add div element
}, false);