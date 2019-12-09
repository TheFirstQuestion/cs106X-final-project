import glob
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from File import File, Base

##################### Config ###########################
ROOT_OF_FILE_SYSTEM = "./Example File System"
DB_NAME = "DATABASE-WOO.db"
########################################################


if __name__ == "__main__":
    # Connect to database
    engine = create_engine("sqlite:///" + DB_NAME)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine, autoflush=True)
    session = DBSession()
    session.commit()


    files = []
    dirs = []
    # Read configuration files
    with open("extension-blacklist.txt") as f:
        extensionBlacklist = f.read().splitlines()
    with open("folder-blacklist.txt") as f:
        folderBlacklist = f.read().splitlines()

    for path in glob.glob(ROOT_OF_FILE_SYSTEM + "/**", recursive=True):
        if os.path.isdir(path):
            willAppend = True
            name = path.split("/")[-1]
            if name in folderBlacklist:
                willAppend = False
            if willAppend:
                dirs.append(path)
        elif os.path.isfile(path):
            extension = path.split(".")[-1]
            if not (extension in extensionBlacklist):
                files.append(path)

    counter = 0
    for f in files:
        try:
            session.add(File(f, session, counter))
            session.commit()
            counter = counter + 1
        except:
            continue

    session.close()
