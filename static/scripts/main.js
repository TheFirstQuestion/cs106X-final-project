// ################### CONSTANTS ###################################
var WHOLE_WIDTH = $(document).width();
var WHOLE_HEIGHT = $(document).height();
var WHOLE_CENTER = [WHOLE_WIDTH / 2, WHOLE_HEIGHT / 2];
var NUM_INITIAL_KEYWORDS = 10;
var DEFAULT_SHAPE_SIZE = 200;
var GENERAL_GRID_CENTER = [WHOLE_CENTER[0], 80 + (1.25 * DEFAULT_SHAPE_SIZE)];
var FOCUS_SPOT = [WHOLE_CENTER[0], 20 + (DEFAULT_SHAPE_SIZE / 2)];
// #################################################################


// Make the canvas cover the whole screen
var canvasElement = document.getElementById("myCanvas");
canvasElement.width  = window.innerWidth;
canvasElement.height = window.innerHeight;
// Move the text input to its spot
$('#typingField').css({
    left: 30,
    top: 30
})
// Create the fabric.js canvas and set basic stuff
var canvas = new fabric.Canvas("myCanvas");
canvas.selection = false;
canvas.backgroundColor = "#87CEEB";
// Label the center for development purposes
//markCenter();
// Default load action
init();

function init() {
    clearCanvas();
    //drawFolder(ROOT_OF_FILE_SYSTEM, WHOLE_CENTER);
    //var points = semicirclePoints(WHOLE_CENTER, 275, NUM_INITIAL_KEYWORDS);
    //var points = circlePoints(WHOLE_CENTER, 275, NUM_INITIAL_KEYWORDS);
    //var points = evenlySpacedHorizontalPoints(WHOLE_CENTER, WHOLE_WIDTH, NUM_INITIAL_KEYWORDS);
    var sortedKeywords = sortByWeight(ALL_THE_KEYWORDS);
    var points = gridPoints(GENERAL_GRID_CENTER, WHOLE_WIDTH, NUM_INITIAL_KEYWORDS);
    for (var i = 0; i < NUM_INITIAL_KEYWORDS; i++) {
        drawKeyword(sortedKeywords[i].word, points[i]);
        //drawKeyword(ALL_THE_KEYWORDS[NUM_INITIAL_KEYWORDS+i].word, randomPoint());
    }
    //drawFolder(ROOT_OF_FILE_SYSTEM, WHOLE_CENTER);
}


function focusOnKeyword(word) {
    clearCanvas();
    var files = filesFromKeyword(word);
    files = files.slice(0, Math.min(NUM_INITIAL_KEYWORDS, files.length));
    drawKeyword(word, FOCUS_SPOT);
    //var points = semicirclePoints(point, 400, files.length);
    var points = gridPoints(GENERAL_GRID_CENTER, WHOLE_WIDTH, files.length);
    for (var i = 0; i < files.length; i++) {
        drawFile(files[i].name, points[i]);
    }
}

function focusOnFile(name) {
    clearCanvas();
    var keywords = keywordsFromFile(name);
    keywords = keywords.slice(0, Math.min(NUM_INITIAL_KEYWORDS, keywords.length));
    drawFile(name, FOCUS_SPOT);
    //var points = semicirclePoints(point, 400, keywords.length);
    var points = gridPoints(GENERAL_GRID_CENTER, WHOLE_WIDTH, keywords.length);
    for (var i = 0; i < keywords.length; i++) {
        drawKeyword(keywords[i].word, points[i]);
    }
}

function focusOnFolder(name) {
    clearCanvas();
    var splitPath = name.split("/");
    var thisFolderName = splitPath[splitPath.length - 1];
    var children = subfoldersOfFolder(thisFolderName);
    //console.log("children: ");
    //console.log(children);
    var points = gridPoints(GENERAL_GRID_CENTER, WHOLE_WIDTH, children.length);
    for (var i = 0; i < children.length; i++) {
        drawFolder(children[i].path, points[i]);
    }
}

function dealWithTyping() {
    var typed = $("#typingField").val();
    // If deleting text, start over as if page was refreshed
    if (typed == "") {
        init();
        return;
    }

    var possibilities = suggestKeywords(typed);

    clearCanvas();

    var points = gridPoints(GENERAL_GRID_CENTER, WHOLE_WIDTH, NUM_INITIAL_KEYWORDS);
    //var points = evenlySpacedHorizontalPoints(WHOLE_CENTER, WHOLE_WIDTH, NUM_INITIAL_KEYWORDS);
    for (var i = 0; i < NUM_INITIAL_KEYWORDS; i++) {
        drawKeyword(possibilities[i].word, points[i]);
    }
}

function openInNewTab(url) {
    var win = window.open(url, '_blank');
    //win.focus();
}
