var currentid = 0;
var previousid = 0;
var nextid = 0;
var myPlayer;

function loadPreviousVideo() {
    $.getJSON("rendervideo/?VideoNumber=" + previousid, function(data) {
        console.log(data.nextId);
        console.log(data.url);
        console.log(data.prevId);
        nextid = data.nextId;
        previousid = data.prevId;
        myPlayer.src({ src: data.url });
    });
}

function loadNextVideo() {
    $.getJSON("rendervideo/?VideoNumber=" + nextid, function(data) {
        console.log(data.nextId);
        console.log(data.url);
        console.log(data.prevId);
        nextid = data.nextId;
        previousid = data.prevId;
        myPlayer.src({ src: data.url });
    });
}

function loadVideo(id) {
    $.getJSON("rendervideo/?VideoNumber=" + id, function(data) {
        console.log(data.nextId);
        console.log(data.url);
        console.log(data.prevId);
        nextid = data.nextId;
        previousid = data.prevId;
        myPlayer.src({ src: data.url });
    });
}

videojs("example_video_1", {}, function(){
    console.log("Player is ready !")
    myPlayer = this;
    // Player (this) is initialized and ready.
    $.getJSON('rendervideo/', function(data) {
        console.log(data.nextId);
        console.log(data.url);
        console.log(data.prevId);
        nextid = data.nextId;
        previousid = data.prevId;
        myPlayer.src({ src: data.url });
    });
});

function updateIds(newpreviousid, newnextid) {
    previousid = newpreviousid;
    nextid = newnextid;
}


// SEARCH
var currentPromise = $.Deferred().resolve().promise();

function displayResults(numberOfRes, text) {
    var resDiv = $(".results");
    $(document).mouseup(function (e) {
        var container = $(".searchbox-container");
        var results = $(".results");
        var searchbox = $(".searchbox");
        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) &&
            container.has(e.target).length === 0) {
            results.slideUp(200);
        }
        searchbox.on("focus", function () {
            if (!resDiv.is(':empty'))
                results.slideDown(200);
        })
    });

    var searchPromise = $.ajax({
        url: "/StreamServerApp/search_video/?q="+text.value,
        type: "GET"
    });

    var thenPromise = currentPromise.then(
        function () {
            return searchPromise;
        },
        function () {
            return searchPromise;
        });
    currentPromise = thenPromise;
    thenPromise.done(function (data) {
        resDiv.empty();
        if (data.length <= 0 && text.value !== '') {
            resDiv.append("<div class='ui large label' style='margin:2px; display:block'>No video found</div>");
        } else {
            for (var i = 0; i < data.length; i++) {
                var el = $("<a class='ui teal large label' style='margin:2px; display:block' " +
                    "video-id=" + data[i].id + ">" + data[i].name + "</a>");
                resDiv.append(el);
                el.click(function () {
                    resDiv.slideUp(200);
                    loadVideo($(this).attr('video-id'));
                });
            }
        }
        if (!resDiv.is(':empty'))
            resDiv.slideDown(200);
        else
            resDiv.slideUp(200);
    });
    thenPromise.fail(function () {
        console.log('failure');
    });
}
