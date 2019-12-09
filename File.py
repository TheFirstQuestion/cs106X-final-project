import json
import ocr
import nlp
import pypandoc
from tika import parser
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

####### CONSTANTS #######
FREQ_CUTOFF_WORD = 0.01
WEIGHT_KEYWORD = 3
WEIGHT_FOLDER = 5
WEIGHT_FILENAME = 4
#########################

# Load definitions from json file
with open("definitions.json") as j:
    definitions = json.load(j)

class File(Base):
    __tablename__ = 'File'
    id = Column(Integer, primary_key=True, autoincrement=False)
    path = Column(String(250))
    name = Column(String(250))
    extension = Column(String(250))
    type = Column(String(250))
    contents = Column(String(100000))
    created = Column(DateTime(timezone=True), server_default=func.now())
    folder = relationship("Folder", secondary="ff", back_populates="children")
    keywords = relationship("Keyword", secondary="link", back_populates="files")

    def __init__(self, fullpath, session, counter):
        self.id = counter
        self.path = fullpath
        fps = fullpath.split("/")
        # 1:-1 to exclude '' and the file name
        folders = fps[1:-1]
        # special case: no extension
        if (fps[-1].find(".") == -1):
            self.name = fps[-1]
            self.extension = ""
            self.type = "complicated"
        else:
            # Sometimes file names have . in them
            self.name = ".".join(fps[-1].split(".")[:-1])
            self.extension = fullpath.split(".")[-1].lower()
            # Get type from json
            self.type = definitions[self.extension]
        self.contents = self.readFile()
        self.wordFreq = self.countWords()
        self.phrases = self.getPhrases()
        self.addFolder(folders, session)

        # Add keywords!
        #self.addKeyword(wordToAdd=self.name, weight=WEIGHT_FILENAME, session=session)
        for w in self.wordFreq:
            if (self.wordFreq[w] >= FREQ_CUTOFF_WORD) and (len(w) > 2):
                self.addKeyword(wordToAdd=w, weight=WEIGHT_KEYWORD, session=session)
        for p in self.phrases:
            phrase = " ".join(p)
            self.addKeyword(wordToAdd=phrase, weight=WEIGHT_KEYWORD, session=session)


    def readFile(self):
        # Files that we can't easily read are ignored
        if (self.type == "archive" or self.type == "misc." or self.type == "audio" or self.type == "video" or self.type == "complicated"):
            return None
        # .pdf: use tika instead of Pandoc
        elif (self.extension == "pdf"):
            return parser.from_file(self.path)["content"]
        # Python can read some files natively
        elif (self.extension == "txt" or self.extension == "srt" or self.type == "programming"):
            with open(self.path) as f:
                return f.read()
        # Images: use OCR script
        elif (self.type == "image"):
            return ocr.OCR(self.path)
        # Documents: use Pandoc
        else:
            output = pypandoc.convert_file(self.path, 'plain')
            return output


    def countWords(self):
        if (self.contents == None):
            return None
        return nlp.countWords(self)

    def getPhrases(self):
        if (self.contents == None):
            return None
        return nlp.getCommonPhrases(self)

    def addKeyword(self, wordToAdd, weight, session):
        # Check if already in database, because keyword must be unique and sqlalchemy is dumb and throws an exception
        row = session.query(Keyword).filter(Keyword.word == wordToAdd).first()
        if row is None:
            self.keywords.append(Keyword(kword=wordToAdd, weight=weight))
        else:
            session.add(Link(fileID=self.id, keywordID=row.id))

    def addFolder(self, path, session):
        # Check if already in database, because keyword must be unique and sqlalchemy is dumb and throws an exception
        row = session.query(Folder).filter(Folder.name == path[-1]).first()
        if row is None:
            self.folder.append(Folder(path=path, session=session))
        else:
            session.add(FileAndFolder(fileID=self.id, folderID=row.id))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name  + "." + self.extension


##############################################################
# Smaller classes that File relies on
class Keyword(Base):
    __tablename__ = 'Keyword'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    terms = Column(Integer)
    stem = Column(String)
    files = relationship("File", secondary="link", back_populates="keywords")

    def __init__(self, kword, weight):
        self.word = kword
        self.stem = nlp.stem(self.word)
        self.terms = len(self.word.split(" "))
        self.weight = weight * self.terms

    def __repr__(self):
        return self.word

    def __str__(self):
        return self.word


class Folder(Base):
    __tablename__ = 'Folder'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    path = Column(String(250))
    level = Column(Integer)
    parentID = Column(ForeignKey('Folder.id'))
    parent = relationship("Folder")
    children = relationship("File", secondary="ff", back_populates="folder")

    def __init__(self, path, session):
        self.path = "/".join(path)
        self.name = path[-1]
        self.level = len(path)
        self.parentID = self.findParent(path[:-1], session)
        if (self.parentID is not None):
            self.parent.append(session.query(Folder).filter(Folder.id == self.parentID).one())

    def findParent(self, path, session):
        # Base case: already at root
        if self.level == 1:
            return None

        row = session.query(Folder).filter(Folder.path == "/".join(path)).first()
        if (row is None):
            session.add(Folder(path=path, session=session))
            return self.findParent(path, session)
        else:
            if row.level < self.level:
                return row.id

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Link(Base):
   __tablename__ = 'link'
   id = Column(Integer, primary_key=True)
   fileID = Column(Integer, ForeignKey("File.id"))
   keywordID = Column(Integer, ForeignKey("Keyword.id"))

   def __repr__(self):
       return str(self.fileID) + "->" + str(self.keywordID)

   def __str__(self):
       return str(self.fileID) + "->" + str(self.keywordID)


class FileAndFolder(Base):
   __tablename__ = 'ff'
   id = Column(Integer, primary_key=True)
   fileID = Column(Integer, ForeignKey("File.id"))
   folderID = Column(Integer, ForeignKey("Folder.id"))

   def __repr__(self):
       return str(self.fileID) + "->" + str(self.folderID)

   def __str__(self):
       return str(self.fileID) + "->" + str(self.folderID)

############################################################################
####################################### main
if __name__ == "__main__":
    #f = File("./Example File System/09/Speech/Problem Solving/Pictures/IMG_7124.JPG")
    #f = File("./Example File System/Space-Site/index.html")
    f = File("./Example File System/12/AP Language and Composition/Senior Paper/Sources/The_Californian_Ideology.pdf")
    print(f)
    #print(f.extension)
    #print(f.type)
    #print(f.folders)
    #print(f.path)
    #print(f.contents)
    #print(f.wordFreq)
    print(f.keywords)
