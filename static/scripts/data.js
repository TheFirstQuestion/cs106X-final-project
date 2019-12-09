function getKeyword(word) {
    // Assumes the word exists
    for (var i = 0; i < ALL_THE_KEYWORDS.length; i++) {
        if (ALL_THE_KEYWORDS[i].word == word) {
            return ALL_THE_KEYWORDS[i];
        }
    }
}

function getFile(name) {
    // Assumes the file exists
    for (var i = 0; i < ALL_THE_FILES.length; i++) {
        if (ALL_THE_FILES[i].name == name) {
            return ALL_THE_FILES[i];
        }
    }
}

function getFolder(name) {
    // Assumes the file exists
    for (var i = 0; i < ALL_THE_FOLDERS.length; i++) {
        if (ALL_THE_FOLDERS[i].name == name) {
            return ALL_THE_FOLDERS[i];
        }
    }
}

function filesFromKeyword(w) {
    var word = getKeyword(w);
    var files = word.files;
    return files;
}

function keywordsFromFile(f) {
    var file = getFile(f);
    var words = file.keywords;
    return words;
}

function subfoldersOfFolder(name) {
    console.log("name: " + name);
    var children = [];
    for (var i = 0; i < ALL_THE_FOLDERS.length; i++) {
        var parent = ALL_THE_FOLDERS[i].parent[0];
        if (typeof parent !== 'undefined') {
            console.log(parent.name);
            if (parent.name == name) {
                console.log(ALL_THE_FOLDERS[i]);
                children.push(ALL_THE_FOLDERS[i]);
            }
        }
    }
    return children;
}

function fileTypeToColor(type) {
    if (type == "document") {
        return "green";
    } else if (type == "image") {
        return "blue";
    } else if (type == "programming") {
        return "purple";
    } else if (type == "misc.") {
        return "red";
    } else {
        return "pink";
    }
}

function calculateWeight(keyword) {
    var occurances = keyword.files;
    var weight = occurances.length;
    for (var i = 0; i < occurances.length; i++) {
        var file = occurances[i];
        weight += keyword.terms;
        if (file.type == "programming") {
            weight /= 4;
        }
    }
    return weight;
}

function suggestKeywords(typedText) {
    var possibilities = [];
    for (var i = 0; i < ALL_THE_KEYWORDS.length; i++) {
        var thisWord = ALL_THE_KEYWORDS[i];
        if (thisWord.word.startsWith(typedText)) {
            possibilities.push(thisWord);
        }
    }

    return possibilities;
}
