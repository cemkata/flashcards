from bottle import Bottle, request, redirect, template, static_file
import sqlite3
from sqlite3 import Error
import os
import sys
import html
import json

from config import * # App config is loaded here

cwd = os.getcwd()
database = os.path.join(cwd, databaseFile)

app = Bottle()

admin_remark_id = 1

@app.route('/static/<filepath:path>')
def static_content(filepath):
     return static_file(filepath, root='./views/static')
 
@app.route('/favicon.ico')
def favicon():
     return static_file('icon.png', root='./views/static')

@app.route('/')
def show_couse_selection():
     return template('fe_index', courses = get_courses())

@app.route('/showcourse')
def show_course_decks():
     courseID = request.query.courseID or -1
     if courseID == -1:
        redirect("/")
     try:
        int(courseID)
     except ValueError:
        redirect("/")
            
     cName = get_course_name(courseID)
     deck = get_decks(courseID)
     if(len(deck) == 1):
        redirect("/showflashcards?courseID="+str(courseID)+"&deckID=1")
     else:
        return template('fe_showDeck', course_id = courseID, course_name = cName[0], deck = get_decks(courseID))

@app.route('/showflashcards')
def show_flashcard():
     courseID = request.query.courseID or -1
     deckID = request.query.deckID or -1
     if deckID == -1: 
        redirect("/")
     if courseID == -1:
        redirect("/")
     try:
        int(courseID)
        int(deckID)
     except ValueError:
        redirect("/")
        
     return template('fe_slideShow', deckID = deckID, corceID = courseID)

@app.route('/getDeck')
def get_deck():
     #http://127.0.0.1:8081/getDeck?courseID=1&deckID=1
     courseID = request.query.courseID or -1
     deckID = request.query.deckID or -1
     
     if deckID == -1: 
        redirect("/")
     if courseID == -1:
        redirect("/")
     try:
        int(courseID)
        int(deckID)
     except ValueError:
        redirect("/")
        
     sql = "SELECT `answer`, `question` FROM `flashcards_tbl` where course_id = "+ courseID +" and remark="+ deckID
        
     conn = create_connection(database)
     with conn:
        # create a new card
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        fc = []
        for row in rows:
           tmpDic={}
           tmpDic['front']=""
           tmpDic['back']=""

           tmpBack = row[0].splitlines()
           for l in tmpBack:
               tmpDic['back'] += l + "</br>"

           tmpFront = row[1].splitlines()
           for l in tmpFront:
               tmpDic['front'] += l + "</br>"

           fc.append(tmpDic.copy())
     return json.dumps(fc)
     
@app.route('/be')
def redirectToBackEnd():
     redirect("./be/")

@app.route('/be/')
def beckEndIndex():
     return template('be_home', courses = get_courses())
########################
##Card functions start##
########################
@app.route('/be/newCard')
def route_new_card():
     return template('be_add_OR_edit_Card', courses = get_courses())

@app.post('/be/addCard') # or @app.route('/addCard', method='POST')
def route_add_Card():
     question = request.forms.question
     answer = request.forms.answer
     courseID = request.forms.course_id or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/")
     deck_id = request.forms.deck_id or -1
     print(deck_id)
     if deck_id == -1 or deck_id == "-1":
        deck_id = getRemarkIDByNameAndCourseId(courseID, name = "Default deck")
        #get id for default and course id
     # create a new card
     card = (courseID, html.unescape(question), html.unescape(answer));
     card_id = create_card(card, deck_id)
     return template('__done')
    
@app.route('/be/showCards')
def route_show_Cards():
     courseID = request.query.courseID or -1
     deckID = request.query.deckID or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/")
     sql = "SELECT `id`, `course_id`, `question`, `answer` FROM `flashcards_tbl` where course_id = "+ courseID +" AND remark = "+ deckID +" ORDER BY `_rowid_` ASC LIMIT 0, 50000;"
        
     conn = create_connection(database)
     with conn:
        # create a new card
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        fc = []
        for row in rows:
           fc.append(flashcard(row[0], row[1],row[2],row[3]))
        cur.execute("SELECT `name` FROM `courses_tbl` where course_id = " + courseID)
        course_name = cur.fetchone()
     return template('be_all_Cards', flashCards = fc, c_name = course_name[0])

