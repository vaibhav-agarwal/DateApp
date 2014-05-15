import MySQLdb as mdb
import MySQLdb.cursors
con=mdb.connect( host='localhost', user='loginname',
    passwd='password', db='databasename',
    cursorclass=MySQLdb.cursors.DictCursor)

cur = con.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS Users(id VARCHAR(30) PRIMARY KEY ,gcm_registration_id VARCHAR(700),coolname VARCHAR(20) , email VARCHAR(25) , " +
    "password VARCHAR(700), birthday VARCHAR(10) , gender VARCHAR(1),seeking VARCHAR(1) , city VARCHAR(20) , " +
    "country VARCHAR(20) , pic VARCHAR(700), last_Login VARCHAR(75), shout VARCHAR(150)," +
    "user_Favourites VARCHAR(300) , user_TV VARCHAR(300) , user_Music  VARCHAR(300) , user_Movies VARCHAR(300) , user_Badges VARCHAR(300)," +
    "user_Flag VARCHAR(1) , user_Answers VARCHAR(300), picUrls  VARCHAR(700))")

cur.execute(
    "CREATE TABLE IF NOT EXISTS Movies(movie_id VARCHAR(30) PRIMARY KEY , movie_name VARCHAR(100) , movie_Coverpic VARCHAR(700)) ")

cur.execute(
    "CREATE TABLE IF NOT EXISTS Music(music_id VARCHAR(30) PRIMARY KEY , music_name VARCHAR(100) , music_Coverpic VARCHAR(700)) ")

cur.execute(
    "CREATE TABLE IF NOT EXISTS TV(tv_id VARCHAR(30) PRIMARY KEY , tv_name VARCHAR(100) , tv_Coverpic VARCHAR(700) )")

cur.execute(
    "CREATE TABLE IF NOT EXISTS Badges( badge_id VARCHAR(30) PRIMARY KEY , badge_Name VARCHAR(100) , badge_Pic VARCHAR(700) )")

cur.execute(
    "CREATE TABLE IF NOT EXISTS Activity(activity_id INT PRIMARY KEY AUTO_INCREMENT , from_id VARCHAR(30) ," +
    "to_id Varchar(30)  , activity_Type VARCHAR(30) , activity_Timestamp VARCHAR(30) )")

cur.execute(
    "CREATE TABLE IF NOT EXISTS Play(play_id INT PRIMARY KEY AUTO_INCREMENT , from_id VARCHAR(30) , " +
    "to_id Varchar(30)  ,picUrl VARCHAR(700), pic_Timestamp VARCHAR(30))")

cur.execute(
    "CREATE TABLE IF NOT EXISTS Chat(chat_id INT PRIMARY KEY AUTO_INCREMENT , from_id VARCHAR(30)  ," +
    "to_id Varchar(30)  , message VARCHAR(300) , seen VARCHAR(1) , chat_Timestamp VARCHAR(30) , sent VARCHAR(20) )")


cur.execute(
    "CREATE TABLE IF NOT EXISTS Distance( distance_id INT PRIMARY KEY AUTO_INCREMENT , city VARCHAR(30)  ," +
    "country VARCHAR(30)  , latitude VARCHAR(30) , longitude VARCHAR(30) )")

cur.execute(
    "CREATE TABLE IF NOT EXISTS Distance1( distance_id INT PRIMARY KEY AUTO_INCREMENT , city VARCHAR(30)  ," +
    "country VARCHAR(30)  , latitude VARCHAR(30) , longitude VARCHAR(30) )")


cur.execute("ALTER TABLE Activity ADD FOREIGN KEY (from_id) REFERENCES Users(id);")
cur.execute("ALTER TABLE Activity ADD FOREIGN KEY (to_id) REFERENCES Users(id);")


cur.execute("ALTER TABLE Play ADD FOREIGN KEY (from_id) REFERENCES Users(id);")
cur.execute("ALTER TABLE Play ADD FOREIGN KEY (to_id) REFERENCES Users(id);")


cur.execute("ALTER TABLE Chat ADD FOREIGN KEY (from_id) REFERENCES Users(id);")
cur.execute("ALTER TABLE Chat ADD FOREIGN KEY (to_id) REFERENCES Users(id);")


