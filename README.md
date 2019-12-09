# CS 106X Final Project
### Proposal
For my final project, I'm planning to create some sort of file manager. I would basically create an abstraction over the hierarchical file system so that the user can browse files the way they browse the web: by searching and pulling together bits and pieces from files in different locations.

The use cases would look something like this: I search for a quote that I don't remember the source of but know I have saved somewhere -- the results point to an essay I wrote in middle school, as well as subtitles from the movie the essay is about. I need to quickly create a GitHub README but don't have a template saved -- I can search and see all the READMEs I have saved, across multiple folders/projects.

There would also be some sort of non-linear browsing mode -- so you can see all english papers you've written, or test report PDFs, no matter what folders they might be in. In this case, the user could browse by tag/topic/keyword rather than folder; the many-to-many scheme is much more flexible and similar to how people think.

The underlying structure will probably include a map for tags, and linked data structures of some type for the searching part. I will look into what algorithms Google and other search engines use to be able to quickly search through millions of pages of text.

I’m leaning towards writing it in Python, using HTML/CSS for a simple GUI, but C++ or a shell script might be better for the low-level file system part. Depending on how long the scanning/processing of the file system takes, I will probably cache the results in a database.

### Jerry's Response
Wow, Sophie.  I love this so much!.
I am slightly concerned that it's more than I would really expect from a CS106X student, but if you're willing to complete a significant chunk of it -- maybe the server-side portion of the web app and leaving the web work to be completed for a personal project -- then that would be fine with me as well.  But I love the creativity and the ambition, so I want you to do as much of it as you have time for.

### Further Notes
This is a proof-of-concept, not a production system. There are a lot of file types that are simply ignored. Both the OCR and NLP implementations are very rudimentary and really not at all good at their job. I do think it provides a good model as to what the future of file managers may look like.
Also: notice that you can't open files natively! This is because your browser doesn't permit access to your operating system (which is a very, very good thing).

---

## Dependencies
* `apt-get install tesseract-ocr pandoc`
* `python3 -m pip install pytesseract opencv-python pypandoc sqlalchemy tika nltk marshmallow marshmallow-sqlalchemy flask`

## Configuration
#### Required
* `initializeDatabase.py`:
** `ROOT_OF_FILE_SYSTEM`: the root of the file system; all folders within it will be searched; this path should be relative to the location of `main.py`

#### Optional
* `config/extension-blacklist.txt`: a list of extensions for files to ignore, i.e. caches; one per line
* `config/folder-blacklist.txt`: a list of folders to ignore, i.e. libraries, bin; one per line
* `config/definitions.json`: categorizes extensions into types of files, which determines how they are read
* `initializeDatabase.py`:
** `DB_NAME`: the name of the database file (including extension)

## Running
* `python3 setup.py` (once) -- downloads nltk data
* `python3 initializeDatabase.py` -- rescans all the files to generate the database; may take a while!
* `python3 main.py`

Click on a file or keyword to focus on it. Type into the box to search for keywords (case sensitive). Hold shift while clicking on a file to "open" the file (in a new window).

---

## TODO
* create makefile?
* multiple keyword filters
    * once chosen, go to top of screen, click again to un-choose
* add weight calculations into ordering display, choosing which (in init too)
* ability to search whole contents
* make drawing a shape one function, independent of keyword/folder/file
* UI tweaks:
    * animations!
    * add lines? (dashed, slightly darker blue)
    * shadow text box?
    * adjust number of items shown at different times
* Fixes (not  mission critical):
    * `'NoneType object is not iterable'`
    * `libpng warning: iCCP: known incorrect sRGB profile`
    * `Premature end of JPEG file`
    * `Pandoc died with exitcode "1" during conversion: b"pandoc: couldn't parse docx file\nCallStack (from HasCallStack):\n  error, called at src/Text/Pandoc/Error.hs:55:28 in pandoc-1.19.2.4-HbfKWUyODESBIy0vGktOwX:Text.Pandoc.Error\n"`
* add more keyword options
    * folder names -- also add individual words (split on space, dash, underscore, camelCase?)
    * also, folder/file names can conflict with keywords (case sensitive?)
    * some sort of proper noun lookup?
* generalize keywords semantically
    * ie, calculus --> math
    * music --> music type files
    * programming words --> programming files

---

## (Tentative) Relevance Weights
```
when user searches for word / words...

is keyword: 3 (programming: * 0.25)
shares stem w/ keyword: 2 (programming: * 0.25)
matches phrase: 3 * length of phrase (programming: * 0.5)

is whole file name: 2 * length of file name
is part of file name: 6

is whole folder name: 5
is part of folder name: 4

is whole folder name of a parent: 5 / levels between
is part of folder name: 4 / levels between
```

## UI Design
Folder = rectangle
File = triangle
Keyword = circle

keyword = white
folder = yellow

documents = green
image = blue
programming = purple
misc. = red

audio, archive, video = pink


---

## Resources

[digital abstract book from last quarter](https://web.stanford.edu/class/archive/cs/cs106x/cs106x.1194/projects.html)