@app.route('/be/editCard')
def route_edit_card():
     #http://127.0.0.1:8081/edit?id=5
     questionID = request.query.id or -1
     if questionID == -1:
        redirect("./")
     try:
        int(questionID)
     except ValueError:
        redirect("/be/")
     conn = create_connection(database)
     with conn:
        cur = conn.cursor()
        cur.execute("SELECT question, answer FROM flashcards_tbl where id == " + questionID)
        rows = cur.fetchone()
        courses = get_courses()
        try:
            return template('be_add_OR_edit_Card', question = rows[0], answer=rows[1], qid = questionID, courses = courses)
        except TypeError:
            return template('be_add_OR_edit_Card', courses = get_courses())
        
@app.post('/be/updateCard') # or @app.route('/updateCard', method='POST')
def route_update_card():
     question = request.forms.question
     answer = request.forms.answer
     courseID = request.forms.course_id or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/")
     qid = request.forms.qid
     deck_id = request.forms.deck_id or -1
     if deck_id == -1 or deck_id == "-1":
        deck_id = getRemarkIDByNameAndCourseId(courseID, name = "Default deck")
     # create a new card
     card = (courseID, html.unescape(question), html.unescape(answer), qid);
     _ = update_card(card)
     update_card_remark(qid, deck_id)
     return template('__done')
     
@app.route('/be/deleteCard')
def route_delete_card():
     #http://127.0.0.1:8081/delete?id=5
     questionID = request.query.id or -1
     if questionID == -1:
        redirect("./")
     try:
        int(questionID)
     except ValueError:
        redirect("/be/")
     conn = create_connection(database)
     with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM flashcards_tbl where id == " + questionID)
        rows = cur.fetchone()
        return template('__done')
########################
##Card functions end  ##
########################

##########################
##Deck functions start  ##
##########################   
@app.route('/be/editDeck')
def route_edit_Deck():
     #http://127.0.0.1:8081/edit?id=5
     courseID = request.query.courseID
     try:
        int(courseID)
     except ValueError:
        redirect("/be/")
     deckID = request.query.deckID
     try:
        int(deckID)
     except ValueError:
        redirect("/be/")
     if deckID != "-1":
        cName = getRemark(courseID, deckID)
        return template('be_add_OR_edit_Deck', deckName = cName[0], did = deckID)
     else:
        return template('be_add_OR_edit_Deck', cid = courseID)

@app.post('/be/addDeck') # or @app.route('/addCard', method='POST')
def route_add_Deck():
     text = request.forms.deckName
     courseID = request.forms.course_id
     _ = create_remark(text, courseID)
     return template('__done')

@app.post('/be/updateDeck') # or @app.route('/updateCard', method='POST')
def route_update_Deck():
     remrk_id = request.forms.did
     text = request.forms.deckName
     _ = update_remark(remrk_id, text)
     return template('__done')
 
@app.route('/be/deleteDeck')
def route_delete_Deck():
     #TODO
     return template('__done')
     #http://127.0.0.1:8081/deleteDeck?id=5
     courseID = request.query.courseID or -1
     deckID = request.query.deckID or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/showcourses")
        
     if deckID == -1 or deckID == admin_remark_id:
        redirect("./")
     try:
        int(deckID)
     except ValueError:
        redirect("/be/showcourses")
     conn = create_connection(database)
     with conn:
        cur = conn.cursor()
        sql = "delete from flashcards_tbl where remark == {}".format(courseID)
        cur.execute(sql)
        sql = "delete from remarks_tbl where remark == {}".format(courseID)
        cur.execute(sql)
     return template('__done')

@app.route('/be/showDecks')
def route_show_Deck():
     courseID = request.query.courseID or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/")
     cName = get_course_name(courseID)
     return template('be_showDeck', course_id = courseID, course_name = cName[0], deck = get_decks(courseID))
     
@app.route('/be/getDecks')
def route_show_Deck():
     courseID = request.query.courseID or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/")
     return json.dumps(get_decks(courseID))
########################
##Deck functions end  ##
########################

##########################
##course functions start##
##########################
@app.route('/be/newcourse')
def route_new_course():
     return template('be_add_OR_edit_course')
 
@app.post('/be/addcourse') # or @app.route('/addcourse', method='POST')
def route_add_course():
     courseID = request.forms.course_id
     courseName = request.forms.name
     courseDescription = request.forms.description
     # create a new course
     if getcourseID(courseID) is not None:
        errStr = "Course id:"+courseID+" already exist."
        return template('be_add_OR_edit_course', name=courseName, description=courseDescription, error_str = errStr)
     else:
        course = (courseID, html.unescape(courseName), html.unescape(courseDescription));
        _ = create_course(course)
        _ = create_remark("Default deck", courseID)
     return template('__done')

