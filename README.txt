DATE APP

****************************
Endpoint : /register_user
****************************

Method      : post


Args        : 

              login_id ,
              password,
              gcm_registration_id
              
Description : This endpoint is used to register a particular user and returns true if registration of new user was successful

Success Response  :
 
                  { 
               "success" : True
               "error" : False  
                    }
                    
Error Response  : 
                
                { 
                   "success" :False
                    "error" : True
  
               "error_Message " : "User Already Exist"
               "error_Code "    : "103"

               "error_Message " : "Invalid Id "
               "error_Code "    : "102"

               "error_Message " : "Invalid Inputs"
               "error_Code "    : "105"

            }

****************************
Endpoint : /signup
****************************

Method      : post


Args        :

              login_id  , coolname  ,
              email , birthday  , gender,seeking  , city ,
              country  , pic , shout ,favourites  ,tvseries  , music  , movies  ,
              badges ,answers, picurls

Description : This endpoint is used to enter the user details in the  User database

Success Response  : 

             { 
               "success" : True
               "error" : False
             }

Error Response  :

              {
               "success" :False
               "error" : True
               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "error_Message " : "Invalid Id"
               "error_Code "    : "102"
 
               "error_Message " : "Invalid User Input/Inputs"
               "error_Code "    : "105"
            }

****************************
Endpoint : /get_user
****************************

Method      : get


Args        : 

              login_id,latitude,longitude,skip,limit
Description : This endpoint is used to get nearby , far and more far away users to whom we want to interact based upon skip and limit values


Success Response  : 

             { 
              "success" : True
              "error" : True  
              "error" : False
               "users" :[
                { "id" :
                  "city":
                  "country":
                  "age":
                  "last_Login":
                  "coolname":
                  "pic":
                  "picUrls":
                  "shout":
                 }

               ]
             }

Error Response  : 

              {
               "success" :False
               "error" : True 
               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "errorMessage " : "Invalid Id"
               "error_Code "    : "102"

               "error_Message " : "Invalid Latitude/Longitude"
               "error_Code "    : "104"

               "error_Message"  : "Skip/Limit error"
               "error_Code "    : "111"

               "error_Message"  : "No records found"
               "error_Code "    : "113"

               "error_Message"  : "No more records "
               "error_Code "    : "115"


               }


****************************
Endpoint : /get_favourites
****************************

Method : get


Args   : 

           login_id,skip,limit
Description : This endpoint is used to retreive the users which are marked as favourite by the user


Success
Response  : 

              { "success" : True
               "error" : False
               "favourites" :[
                { "id" :
                  "city":
                  "country":
                  "age":
                  "last_Login":
                  "coolname":
                  "pic":
                  "shout":
                 }
               ]
             }

Error Response  : 

              { 
               "success" :False
               "error" : True 
               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "error_Message " : "Invalid Id"
               "error_Code "    : "102"

               "error_Message " : "No Favourites"
               "error_Code "    : "106"

               "error_Message"  : "Skip/Limit error"
               "error_Code "    : "111"

               "error_Message"  : "No more records "
               "error_Code "    : "115"
              }


****************************
Endpoint :  /get_profile
****************************

Method : get


Args   : 

          login_id,current_id
Description : This endpoint is used to get the information which will get displayed whenever a user visits a user profile. Here a comparison of users answers is done with the visitors answers and a compare-result is generated. Also viewed profile                notification is stored  (4-> Viewed Profile)

Success
Response  :

             { 
               "success" : True
               "error" : False
               "profile":[
                { "id" :
                  "city":
                  "country":
                  "age":
                  "last_Login":
                  "coolname":
                  "pic":
                  "picUrls":
                  "user_Badges":
                  "user_Movies":
                  "user_TV":
                  "user_Music":
                  "comparison":
                  "compare_Results":
                  "shout":
                 }
                ]
 
             }

Error
Response  : 

              { "success" :False
               "error" : True
               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "error_Message " : "Invalid Id"
               "error_Code "    : "102"

             }

****************************
Endpoint : /play_details
****************************

Method : get


Args   : 

           seeking  ('M','F','B' ),skip,limit
Description : This endpoint is used to retreive the users information If user seeks Male , then information of male users will be returned , if female then information of female users are returned and in case of both , male as well as female  information will be returned

Success
Response  : 

            { "success" : True
               "error" : False
               "profiles":
               [
                { "id" :
                  "city":
                  "country":
                  "age":
                  "coolname":
                  "pic":
                }
               ]
             }

