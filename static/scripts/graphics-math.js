// First point is at 3:00
function circlePoints(center, radius, numPoints) {
    var points = [];
    var theta = 2 * Math.PI / numPoints;
    for (var i = 0; i < numPoints; i++) {
        var angle = theta * i;
        var x = center[0] + (radius * Math.cos(angle));
        var y = center[1] + (radius * Math.sin(angle));
        points.push([x, y]);
    }
    return points;
}

// Points beneath the horizontal, evenly spaced
function semicirclePoints(center, radius, numPoints) {
    var points = [];
    var theta = Math.PI / (numPoints + 1);
    for (var i = 1; i <= numPoints; i++) {
        var angle = theta * i;
        var x = center[0] + (radius * Math.cos(angle));
        var y = center[1] + (radius * Math.sin(angle));
        points.push([x, y]);
    }
    return points;
}

// Doesn't place points at 0 or totalWidth
function evenlySpacedHorizontalPoints(center, totalWidth, numPoints) {
    var offset = totalWidth / (numPoints + 1);
    var zero = center[0] - (offset * (numPoints + 1) / 2.0);
    var points = [];
    for (var i = 1; i <= numPoints; i++) {
        points.push([zero + (offset * i), center[1]]);
    }
    return points;
}

function randomPoint() {
    var x = Math.floor((Math.random() * WHOLE_WIDTH) + 1);
    var y = Math.floor((Math.random() * WHOLE_HEIGHT) + 1);
    return [x, y];
}

function gridPoints(center, width, numPoints) {
    var points = [];
    var numPerRow = Math.min(Math.floor(width / (1.25 * DEFAULT_SHAPE_SIZE)), 1);
    var numRows = Math.min(Math.floor(numPoints / numPerRow), 1);
    var verticalOffset = DEFAULT_SHAPE_SIZE * 1.25;

    for (var i = 0; i < numRows; i++) {
        var rowCenter = [center[0], center[1] + (verticalOffset * i)];
        points = points.concat(evenlySpacedHorizontalPoints(rowCenter, width, numPerRow));
    }
    return points;
}
