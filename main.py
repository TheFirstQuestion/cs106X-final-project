from File import File, Keyword, Link
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Schema import *
from flask import Flask, render_template,redirect, url_for, request
from initializeDatabase import ROOT_OF_FILE_SYSTEM, DB_NAME
app = Flask(__name__)

def openDB():
    engine = create_engine("sqlite:///" + DB_NAME)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def getFiles():
    session = openDB()
    schema = FileSchema()
    myList = []
    # Serialize into json
    all = session.query(File).order_by(File.id)
    for f in all:
        myList.append(schema.dumps(f))
    session.close()
    #print(myList)
    return myList

def getFolders():
    session = openDB()
    schema = FolderSchema()
    myList = []
    # Serialize into json
    all = session.query(Folder).order_by(Folder.level)
    for f in all:
        myList.append(schema.dumps(f))
    session.close()
    #print(myList)
    return myList

def getKeywords():
    session = openDB()
    schema = KeywordSchema()
    # Sort by number of occurances
    wordList = []
    allWords = session.query(Keyword).all()
    for word in allWords:
        freq = len(session.query(Link).filter(Link.keywordID == word.id).all())
        wordList.append([word, freq])
    wordList = sorted(wordList, key=lambda k: k[1], reverse=True)

    # Serialize into json
    myList = []
    for w in wordList:
        myList.append(schema.dumps(w[0]))
    session.close()
    #print(myList)
    return myList

def getFile(name):
    session = openDB()
    schema = FileSchema()
    file = session.query(File).filter(File.name == name).one()
    f = schema.dumps(file)
    session.close()
    return f

################################### Views ##########################

@app.route("/")
def main():
    return render_template('index.html', PYTHON_ALL_FILES=getFiles(), PYTHON_ALL_KEYWORDS=getKeywords(), PYTHON_ALL_FOLDERS=getFolders(), root=ROOT_OF_FILE_SYSTEM)

@app.route("/view")
def view():
    file = getFile(request.args.get("file"))
    return render_template('viewer.html', FILE=file)

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'), code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
