import datetime
import requests
import json
import base64
from flask import Flask, request
from flask.ext import restful
from flask.ext.restful import reqparse
from math import radians, cos, sin, atan2, sqrt

#import database                                                                              #To create database tables
con=""
cur=""
import MySQLdb as mdb
import MySQLdb.cursors
con=mdb.connect( host='localhost', user='login',
                 passwd='password', db='databasename',
                 cursorclass=MySQLdb.cursors.DictCursor )


cur = con.cursor()

app = Flask(__name__)
api = restful.Api(app)

#######################################################################################################################

ruser = reqparse.RequestParser()                                                           #Parameters for register_user
ruser.add_argument('login_id', type=str, required=True, location='form')
ruser.add_argument('password', type=str, required=True, location='form')
ruser.add_argument('gcm_registration_id', type=str, required=True, location='form')

suser = reqparse.RequestParser()                                                                #Parameters for signup
suser.add_argument('login_id', type=str, required=True, location='form')
suser.add_argument('coolname', type=str, required=True, location='form')
suser.add_argument('email', type=str, required=True, location='form')
suser.add_argument('birthday', type=str, required=True, location='form')
suser.add_argument('gender', type=str, required=True, location='form')
suser.add_argument('seeking', type=str, required=True, location='form')
suser.add_argument('city', type=str, required=True, location='form')
suser.add_argument('country', type=str, required=True, location='form')
suser.add_argument('pic', type=str, required=True, location='form')
suser.add_argument('shout', type=str, required=True, location='form')
suser.add_argument('favourites', type=str, required=True, location='form')
suser.add_argument('tvseries', type=str, required=True, location='form')
suser.add_argument('movies', type=str, required=True, location='form')
suser.add_argument('music', type=str, required=True, location='form')
suser.add_argument('badges', type=str, required=True, location='form')
suser.add_argument('picurls', type=str, required=True, location='form')
suser.add_argument('answers', type=str, required=True, location='form')

guser = reqparse.RequestParser()                                                               #Parameters  for get_user
guser.add_argument('login_id', type=str, required=True, location='args')
guser.add_argument('skip', type=str, required=True, location='args')
guser.add_argument('limit', type=str, required=True, location='args')
guser.add_argument('latitude', type=str, required=True, location='args')
guser.add_argument('longitude', type=str, required=True, location='args')

fuser = reqparse.RequestParser()                                                          #Parameters for get_favourites
fuser.add_argument('login_id', type=str, required=True, location='args')
fuser.add_argument('skip', type=str, required=True, location='args')
fuser.add_argument('limit', type=str, required=True, location='args')


puser = reqparse.RequestParser()                                                             #Parameters for get_profile
puser.add_argument('current_id', type=str, required=True, location='args')
puser.add_argument('login_id', type=str, required=True, location='args')
puser.add_argument('name', type=str, required=True, location='args')

cuser = reqparse.RequestParser()                                                        #Parameters for get_current_user
cuser.add_argument('login_id', type=str, required=True, location='args')

nuser = reqparse.RequestParser()                                                     #Parameters for update_notification
nuser.add_argument('from_id', type=str, required=True, location='form')
nuser.add_argument('to_id', type=str, required=True, location='form')
nuser.add_argument('type', type=str, required=True, location='form')
nuser.add_argument('name', type=str, required=True, location='form')

pluser = reqparse.RequestParser()                                                           #Parameters for play_details
pluser.add_argument('seeking', type=str, required=True, location='args')
pluser.add_argument('skip', type=str, required=True, location='args')
pluser.add_argument('limit', type=str, required=True, location='args')


rauser = reqparse.RequestParser()                                                           #Parameters for rate_picture
rauser.add_argument('from_id', type=str, required=True, location='form')
rauser.add_argument('to_id', type=str, required=True, location='form')
rauser.add_argument('pic', type=str, required=True, location='form')
rauser.add_argument('name', type=str, required=True, location='form')

luser = reqparse.RequestParser()                                                                   #Parameters for login
luser.add_argument('login_id', type=str, required=True, location='form')

duser= reqparse.RequestParser()                                                                 #Parameters for get_data
duser.add_argument('type', type=str, required=True, location='args')

gcuser=reqparse.RequestParser()
gcuser.add_argument('login_id', type=str, required=True, location='form')
gcuser.add_argument('gcm_registration_id', type=str, required=True, location='form')

uplimage=reqparse.RequestParser()
uplimage.add_argument('login_id', type=str, required=True, location='args')
uplimage.add_argument('base64image', type=str, required=True, location='args')

response= {  "error":"True" ,                                                                      #Basic Error Response
             "success":"False"
            }

response1={  "error":"False" ,                                                                   #Basic Success Response
             "success":"True",
            }
imagecount=0
#######################################################################################################################

