function drawFolder(name, pos) {
    var text = wordText(name);
    var rect = new fabric.Rect({
        fill: 'yellow',
        width: 3 * DEFAULT_SHAPE_SIZE,
        height: DEFAULT_SHAPE_SIZE,
        originX: 'center',
        originY: 'center',
        stroke: 'grey',
        strokeWidth: 1
    });
    finishGroup(name, [rect, text], pos, "folder");
}

function drawKeyword(name, pos) {
    var text = wordText(name);
    var circ = new fabric.Circle({
        fill: 'white',
        radius: DEFAULT_SHAPE_SIZE / 2,
        originX: 'center',
        originY: 'center',
        stroke: 'grey',
        strokeWidth: 1
    });
    finishGroup(name, [circ, text], pos, "keyword");
}

function drawFile(name, pos) {
    var file = getFile(name);
    var text = wordText(name + "." + file.extension);
    var tri = new fabric.Rect({
        fill: fileTypeToColor(file.type),
        height: DEFAULT_SHAPE_SIZE,
        width: DEFAULT_SHAPE_SIZE,
        originX: 'center',
        originY: 'center',
        stroke: 'grey',
        strokeWidth: 1
    });
    finishGroup(name, [tri, text], pos, "file");
}

function finishGroup(name, items, pos, type) {
    var group = new fabric.Group(items, {
        originX: 'center',
        originY: 'center',
        left: pos[0],
        top: pos[1]
    });
    group.set('selectable', false);
    canvas.add(group);

    // Define what to do on click
    group.on('mouseup', function(e) {
        if (!SHIFT_HELD) {
            //console.log(name + " clicked");
            if (type == "file") {
                focusOnFile(name);
            } else if (type == "keyword") {
                focusOnKeyword(name);
            } else if (type == "folder") {
                focusOnFolder(name);
            } else {
                console.log("uh oh");
            }
        } else {
            if (type == "file") {
                //console.log("OPEN " + name + "???");
                openInNewTab("/view?file=" + name);
                // When the new window opens the release isn't caught but we just assume
                SHIFT_HELD = false;
            }
        }

    });
}

function wordText(name) {
    return new fabric.Text(name, {
      fontSize: DEFAULT_SHAPE_SIZE / 8,
      originX: 'center',
      originY: 'center'
    });
}

function markCenter() {
    var triangle = new fabric.Triangle({
      width: 20, height: 20, fill: 'green', originX: 'center',
      originY: 'center', left: WHOLE_CENTER[0], top: WHOLE_CENTER[1]
    });
    triangle.set('selectable', false);
    canvas.add(triangle);
}


function clearCanvas() {
    var all = canvas.getObjects();
    for (var i = 0; i < all.length; i++) {
        canvas.remove(all[i]);
    }
}
