var currentid=0;
var numids;

function loadPreviousVideo() {
    newid=currentid-1;
    if(newid>=1){
      $( "#ShowVideo").load("rendervideo/?VideoNumber="+newid);
      currentid=newid;
    }
}

function loadNextVideo() {
    newid=currentid+1;
    if(newid<=numids){
      $( "#ShowVideo").load("rendervideo/?VideoNumber="+newid);
      currentid=newid;
    }
}

function loadVideo(id) {
    $( "#ShowVideo").load("rendervideo/?VideoNumber="+id);
    currentid=id;
}

function setNumberIds(numberofids){
    numids=numberofids;
}