@app.route('/be/showcourses')
def route_show_courses():
     return template('be_all_courses', coursesList = get_courses())

@app.route('/be/editcourse')
def route_edit_course():
     #http://127.0.0.1:8081/editcourse?id=5
     courseID = request.query.id or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/showcourses")
     conn = create_connection(database)
     with conn:
        cur = conn.cursor()
        cur.execute("SELECT course_id, name, description FROM courses_tbl where id == " + courseID)
        rows = cur.fetchone()
        return template('be_add_OR_edit_course', course_id = rows[0], name=rows[1], description=rows[2], cid = courseID)

@app.post('/be/updatecourse') # or @app.route('/updatecourse', method='POST')
def route_update_course():
     name = request.forms.name
     description = request.forms.description
     course_id = request.forms.course_id
     cid = request.forms.cid
     course = (course_id, html.unescape(name), html.unescape(description), cid);
     courseid = update_course(course)
     return template('__done')

@app.route('/be/deletecourse')
def route_delete_course():
     #http://127.0.0.1:8081/deletecourse?id=5
     courseID = request.query.id or -1
     if courseID == -1:
        redirect("./")
     try:
        int(courseID)
     except ValueError:
        redirect("/be/showcourses")
     conn = create_connection(database)
     with conn:
        cur = conn.cursor()
        sql = "delete from flashcards_tbl where course_id == (select course_id from courses_tbl where id = {})".format(courseID)
        cur.execute(sql)
        sql = "delete from remarks_tbl where course_id == (select course_id from courses_tbl where id = {})".format(courseID)
        cur.execute(sql)
        cur.execute("DELETE FROM courses_tbl where id == " + courseID)
     return template('__done')
##########################
##course functions end  ##
##########################

class course:
  def __init__(self, id, course_id, name, description):
    self.course_id = course_id
    self.name = name
    self.description = description
    self.id = id

class flashcard:
  def __init__(self, question_id, id, question, answer):
    self.course_id = id
    self.question = question
    self.answer = answer
    self.qid = question_id

######################
##DB functions start##
######################
def get_courses():
     conn = create_connection(database)
     with conn:
        # create a new card
        cur = conn.cursor()
        cur.execute("SELECT `id`, `course_id`, `name`, `description` FROM `courses_tbl` ORDER BY `course_id` ASC LIMIT 0, 50000;")
        rows = cur.fetchall()
        fc = []
        for row in rows:
           fc.append(course(row[0], row[1],row[2],row[3]))
     return fc

def get_course_name(courseID):
     conn = create_connection(database)
     with conn:
        # create a new card
        cur = conn.cursor()
        cur.execute("SELECT `name` FROM `courses_tbl` where `course_id`="+str(courseID)+";")
        rows = cur.fetchone()
     return rows

def get_decks(courseID):
     conn = create_connection(database)
     with conn:
        # create a new card
        cur = conn.cursor()
        #TODO
        sql = '''select rm."id", rm."description" from "remarks_tbl" as rm
                 where rm."course_id" = '''+str(courseID) +''' order by rm."id"'''
        cur.execute(sql)
        rows = cur.fetchall()
        dc = []
        for row in rows:
           tmpDic = {}
           tmpDic['id']=row[0]
           tmpDic['info']=row[1]
           dc.append(tmpDic.copy())
     return dc
   
def update_course(course):
    """
    Create a new project into the projects table
    :param conn:
    :param course
    :return: project id
    """ 
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE courses_tbl SET course_id = ?, name = ?, description = ? WHERE id = ? '''
        cur = conn.cursor()
        cur.execute(sql, course)
        conn.commit()
    return cur.lastrowid

def create_course(course):
    """
    Create a new course into the projects table
    :param conn:
    :param course
    :return: project id
    """
    conn = create_connection(database)
    with conn:
        sql = ''' INSERT INTO courses_tbl(course_id, name, description)
                  VALUES(?,?,?) '''

        cur = conn.cursor()
        cur.execute(sql, course)
        conn.commit()
    return cur.lastrowid

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_card(card, remark = False):
    """
    Create a new flashcard into the projects table
    :param conn:
    :param card
    :return: project id
    """
    conn = create_connection(database)
    with conn:
        sql = ''' INSERT INTO flashcards_tbl(course_id, remark, question, answer)
                  VALUES(?,?,?,?) '''
        if remark:
           new_card = (card[0], remark, card[1], card[2])
        else:
           new_card = (card[0], admin_remark_id, card[1], card[2])
        cur = conn.cursor()
        cur.execute(sql, new_card)
        conn.commit()
    return cur.lastrowid
    
def update_card(card):
    """
    Create a new project into the projects table
    :param conn:
    :param card
    :return: project id
    """ 
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE flashcards_tbl SET course_id = ?, question = ?, answer = ? WHERE id = ? '''
        cur = conn.cursor()
        cur.execute(sql, card)
        conn.commit()
    return cur.lastrowid

