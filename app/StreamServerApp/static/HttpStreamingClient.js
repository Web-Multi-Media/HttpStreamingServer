var currentid = 0;
var previousid = 0;
var nextid = 0;

function loadPreviousVideo() {
    $("#ShowVideo").load("rendervideo/?VideoNumber=" + previousid);
}

function loadNextVideo() {
    $("#ShowVideo").load("rendervideo/?VideoNumber=" + nextid);
}

function loadVideo(id) {
    $("#ShowVideo").load("rendervideo/?VideoNumber=" + id);
}

function loadFirstVideo() {
    $.getJSON('rendervideo/', function(data) {
        console.log(data);
        //data is the JSON string
    });
}

videojs("example_video_1", {}, function(){
    console.log("Player is ready !")
    // Player (this) is initialized and ready.
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