def send_gcm_notification(notificationtype,fromid,pic,name,profilepic,toid,recenttime):                           #Send GCM Notification

    ab={ 'type'   : notificationtype,
        'from_id' : fromid,
         'picurl' : pic,
         'name'   : name,
         'pic'    : profilepic, 
         'time'   : recenttime }

    cur.execute("SELECT gcm_registration_id from Users WHERE user_Flag=1 AND id ='"+toid+"'")
    con.commit()
    a=cur.fetchall()

    gcm_registration_id=a[0]['gcm_registration_id']

    l=[]
    l.append(gcm_registration_id)

    json_data = { "registration_ids" : l ,
                  "data" :  ab}

    url = 'https://android.googleapis.com/gcm/send'

    apiKey = "Enter the key"
              
    myKey = "key=" + apiKey

    data = json.dumps(json_data)

    headers = {'Content-Type': 'application/json',
               'Authorization': myKey}

    response = requests.post(url,data=data,headers=headers)

    print response.status_code

    content = json.loads(response.content)

    print content

########################################################################################################################

class Register_User(restful.Resource):


    def post(self):


        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = ruser.parse_args()


        if len(args['login_id'])==0:

            e=dict(response)
            e["error_Message"]="Invalid Id"
            e["error_Code"]="102"
            return e

        elif 0 in [len(args['password']) , len(args['gcm_registration_id']) ]:

            e=dict(response)
            e["error_Message"]="Invalid User Inputs"
            e["error_Code"]="105"
            return e

        else:
            cur.execute("SELECT Id from Users WHERE Id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()

            if len(a) == 0:
                 cur.execute("INSERT INTO Users (id,password,user_Flag,last_Login,gcm_registration_id) VALUES ( " +
                             str(args['login_id']) + " , '" + str(args['password']) + "' , " +str('0') + ", '" +
                             str(datetime.datetime.now())+"' ,'"+str(args['gcm_registration_id']) +"')")
                 con.commit()
                 print response1
                 return response1

            elif len(a)!=0:
                 e=dict(response)
                 e["error_Message"]="User Already Exists"
                 e["error_Code"]="103"
                 return e


########################################################################################################################

class User_Signup(restful.Resource):


    def post(self):


        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = suser.parse_args()

        if len(args['login_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Login Id"
            e["error_Code"]="102"
            return e


        elif 0 in  [len(args['login_id']), len(args['coolname']), len(args['email']) ,
                    len(args['birthday']), len(args['gender']),len(args['seeking']),
                    len(args['city']), len(args['country']),len(args['pic']),
                    len(args['shout']),len(args['favourites']),len(args['tvseries']),
                    len(args['movies']), len(args['music']),len(args['badges']),
                    len(args['picurls']),len(args['answers'])]:
            e=dict(response)
            e["error_Message"]="Invalid User Input/Inputs"
            e["error_Code"]="105"
            return e

        else:

            cur.execute("SELECT id from Users WHERE Id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()
            if len(a)==0:
                 e=dict(response)
                 e["error_Message"]="User Does Not Exists"
                 e["error_Code"]="101"
                 return e

            if str(args['favourites'])=='EMPTY' and  str(args['shout'])=='EMPTY' and str(args['picurls'])=='EMPTY':
                a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                args['seeking']) + \
                "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                args['pic']) + "' ,"+ \
                "user_TV='" + str(
                args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                args['badges']) + "' ,user_Flag='" + str(1) + "' ,user_Answers='"+str(
                args['answers'])+"'  WHERE id=" + str(args['login_id'])


            elif str(args['favourites'])=="EMPTY":

                if str(args['shout'])=="EMPTY":
                    a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' , picUrls='"+str(args['picurls'])+ "' , user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])


                elif str(args['picurls'])=="EMPTY":
                    a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,shout='" + str(args['shout']) + "' ,"+ \
                    "user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' ,user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])


                else:
                    a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,shout='" + str(args['shout']) + "' ,"+ \
                    "user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' , picUrls='"+str(args['picurls'])+ "' , user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])

            elif str(args['shout'])=="EMPTY":

                if str(args['favourites'])=="EMPTY":

                    a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,"+ \
                    "user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' , picUrls='"+str(args['picurls'])+ "' , user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])

                elif str(args['picurls'])=="EMPTY":
                        a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                        "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                        args['seeking']) + \
                        "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                        args['pic']) + "' ,"+ \
                        "user_Favourites='" + str(args['favourites']) + "' ,user_TV='" + str(
                        args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                        "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                        args['badges']) + "' ,user_Flag='" + str(1) + "' ,  user_Answers='"+str(
                        args['answers'])+"'  WHERE id=" + str(args['login_id'])

                else:
                        a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,"+ \
                    "user_Favourites='" + str(args['favourites']) + "' ,user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' , picUrls='"+str(args['picurls'])+ "' , user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])



            elif str(args['picurls'])=="EMPTY":


                if str(args['favourites'])=="EMPTY":
                    a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,shout='" + str(args['shout']) + "' ,"+ \
                    "user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' ,  user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])

                elif str(args['shout'])=="EMPTY":
                    a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,"+ \
                    "user_Favourites='" + str(args['favourites']) + "' ,user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' , user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])

                else:
                        a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                    "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                    args['seeking']) + \
                    "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                    args['pic']) + "' ,shout='" + str(args['shout']) + "' ,"+ \
                    "user_Favourites='" + str(args['favourites']) + "' ,user_TV='" + str(
                    args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                    "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                    args['badges']) + "' ,user_Flag='" + str(1) + "' , user_Answers='"+str(
                    args['answers'])+"'  WHERE id=" + str(args['login_id'])


            else:
                a = "UPDATE Users SET coolname='" + str(args['coolname']) + "' ,email='" + str(args['email']) + \
                "' ,birthday='" + str(args['birthday']) + "' ,gender='" + str(args['gender']) + "' ,seeking='" + str(
                args['seeking']) + \
                "' ,city='" + str(args['city']) + "' ,country='" + str(args['country']) + "' ,pic='" + str(
                args['pic']) + "' ,shout='" + str(args['shout']) + "' ,"+ \
                "user_Favourites='" + str(args['favourites']) + "' ,user_TV='" + str(
                args['tvseries']) + "' ,user_Music='" + str(args['music']) + \
                "' ,user_Movies='" + str(args['movies']) + "' ,user_Badges='" + str(
                args['badges']) + "' ,user_Flag='" + str(1) + "' , picUrls='"+str(args['picurls'])+ "' , user_Answers='"+str(
                args['answers'])+"'  WHERE id=" + str(args['login_id'])

            cur.execute(a)
            con.commit()
            return response1


