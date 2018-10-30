var currentid=0;
var previousid=0;
var nextid=0;

function loadPreviousVideo() {
      $( "#ShowVideo").load("rendervideo/?VideoNumber="+previousid);
}

function loadNextVideo() {
      $( "#ShowVideo").load("rendervideo/?VideoNumber="+nextid);
}

function loadVideo(id) {
    $( "#ShowVideo").load("rendervideo/?VideoNumber="+id);
}

function loadFirstVideo(id) {
    $( "#ShowVideo").load("rendervideo/");
}

function updateIds(newpreviousid, newnextid){
    previousid=newpreviousid;
    nextid=newnextid;
}