from pymongo import MongoClient
import re
import json
categories={}
greensheet={}
client = MongoClient('mongodb://spartan:spartan@ds131041.mlab.com:31041/greensheets')
db=client.get_default_database()

#to handle generic questions

def handle_greetings(categories):
    if categories.has_key('bye'):
       return 'See you soon, Have a great day!!'
    elif categories.has_key('greetings'):
       return 'Hello,'+emoji.emojize(':wave:')+'nice to see you!!'
    elif categories.has_key('hru'):
       return 'I am fine!!'+emoji.emojize(':smiley:')
    elif categories.has_key('hrd'):
       return 'I am doing great, thank you!!'+emoji.emojize(':relaxed:')
    elif categories.has_key('thank'):
       return "You are most welcome!!"
    elif categories.has_key('hwyd'):
       return "It's great, Thank you for asking!!"
    elif categories.has_key('name'):
       return "Hai..I am chocolate,"+emoji.emojize(':wink:')  +" what can I do for you."+emoji.emojize(':simple_smile:')
    elif categories.has_key('plans'):
       return "Helping you!!"
    elif categories.has_key('help'):
       l=[]
       l=db.docCollection.distinct('Course')
       return "I can help you with the info you want regarding course.."+str(l[0])

# handle_question method is used to answer the questions from mongo DB based on categories given byt wit.ai

def handle_question(categories):
    try:
        categories.pop('bye',None)
        categories.pop('greetings',None)
        subname=categories['subjectname']
        if subname==None:
            return 'Please Enter the Course Code'
        m = re.search(r"([A-Za-z]+)([0-9]+)", subname.replace(" ", ""))
        subname = m.group(1) + " " + m.group(2)
        del  categories['subjectname']
        regx = re.compile(".*"+re.escape(subname)+".*", re.IGNORECASE)
        greensheet=db.docCollection.find_one({"Course":regx})
        loop_no = 0
        response=''
        if greensheet:
            keyCount = len(categories)
            if keyCount > 1 and categories.has_key('instructor') :
                del categories['instructor']
            for key,value in categories.iteritems():
                key = key.replace('_',' ')
                for k in greensheet:
                  if key.lower()==k.lower():
                    loop_no = 1
                    response += k+" "+greensheet[k]+"\n"
                    break
                if loop_no!=1:
                    for k in greensheet:
                        if re.search(key,k,re.IGNORECASE):
                            loop_no = 2
                            response += k+" "+greensheet[k]+"\n"
                            break
            return response
        else:
            msg = "Iam Sorry!!..I dont have information about this course would you like to upload it's greensheet? Click https://documentapi.herokuapp.com"
            return msg
    except AttributeError:
        return "Please specify correct course code and number"
    except:
        return "try again!!"
    pass