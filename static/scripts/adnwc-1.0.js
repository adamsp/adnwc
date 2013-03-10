var browserWidth = 0;
var browserHeight = 0;
var word_array = [];
var drawing = false;

// Thanks, StackOverflow: http://stackoverflow.com/a/3945897/1217087
function getSize() {
    if( typeof( window.innerWidth ) == 'number' )
    {
        //Non-IE
        isIE = false;
        browserWidth = window.innerWidth;
        browserHeight = window.innerHeight;
    } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
        //IE 6+ in 'standards compliant mode'
        browserWidth = document.documentElement.clientWidth;
        browserHeight = document.documentElement.clientHeight;
    } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
        
        //They're not running IE7 / FireFox2. Older browser. Find some technology
        //to destroy their computer so they're forced to upgrade.
        browserWidth = document.body.clientWidth;
        browserHeight = document.body.clientHeight;
    }
}

function drawCloud() {
    if (drawing) return;
    drawing = true;
    getSize();
    $("#cloud").html('');
    $("#cloud").jQCloud(word_array, {
                        width: browserWidth * 0.8,
                        height: browserHeight * 0.8,
                        delayedMode: true,
                        afterCloudRender: function() { drawing = false; }});
}

function updateItems(endpoint, prefix) {
    if (drawing) {
        setTimeout(updateItems(endpoint, prefix), 200);
        return;
    }
    $.getJSON(
              endpoint,
              function (data) {
              word_array.length = 0;
              for(var i = 0; i < data.length; i++){
              word_array.push({
                              text: prefix + data[i][0],
                              weight: data[i][1],
                              html: {
                              title: prefix + data[i][0] + ": " + data[i][1] + " occurrences."
                              }})
              };
              drawCloud(word_array);
              });
}

updateItems('/wc', '')

// Only re-draw when the window has finished resizing.
$(window).resize(function() {
                 clearTimeout(this.id);
                 this.id = setTimeout(drawCloud, 100);
                 });