def update_card_remark(card_id, remark = False):
    """
    Create a new flashcard into the projects table
    :param conn:
    :param card id
    :param remark id
    :return: project id
    """
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE flashcards_tbl SET remark = ? WHERE id = ? '''
        cur = conn.cursor()
        if remark:
           cur.execute(sql, (remark, card_id))
        else:
           cur.execute(sql, (remark, admin_remark_id))
        conn.commit()
    return cur.lastrowid

def getRemarkIDByNameAndCourseId(courseID, name):
    conn = create_connection(database)
    sql = '''select id from remarks_tbl where description = "'''+name+'''" and course_id = '''+courseID
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return int(cur.fetchone()[0])

def getRemarkIDByName(name = "admin"):
    conn = create_connection(database)
    sql = '''select id from remarks_tbl where description = "'''+name+'''"'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return int(cur.fetchone()[0])

def getRemark(course_id, remrk_id):
     conn = create_connection(database)
     with conn:
        cur = conn.cursor()
        sql = '''select description from remarks_tbl where course_id = "'''+course_id+'''" and id = "'''+remrk_id+'''"'''
        cur.execute(sql)
        rows = cur.fetchone()
     return rows

def update_remark(remrk_id, text):
    """
    Update a new remark into the projects table
    :param conn:
    :param remrk_id
    :param text
    :return: None
    """
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE remarks_tbl SET description = ? WHERE id = ? '''
        cur = conn.cursor()
        cur.execute(sql, (text, remrk_id))
        conn.commit()
    return cur.lastrowid

def create_remark(remark, cid):
    """
    Create a new remark into the projects table
    :param conn:
    :param card
    :return: project id
    """
    sql = ''' INSERT INTO remarks_tbl(description, course_id) VALUES (?, ?);'''
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute(sql, (remark, cid))
        conn.commit()
    return cur.lastrowid

def getcourseID(course_ID):
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id from courses_tbl where course_id == " + course_ID)
    return cur.fetchone()

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def createDB():
    sql_create_flashcards_table = """ CREATE TABLE IF NOT EXISTS "flashcards_tbl" (
                                        "id" integer PRIMARY KEY,
                                        "course_id" integer NOT NULL,
                                        "remark" integer NOT NULL,
                                        "question" text NOT NULL,
                                        "answer" text NOT NULL
                                    ); """
                                    
    sql_create_courses_table = """ CREATE TABLE IF NOT EXISTS "courses_tbl" (
                                        "id" integer PRIMARY KEY,
                                        "course_id" integer NOT NULL UNIQUE,
                                        "name" text NOT NULL,
                                        "description" text
                                    ); """

    sql_create_remarks_table = """ CREATE TABLE IF NOT EXISTS "remarks_tbl" (
                                        "id"	INTEGER,
                                        "description"	text NOT NULL,
                                        "course_id"	INTEGER NOT NULL,
                                        PRIMARY KEY("id" AUTOINCREMENT)
                                    ); """
    # create a database connection
    if os.path.exists(database):
       os.remove(database)

    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create table
        create_table(conn, sql_create_flashcards_table)
        create_table(conn, sql_create_courses_table)
        create_table(conn, sql_create_remarks_table)
        create_remark("admin")
        print("Done!")
    else:
        print("Error! cannot create the database connection.")

######################
##DB functions end  ##
######################

def bulkAdd(filename, remark, courseID):
     with open(filename, "r" , encoding="utf8") as infile:    # save
          content = infile.read()
     strngs = content.split("_e_n_d_")
     question = 0
     answer = 1
     if getcourseID(courseID) is None:
         print("course id does not exist exist. Please add it via the webinterface.")
         return

     if remark != False:
        remark = create_remark(remark)
     for s in range(0, len(strngs)-1):
         fin = strngs[s].split("_b_a_c_k_")
         card = (courseID, html.unescape(fin[question]), html.unescape(fin[answer]));
         card_id = create_card(card, remark)

def exportDeck(courseID, deckID):
     sql = "SELECT `answer`, `question` FROM `flashcards_tbl` where course_id = "+ courseID +" and remark="+ deckID
        
     conn = create_connection(database)
     with conn:
        # create a new card
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        fc = []
        with open("deck_"+courseID+"_"+deckID+".txt", "w") as f:
            for row in rows:
               f.write(row[0]+"_b_a_c_k_"+row[1]+"_e_n_d_")

def backUpDB():
    import shutil
    from datetime import date
    import glob
    print("Backup starts.")
    today = date.today()
    backUpName = databaseFile + "_backup_" + str(today.year) + "_" + str(today.month) + "_" + str(today.day)
    databaseNew = os.path.join(cwd, backUpName)
    #COMPRESS the back up file
    if backup_compress:
    #    import gzip
    #    with open(database, 'rb') as f_in:
    #        with gzip.open(databaseNew + ".gz", 'wb') as f_out:
    #           shutil.copyfileobj(f_in, f_out)
    ### use tar+gzip
        import tarfile
        with tarfile.open(databaseNew + ".tgz", "w:gz") as tar:
            tar.add(database, arcname=databaseFile)
    else:
        shutil.copy2(database, databaseNew)
    if maxDBbackups < 0: # diseble the backups cleanup (unlimited backups)
       return
    listing = glob.glob('./' + databaseFile +'_backup_*')
    listing.sort(key=os.path.getmtime)
    if len(listing) > maxDBbackups:
        lastFile = os.path.join(cwd, listing[0])
        if os.path.exists(lastFile):
           os.remove(lastFile)
    print("Backup done.")
    print("Backup name: " + backUpName + ".tgz")

def restoreDB(fname):
    import shutil
    import tarfile
    if fname.endswith("tar.gz") or fname.endswith("tgz"):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall()
        tar.close()
    elif fname.endswith("tar"):
        tar = tarfile.open(fname, "r:")
        tar.extractall()
        tar.close()
    else:
        shutil.copy2(fname, databaseFile)

def showHelp():
    print("""
    -h shows this help
    -cdb creates the database
    -bckp creates a database
    -rstr backUpfile
    -cnfg show the server configuration
    -imp <file name> <Remark optional> <course id> the name for bulck add
    -expt <corce,deck> i.e. 1,1
    
    The file format is as folows: (The new line, tabs and other specila chars are ignored. use the formant below)
    cardFront_b_a_c_k_cardBack_e_n_d_cardFront_b_a_c_k_cardBack_e_n_d_cardFront_b_a_c_k_cardBack_e_n_d_""")

def main():
    global admin_remark_id
    admin_remark_id = getRemarkIDByName()
    app.run(host = serverAddres, port = serverPort, debug=True)

if __name__ == '__main__':
  print("")
  print("Starting flashcards version " + str(ver))
  print("")
  try:
    if sys.argv[1:][0] == "-cdb":
       #try:
       #     backUpDB()
       #     print("Backup of the old badabase created.")
       #except FileNotFoundError as e:
       #     print("[Info] Backup failed.\n       No previous database found.")
       createDB()
    elif sys.argv[1:][0] == "-bckp":
       backUpDB()
    elif sys.argv[1:][0] == "-rstr":
       try:
           filename = sys.argv[1:][1]
           restoreDB(filename)
       except IndexError:
           print("No input file.")
    elif sys.argv[1:][0] == "-imp":
       try:
           filename = sys.argv[1:][1]
       except IndexError:
           print("No input file.")
       try:
           remark = sys.argv[1:][2]
       except IndexError:
           remark = False
       try:
           courseID = sys.argv[1:][3]
       except IndexError:
           print("No course id.")
       try:
           backUpDB()
           bulkAdd(sys.argv[1:][1], remark, courseID)
           print("Import done.")
       except FileNotFoundError as e:
           print(e)   
    elif sys.argv[1:][0] == "-expt":
       try:
           tmpStr = sys.argv[1:][1]
           corce,deck = tmpStr.split(',')
           exportDeck(corce, deck)
       except IndexError:
           print("No input file.")           
    elif sys.argv[1:][0] == "-cnfg":
       print("Database file  " + databaseFile)
       print("Max DB backup  " + str(maxDBbackups))
       print("Server address " + serverAddres)
       print("Server port    " + str(serverPort))
       print("")
       print("Working folder " + cwd)
    elif len(sys.argv[1:][0]) > 0:
       showHelp()
  except IndexError: #No start parameters just call main
       main()