Error Response  : 

            { "success" :False
               "error" : True
               "error_Message " : "Invalid Seek"
               "error_Code "    : "107"

               "success" :False
               "error" : True
               "error_Message " : "Skip/Limit error"
               "error_Code "    : "111"


             }

****************************
Endpoint : /rate_picture
****************************

Method: post


Args  : 

          from_id , to_id , pic
Description :  This endpoint is used to rate pictures of other users and store
                the results in the play table. A notification is also sent for photolike
                (5->PhotoLike)


success
Response  : { 
               "success" : True
               "error" : False
            }

error
Response  :  { 
               "success" :False
               "error" : True
               "error_Message " : "User/Users Does Not Exist"
               "error_Code "    : "108"

               "error_Message " : "Invalid Id/Ids"
               "error_Code "    : "109"

               "error_Message " : "Invalid Pic"
               "error_Code "    : "110"

             }

****************************
Endpoint :  /update_notification
****************************

Method  :  post


Args : 

         from_id , to_id ,type  ('1->Adore You' ,'2->Interested In You' ,'3->Favourite', '6->Unfavourite')
Description: This endpoint is used to update notifications


Success Response  :

            { "success" : True
               "error" : False

            }

Error Response  : 

             { "success" :False
               "error" : True
               "error_Message " : "User/Users Does Not Exist"
               "error_Code "    : "108"

               "error_Message " : "Invalid Id/Ids"
               "error_Code "    : "109"

               "error_Message " : "Invalid Type"
               "error_Code "    : "112"

               "error_Message " : "Notification Unsuccessful"
               "error_Code "    : "114"

             }

****************************
Endpoint : /get_current_user
****************************

Method  :  get


Args  :  

        login_id
Description : For a given id ,this endpoint will return all the  information of that particular user


Success
Response  : 

              { "success" : True
               "error" : False
               "details":[

                { "id" :
                  "password":
                  "city":
                  "country":
                  "birthday":
                  "coolname":
                  "gender":
                  "seeking":
                  "pic":
                  "last_Login":
                  "shout":
                  "user_Badges":
                  "user_Movies":
                  "user_TV":
                  "user_Music":
                  "user_Answers
                  "user_Favourites":
                  "picUrls":
                 }

               ]
             }

Error Response  : 

              { "success" :False
               "error" : True
               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "error_Message " : "Invalid Id"
               "error_Code "    : "102"

              }


****************************
Endpoint : /login
****************************

Method : post


Args  :  

          login_id
          
Description : For a given id , it logins into the database

Success
Response  : 

             {  "success" : True
               "error" : False
               "flag":
             }

Error
Response  :  

             { "success" :False
               "error" : True
               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "error_Message " : "Invalid Id"
               "error_Code "    : "102"

             }


****************************
Endpoint :  /get_data
****************************

Method  :  get


Args : 

        type  ('BG->Badges' ,'MO->Movies' ,'MU->Music', 'TV->TV Series')

Description: This endpoint is used to get movie,music,tv and badges data


Success Response  :

           { "success" : True
               "error" : False
               "user_data"  :
                 [
                 { "id":"",
                   "name":"",
                   "url":""
                  }
                 ]
            }

Error Response  : 

             { "success" :False
               "error" : True
               "error_Message " : "Invalid Type"
               "error_Code "    : "112"
              }


****************************
Endpoint :  /set_gcmid
****************************


Method  :  post


Args : 

        login_id , gcm_registration_id

Description  : This endpoint is used to update the gcm id

Success Response  :

             { "success" : True
               "error" : False
             }

Error Response  : 

             { "success" :False
               "error" : True

               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "error_Message " : "Invalid Id "
               "error_Code "    : "102"

               "error_Message " : "Invalid Inputs"
               "error_Code "    : "105"

             }


****************************
Endpoint :  /upload_image
****************************


Method  :  GET


Args :

         login_id , base64image

Description  : This endpoint is used to generate a url for the base64 image

Success Response  :

             { "success" : True
               "error" : False
               "profilepic":
             }

Error Response  : 


             { "success" :False
               "error" : True

               "error_Message " : "User Does Not Exist"
               "error_Code "    : "101"

               "error_Message " : "Invalid Id "
               "error_Code "    : "102"

               "error_Message " : "Invalid Inputs"
               "error_Code "    : "105"

             }