########################################################################################################################

class Get_User(restful.Resource):

    def get(self):


        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = guser.parse_args()


        if len(args['login_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Id"
            e["error_Code"]="102"
            return e

        elif 0 in [len(args['skip']),len(args['limit'])] or int(args['skip'])<0 or int(args['limit'])<=0:
            e=dict(response)
            e["error_Message"]="Skip/Limit error"
            e["error_Code"]="111"
            return e

        elif 0 in [len(args['latitude']) ,len(args['longitude']) ] or int(args['latitude']) not in range(-90,90) \
            or int(args['longitude']) not in range(-180,180):

            print int(args['latitude'])
            e=dict(response)
            e["error_Message"]="Invalid Latitude/Longitude"
            e["error_Code"]="104"
            return e


        elif args['login_id']=="000":

            cur.execute("SELECT id,coolname,city,country,last_Login,pic,gender,birthday As age,picUrls,shout from Users WHERE user_Flag=1")
            con.commit()
            a =cur.fetchall()
            print a

            distflag=0
            dist=self.rgeocode(a,distflag,args)
            if distflag==0:

                ids=[]
                distances=[]
                for v in sorted(dist.items(),key=lambda x: x[1]):
                    ids.append(v[0])
                    distances.append(v[1])

                record=[]
                for i in range(len(ids)):
                    for j in range(len(a)):
                        if a[j]['id']==ids[i]:
                            record.append(a[j])

                if len(record)<1:
                    e=dict(response)
                    e["error_Message"]="No Records Found"
                    e["error_Code"]="113"
                    return e

                for i in range(len(record)):
                    record[i]['age']=str(datetime.date.today().year-int(record[i]['age'].split('/')[2]))

                flag=0
                if len(record)-1<int(args['skip']):
                    flag=1

                elif int(args['skip'])+int(args['limit'])>=len(record):
                    record=record[int(args['skip']):len(record) ]

                elif int(args['skip'])+int(args['limit'])<len(record):
                    record=record[int(args['skip']):int(args['skip'])+int(args['limit'])]

                if flag==1:
                    e=dict(response)
                    e["error_Message"]="No More Records"
                    e["error_Code"]="115"
                    return e

                else:
                    s=dict(response1)
                    s["users"]=record
                    return s

            elif distflag==1:
                    e=dict(response)
                    e["error_Message"]="No Records Found because of Incorrect Place"
                    e["error_Code"]="113"
                    return e


        else:

            cur.execute("SELECT id,seeking,city,country from Users WHERE user_Flag=1 AND id=" + str(args['login_id']))
            con.commit()
            b = cur.fetchall()

            if len(b) == 0:
                e=dict(response)
                e["error_Message"]="User Does Not Exist"
                e["error_Code"]="101"
                return e

            else:

                favourites=self.getfavourite(args)
                
                print favourites
     
                if b[0]['seeking']=='B':
                    #p="SELECT id,coolname,city,country,last_Login,pic,birthday As age,picUrls,shout from Users WHERE id !='"+b[0]['id']+"' AND id NOT IN"+favourites
                    cur.execute("SELECT id,coolname,city,country,last_Login,pic,gender,birthday As age,picUrls,shout from Users"+
                                " WHERE id !='"+b[0]['id']+"' AND id NOT IN "+favourites +"AND user_Flag=1")
                    con.commit()
                else:
                    cur.execute("SELECT id,coolname,city,country,last_Login,pic,gender,birthday As age,picUrls,shout from Users"+
                                " WHERE id !='"+b[0]['id']+"' AND id NOT IN"+favourites +" AND gender='"+b[0]['seeking']+"' AND user_Flag=1")
                    con.commit()
                a = cur.fetchall()

                distflag=0
                
                       
                maps1="http://nominatim.openstreetmap.org/search?q="
                maps2="&format=json"

                cur.execute("SELECT latitude,longitude from Distance1 WHERE city='"+b[0]['city']+"' AND country='"+b[0]['country']+"'")
                con.commit()
                c=cur.fetchall()


                if len(c)<1:
                    aa=requests.get(maps1+b[0]['city']+","+b[0]['country']+maps2).text
                    lat1=aa.find('"lat"')

                    if lat1==-1:
                        e=dict(response)
                        e["error_Message"]="No Records Found because of Incorrect Place"
                        e["error_Code"]="113"
                        return e

                    lat2=aa.find('"',lat1+7)
                    latitude=aa[lat1+7:lat2]

                    long1=aa.find('"lon"',lat2)
                    long2=aa.find('"',long1+7)
                    longitude=aa[long1+7:long2]

                    ab = "INSERT INTO Distance1 (city,country,latitude,longitude) VALUES ( '" + \
                     b[0]['city'] + "' , '" + b[0]['country'] + "' , '" + latitude + "' ,'" + \
                     longitude + "' )"
                    cur.execute(ab)
                    con.commit()

                    args['latitude']=latitude
                    args['longitude']=longitude


                else:
                    args['latitude']=c[0]['latitude']
                    args['longitude']=c[0]['longitude']

                
                dist=self.rgeocode(a,distflag,args)


                if distflag==0:
                    ids=[]
                    distances=[]

                    for v in sorted(dist.items(),key=lambda x: x[1]):
                        ids.append(v[0])
                        distances.append(v[1])

                    record=[]

                    for i in range(len(ids)):
                        for j in range(len(a)):
                            if a[j]['id']==ids[i]:
                                record.append(a[j])

                    if len(record)<1:
                        e=dict(response)
                        e["error_Message"]="No Records Found"
                        e["error_Code"]="113"
                        return e

                    for i in range(len(record)):
                        record[i]['age']=str(datetime.date.today().year-int(record[i]['age'].split('/')[2]))

                    flag=0

                    if len(record)-1<int(args['skip']):
                        flag=1

                    elif int(args['skip'])+int(args['limit'])>=len(record):
                        record=record[int(args['skip']):len(record) ]


                    elif int(args['skip'])+int(args['limit'])<len(record):
                        record=record[int(args['skip']):int(args['skip'])+int(args['limit'])]


                    if flag==1:
                        e=dict(response)
                        e["error_Message"]="No More Records"
                        e["error_Code"]="115"
                        return e

                    else:
                        s=dict(response1)
                        s["users"]=record
                        return s

                elif distflag==1:
                    e=dict(response)
                    e["error_Message"]="No Records Found because of Incorrect Place"
                    e["error_Code"]="113"
                    return e


    def getfavourite(self,args):                                                       #Exclude favourites from get_user

        cur.execute("SELECT user_Favourites from Users WHERE user_Flag=1 AND id='" + str(args['login_id'])+"'")
        con.commit()
        d = cur.fetchall()
        favourites=""
        if len(d)!=0:
            f=d[0]['user_Favourites'].split('#')
            favourites="( "
            for i in range(len(f)-1):
                favourites=favourites+"'"+f[i]+"',"
            favourites=favourites+"'"+f[len(f)-1]+"' )"
        return favourites


    def rgeocode(self,a,distflag,args):                                            #Find latitude,longitude if not in db

        #maps1="http://maps.googleapis.com/maps/api/geocode/json?address="
        #maps2="+CA&sensor=true"

        maps1="http://nominatim.openstreetmap.org/search?q="
        maps2="&format=json"


        dist={}


        for i in range(len(a)):
            cur.execute("SELECT latitude,longitude from Distance1 WHERE city='"+a[i]['city']+"' AND country='"+a[i]['country']+"'")
            con.commit()
            c=cur.fetchall()


            if len(c)<1:
                aa=requests.get(maps1+a[i]['city']+","+a[i]['country']+maps2).text
                lat1=aa.find('"lat"')

                if lat1==-1:
                    distflag==1
                    break

                lat2=aa.find('"',lat1+7)
                latitude=aa[lat1+7:lat2]

                long1=aa.find('"lon"',lat2)
                long2=aa.find('"',long1+7)
                longitude=aa[long1+7:long2]

                ab = "INSERT INTO Distance1 (city,country,latitude,longitude) VALUES ( '" + \
                     a[i]['city'] + "' , '" + a[i]['country'] + "' , '" + latitude + "' ,'" + \
                     longitude + "' )"
                cur.execute(ab)
                con.commit()


            else:
                latitude=float(c[0]['latitude'])
                longitude=float(c[0]['longitude'])


            distances=self.calculate(float(latitude),float(longitude),float(args['latitude']),float(args['longitude']))
            dist[a[i]['id']]=distances

        return dist


    def calculate(self,lat1,long1,lat2,long2):                        #To calculate distance between 2 points (lat,long)
        lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
        R=6371
        lat=lat2-lat1
        long = long2-long1
        a = sin(lat/2)**2 + cos(lat1) * cos(lat2) * sin(long/2)**2
        c= 2 * atan2(sqrt(a), sqrt(1-a))
        d = R*c
        return d


########################################################################################################################

class Get_Favourite_User(restful.Resource):

    def get(self):

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()

        args = fuser.parse_args()

        if len(args['login_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Login Id"
            e["error_Code"]="102"
            return e

        elif 0 in [len(args['skip']),len(args['limit'])] or int(args['skip'])<0 or int(args['limit'])<=0:
            e=dict(response)
            e["error_Message"]="Skip/Limit error"
            e["error_Code"]="111"
            return e

        else:
            cur.execute("SELECT id from Users WHERE user_Flag=1 AND id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()

            if len(a)==0:
                e=dict(response)
                e["error_Message"]="User Does Not Exist"
                e["error_Code"]="101"
                return e

            cur.execute("SELECT user_Favourites from Users WHERE user_Flag=1 AND id='" + str(args['login_id'])+"'")
            con.commit()
            a = cur.fetchall()

            if a[0]['user_Favourites']=="NULL":
                e=dict(response)
                e["error_Message"]="No Favourites"
                e["error_Code"]="106"
                return e

            elif len(a)!=0:
                f=a[0]['user_Favourites'].split('#')
                favourite="( "
                for i in range(len(f)-1):
                    favourite=favourite+"'"+f[i]+"',"
                favourite=favourite+"'"+f[len(f)-1]+"' )"
                cur.execute("SELECT id,coolname,city,country,last_Login,pic,birthday As age,shout from Users WHERE user_Flag=1 AND id IN"+favourite)
                con.commit()
                a=cur.fetchall()

                flag=0
                
                for i in range(len(a)):
                        a[i]['age']=str(datetime.date.today().year-int(a[i]['age'].split('/')[2]))


                if len(a)-1<int(args['skip']):
                    flag=1

                elif int(args['skip'])+int(args['limit'])>=len(a):
                    a=a[int(args['skip']):len(a) ]

                elif int(args['skip'])+int(args['limit'])<len(a):
                    a=a[int(args['skip']):int(args['skip'])+int(args['limit'])]


                if flag==1:
                    e=dict(response)
                    e["error_Message"]="No More Records"
                    e["error_Code"]="115"
                    return e

                else:
                    s=dict(response1)
                    s["favourites"]=a
                    return s

########################################################################################################################

class Get_User_Profile(restful.Resource):

    def get(self):


        global con
        global cur

                                                    #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()

        args = puser.parse_args()

        if len(args['login_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Id"
            e["error_Code"]="102"
            return e

        else:
            cur.execute("SELECT id from Users WHERE user_Flag=1 AND id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()

            if len(a)==0:
                e=dict(response)
                e["error_Message"]="User Does Not Exist"
                e["error_Code"]="101"
                return e

            else:
                percentage,compare_results,a=self.getcompareresult(args)

                badges=a[0]['user_Badges'].split("#")
                movies=a[0]['user_Movies'].split("#")
                musics=a[0]['user_Music'].split("#")
                tvs=a[0]['user_TV'].split("#")

                b,c,d,e=self.getrecords(badges,movies,musics,tvs)

                cur.execute("SELECT id,coolname,city,country,last_Login,pic,birthday As age ,shout,gender,picUrls from Users WHERE user_Flag=1 AND id='"
                        + str(args['login_id'])+"'")
                con.commit()
                a = cur.fetchall()

                a[0]['user_Badges']=b
                a[0]['user_Movies']=c
                a[0]['user_Music']=d
                a[0]['user_TV']=e
                a[0]['comparison']=percentage
                a[0]['compare_Results']=compare_results

                for i in range(len(a)):
                        a[i]['age']=str(datetime.date.today().year-int(a[i]['age'].split('/')[2]))


                aa = "INSERT INTO Activity (from_Id,to_id,activity_Type,activity_Timestamp) VALUES (" + \
                        str(args['current_id']) + " , " + str(args['login_id']) + " , '" + "4" + "' ,'" + \
                         str(datetime.datetime.now()) + "' )"
                cur.execute(aa)
                con.commit()

                cur.execute("SELECT pic,coolname from Users WHERE user_Flag=1 AND id='" + str(args['current_id']) + "'")
                con.commit()
                y = cur.fetchall()

                send_gcm_notification('4',args['current_id'],'NULL',y[0]['coolname'],y[0]['pic'],args['login_id'],str(datetime.datetime.now()))



                s=dict(response1)
                s["profile"]=a
                return s


    def getcompareresult(self,args):                                                 #Get comparison results b/w 2 users


        cur.execute("SELECT user_Answers from Users WHERE  user_Flag=1 AND id='"+ str(args['current_id'])+"'")
        con.commit()
        a = cur.fetchall()
        y=a[0]['user_Answers']

        cur.execute("SELECT id,birthday As age,user_Badges,user_Movies,user_Music,user_TV,user_Answers from Users WHERE user_Flag=1 AND id='"
                          + str(args['login_id'])+"'")
        con.commit()
        a = cur.fetchall()

        a[0]['age']=str(datetime.date.today().year-int(a[0]['age'].split('/')[2]))
        x=a[0]['user_Answers']

        count=0

        compare_results=""

        if len(x)==1:
            if x[0]==y[0] and x[0]!="#":
                compare_results=compare_results+"T"
                count=count+1
            elif x[0]!="#":
                compare_results.append("F")
        else:
            for i in range(len(x)-1):
                if x[i]==y[i] and x[i]!="#":
                    compare_results=compare_results+"T#"
                    count=count+1
                elif x[i]!="#":
                    compare_results=compare_results+"F#"
            if x[len(x)-1]==y[len(y)-1]:
                compare_results=compare_results+"T"
                count=count+1
            else:
                compare_results=compare_results+"F"

        percentage=count*10
        return percentage,compare_results,a



    def getrecords(self,badges,movies,musics,tvs):                     #To get records of user's badges ,movies,music,tv

        badge= "( "
        for i in range(len(badges)-1):
            badge=badge+"'"+badges[i]+"',"
        badge=badge+"'"+badges[len(badges)-1]+"' )"
        print badge
        cur.execute("SELECT badge_id from Badges WHERE badge_Id IN"+badge)
        con.commit()
        bb=cur.fetchall()


        b=""
        if len(bb)==1:
            b=b+bb[0]['badge_id']
        else:
            for i in range(len(bb)-1):
                b=b+bb[i]['badge_id']+"#"
            b=b+bb[len(bb)-1]['badge_id']                                                                    #For Badges

        movie="( "
        for i in range(len(movies)-1):
            movie=movie+"'"+movies[i]+"',"
        movie=movie+"'"+movies[len(movies)-1]+"' )"
        cur.execute("SELECT movie_id from Movies WHERE movie_Id IN"+movie)
        con.commit()
        cc=cur.fetchall()

        c=""
        if len(cc)==1:
            c=c+cc[0]['movie_id']
        else:
            for i in range(len(cc)-1):
                c=c+cc[i]['movie_id']+"#"
            c=c+cc[len(cc)-1]['movie_id']                                                                    #For Movies


        music="( "
        for i in range(len(musics)-1):
            music=music+"'"+musics[i]+"',"
        music=music+"'"+musics[len(musics)-1]+"' )"
        cur.execute("SELECT music_id from Music WHERE music_Id IN"+music)
        con.commit()
        dd=cur.fetchall()

        d=""
        if len(dd)==1:
            d=d+dd[0]['music_id']

        else:
            for i in range(len(dd)-1):
                d=d+dd[i]['music_id']+"#"
            d=d+dd[len(dd)-1]['music_id']                                                                     #For Music


        tv="( "
        for i in range(len(tvs)-1):
            tv=tv+"'"+tvs[i]+"',"
        tv=tv+"'"+tvs[len(tvs)-1]+"' )"
        cur.execute("SELECT tv_id from TV WHERE tv_Id IN"+tv)
        con.commit()
        ee=cur.fetchall()

        e=""
        if len(ee)==1:
            e=e+ee[0]['tv_id']

        else:
            for i in range(len(ee)-1):
                e=e+ee[i]['tv_id']+"#"
            e=e+ee[len(ee)-1]['tv_id']                                                                    #For TV Series


        return  b,c,d,e


########################################################################################################################

class Get_Current_User(restful.Resource):

    def get(self):

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = cuser.parse_args()

        if len(args['login_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Id"
            e["error_Code"]="102"
            return e

        else:
            cur.execute("SELECT id from Users WHERE user_Flag=1 AND id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()

            if len(a)==0:
                e=dict(response)
                e["error_Message"]="User Does Not Exist"
                e["error_Code"]="101"
                return e

            else:
                cur.execute("SELECT id,coolname,password,birthday,gender,seeking,city,country,"
                +"pic,last_Login,shout,user_Favourites,user_TV,user_Movies,user_Music,"
                +"user_Badges,user_Answers,picUrls from Users WHERE user_Flag=1 AND id=" + str(args['login_id']))
                a = cur.fetchall()
                con.commit()
                s=dict(response1)
                s["details"]=a
                return s


########################################################################################################################

class Update_Notifications(restful.Resource):

    def post(self):

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = nuser.parse_args()

        if 0 in [len(args['from_id']),len(args['to_id'])] or args['from_id']==args['to_id']:
            e=dict(response)
            e["error_Message"]="Invalid Id/Ids"
            e["error_Code"]="109"
            return e

        else:
            cur.execute("SELECT id,pic,coolname from Users WHERE user_Flag=1 AND id='" + str(args['from_id']) + "'")
            con.commit()
            y = cur.fetchall()

            cur.execute("SELECT id from Users WHERE user_Flag=1 AND id='"+ str(args['to_id'])+"'")
            con.commit()
            z = cur.fetchall()

            if len(y)<1 or len(z)<1:
                e=dict(response)
                e["error_Message"]="User/Users Does Not Exist"
                e["error_Code"]="108"
                return e

            else:
                if args['type'] in ['1' ,'2' ,'3','6' ]:

                    a = "INSERT INTO Activity (from_Id,to_id,activity_Type,activity_Timestamp) VALUES (" + \
                        str(args['from_id']) + " , " + str(args['to_id']) + " , '" + str(args['type']) + "' ,'" + \
                        str(datetime.datetime.now()) + "' )"
                    cur.execute(a)
                    con.commit()

                    send_gcm_notification(args['type'],y[0]['id'],'NULL',y[0]['coolname'],y[0]['pic'],args['to_id'],str(datetime.datetime.now()))

                    if args['type']=='3' or args['type']=='6':

                        favourite,uflag=self.updatefavourite(args)

                        if uflag==1:
                            e=dict(response)
                            e["error_Message"]="Notification Unsuccessful"
                            e["error_Code"]="114"
                            return e

                        cur.execute("UPDATE Users SET user_Favourites='"+favourite+"' WHERE id='"+str(args['from_id'])+"'")
                        con.commit()

                    return response1


                else:
                    e=dict(response)
                    e["error_Message"]="Invalid Type"
                    e["error_Code"]="112"
                    return e

    def updatefavourite(self,args):                                                          #Adding/Deleting favourites
        cur.execute("SELECT id,user_Favourites from Users WHERE user_Flag=1 AND id='"+str(args['from_id'])+"'")
        con.commit()
        a=cur.fetchall()

        uflag=0

        if args['type']=='3':
            if a[0]['user_Favourites']!="NULL":
                favourites=a[0]['user_Favourites'].split('#')
            else:
                favourites=[]
            favourites.append(str(args['to_id']))
            favourites=list(set(favourites))

        if args['type']=='6':

            if a[0]['user_Favourites']!="NULL":
                favourites=a[0]['user_Favourites'].split('#')
                favourites.remove(str(args['to_id']))
            else:
                favourites=""
                uflag=1


        favourite=""

        if len(favourites)<1:
            favourite=favourite+"NULL"

        elif len(favourites)==1:
            favourite=favourite+favourites[0]
        else:
            for i in range(len(favourites)-1):
                favourite=favourite+favourites[i]+"#"
            favourite=favourite+favourites[len(favourites)-1]

        return favourite,uflag

########################################################################################################################

class Play(restful.Resource):

    def get(self):

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = pluser.parse_args()

        if 0 in [len(args['skip']),len(args['limit'])] or args['skip']<0 or args['limit']<=0:
            e=dict(response)
            e["error_Message"]="Skip/Limit error"
            e["error_Code"]="111"
            return e

        elif len(args['seeking'])==0 or  args['seeking'] not in ['M' ,'F' ,'B' ]:
            e=dict(response)
            e["error_Message"]="Invalid Seek"
            e["error_Code"]="107"
            return e

        else:
             if args['seeking'] == 'B':
                 cur.execute("SELECT id,coolname ,city ,country ,birthday AS age,pic _id from Users WHERE user_Flag=1")
                 con.commit()
             if args['seeking'] == 'M':
                 cur.execute("SELECT id,coolname ,city ,country ,birthday AS age,pic from Users WHERE user_Flag=1 AND seeking='M'")
                 con.commit()
             if args['seeking'] == 'F':
                 cur.execute("SELECT id,coolname ,city ,country ,birthday As age,pic from Users WHERE user_Flag=1 AND seeking='F'")
                 con.commit()
             a = cur.fetchall()
             for i in range(len(a)):
                     a[i]['age']=str(datetime.date.today().year-int(a[i]['age'].split('/')[2]))

             flag=0
             if len(a)-1<int(args['skip']):
                 flag=1
             elif int(args['skip'])+int(args['limit'])>=len(a):
                 a=a[int(args['skip']):len(a) ]
             elif int(args['skip'])+int(args['limit'])<len(a):
                 a=a[int(args['skip']):int(args['skip'])+int(args['limit'])]


             if flag==1:
                 e=dict(response)
                 e["error_Message"]="Skip/Limit error"
                 e["error_Code"]="111"
                 return e

             else:
                 s=dict(response1)
                 s["profiles"]=a
                 print s
                 return s

########################################################################################################################

class Rate_Picture(restful.Resource):

    def post(self):

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()



        args = rauser.parse_args()

        if 0 in [len(args['from_id']),len(args['to_id'])]  or args['from_id']==args['to_id'] :
            e=dict(response)
            e["error_Message"]="Invalid Id/Ids"
            e["error_Code"]="109"
            return e

        elif len(args['pic'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Pic"
            e["error_Code"]="110"
            return e

        else:

            cur.execute("SELECT id,pic,coolname from Users WHERE user_Flag=1 AND id='"+ str(args['from_id'])+"'")
            con.commit()
            y = cur.fetchall()

            cur.execute("SELECT id,picUrls from Users WHERE user_Flag=1 AND id='"+ str(args['to_id'])+"'")
            con.commit()
            z = cur.fetchall()


            if len(y)<1 or len(z)<1:
                e=dict(response)
                e["error_Message"]="User/Users Does Not Exist"
                e["error_Code"]="108"
                return e

            elif z[0]['picUrls']=='NULL':
                e=dict(response)
                e["error_Message"]="Invalid Pic"
                e["error_Code"]="110"
                return e



            else:

                pics=z[0]['picUrls'].split("#")

                if args['pic'] not in pics:
                    e=dict(response)
                    e["error_Message"]="Invalid Pic"
                    e["error_Code"]="110"
                    return e

                else:
                    send_gcm_notification('5',args['from_id'],args['pic'],y[0]['coolname'],y[0]['pic'],args['to_id'],str(datetime.datetime.now()))

                    a = "INSERT INTO Play (from_Id,to_id,picUrl,pic_Timestamp) VALUES ( '" +\
                        str(args['from_id']) + "' ,'" + str(args['to_id']) + "' ,'" + str(args['pic']) + " ' ,'"+\
                        str(datetime.datetime.now())+"' ) "
                    cur.execute(a)
                    con.commit()

                    a = "INSERT INTO Activity (from_Id,to_id,activity_Type,activity_Timestamp) VALUES (" + \
                        str(args['from_id']) + " , " + str(args['to_id']) + " , '" + "5" + "' ,'" + \
                         str(datetime.datetime.now()) + "' )"
                    cur.execute(a)
                    con.commit()

                    return response1


########################################################################################################################

class User_Login(restful.Resource):


    def post(self):

        global con
        global cur

                                                    #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()



        args = luser.parse_args()

        if len(args['login_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Id"
            e["error_Code"]="102"
            return e

        else:
            cur.execute("SELECT id,user_Flag from Users WHERE id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()

            if len(a)==0:
                e=dict(response)
                e["error_Message"]="User Does Not Exist"
                e["error_Code"]="101"
                return e

            else:
                cur.execute("UPDATE Users SET last_Login='" + str(datetime.datetime.now())+"' WHERE id='"+
                            args['login_id']+"'")
                con.commit()

                s=dict(response1)
                s["flag"]=a[0]['user_Flag']
                return s


########################################################################################################################

class Get_Data(restful.Resource):

    def get(self):

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()

        dataflag=0
        
        args = duser.parse_args()

        if len(args['type'])==0:
        
            e=dict(response)
            e["error_Message"]="Incorrect Type"
            e["error_Code"]="112"
            return e

        else:
            if args['type']=='BG':
                cur.execute("SELECT badge_id AS id , badge_name AS name , badge_pic AS url from Badges")
                con.commit()
                a=cur.fetchall()
            elif args['type']=='MO':
                cur.execute("SELECT movie_id AS id , movie_name AS name , movie_Coverpic AS url from Movies")
                con.commit()
                a=cur.fetchall()
            elif args['type']=='MU':
                cur.execute("SELECT music_id AS id , music_name AS name , music_Coverpic AS url from Music")
                con.commit()
                a=cur.fetchall()
            elif args['type']=='TV':
                cur.execute("SELECT tv_id AS id , tv_name AS name , tv_Coverpic AS url from TV")
                con.commit()
                a=cur.fetchall()
            else:
                dataflag=1 
                e=dict(response)
                e["error_Message"]="Incorrect Type"
                e["error_Code"]="112"
                return e

            if dataflag==0:
                  s=dict(response1)
                  s["user_data"]=a
                  return s


########################################################################################################################

class Set_GCM(restful.Resource):

    def post(self):

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = gcuser.parse_args()
        if len(args['login_id'])==0:

            e=dict(response)
            e["error_Message"]="Invalid Id"
            e["error_Code"]="102"
            return e

        elif len(args['gcm_registration_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid User Inputs"
            e["error_Code"]="105"
            return e

        else:
            cur.execute("SELECT id from Users WHERE user_Flag=1 AND id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()

            if len(a)==0:
                e=dict(response)
                e["error_Message"]="User Does Not Exist"
                e["error_Code"]="101"
                return e

            else:
                a = "UPDATE Users SET gcm_registration_id='" + str(args['gcm_registration_id']) + "' WHERE id=" + str(args['login_id'])
                cur.execute(a)
                con.commit()
                return response1


########################################################################################################################

class Upload_image(restful.Resource):
    def get(self):
        global imagecount

        global con
        global cur

                                                     #To check if database connection is intact
        con=mdb.connect( host='localhost', user='login',
        passwd='password', db='databasename',
        cursorclass=MySQLdb.cursors.DictCursor)
        cur = con.cursor()


        args = uplimage.parse_args()
        if len(args['login_id'])==0:
            e=dict(response)
            e["error_Message"]="Invalid Id"
            e["error_Code"]="102"
            return e
        elif len(args['base64image'])==0:
            e=dict(response)
            e["error_Message"]="Invalid User Input/Inputs"
            e["error_Code"]="105"
            return e
        else:
            cur.execute("SELECT id from Users WHERE user_Flag=1 AND id=" + str(args['login_id']))
            con.commit()
            a = cur.fetchall()

            if len(a)==0:
                e=dict(response)
                e["error_Message"]="User Does Not Exist"
                e["error_Code"]="101"
                return e

            else:
                imagecount=imagecount+1
                imagename=str(args['login_id'])+str(imagecount)

                image=args['base64image']
                image=base64.b64decode(image)
                f=open("./static/"+imagename,"wb")
                f.write(image)
                f.close()

                pic="URL/"+imagename
                s=dict(response1)
                s["profilepic"]=pic
                return s

########################################################################################################################

api.add_resource(Register_User, '/register_user')
api.add_resource(User_Signup, '/signup')
api.add_resource(Get_User, '/get_user')
api.add_resource(Get_Favourite_User, '/get_favourites')
api.add_resource(Get_User_Profile, '/get_profile')
api.add_resource(Get_Current_User, '/get_current_user')
api.add_resource(Update_Notifications, '/update_notification')
api.add_resource(Rate_Picture, '/rate_picture')
api.add_resource(User_Login,'/login')
api.add_resource(Get_Data,'/get_data')
api.add_resource(Set_GCM , '/set_gcmid')
api.add_resource(Upload_image , '/upload_image')
#***************************************
api.add_resource(Play, '/play_details')
#***************************************


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8030,debug=True)

#######################################################################################################################