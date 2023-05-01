import tkinter
import sounddevice as sd
from tkinter import *
import queue
import soundfile as sf
import threading
from tkinter import messagebox

import argparse
import tempfile
import queue
import sys

from cal_setup import get_calendar_service
import datetime as dateTime
from dateutil.parser import parse

import requests
from requests.structures import CaseInsensitiveDict

import random
import datetime as dateTime
from datetime import datetime, timedelta

import speech_recognition as sr
import spacy
nlp = spacy.load('en_core_web_sm')
intvars=[]

top=object()
#Functions to play, stop and record audio in Python voice recorder
#The recording is done as a thread to prevent it being the main process
def add_rem(rem):
    try:
        d = rem[1]
        service = get_calendar_service()
        #d = datetime.now().date()
        tomorrow = datetime(d.year, d.month, d.day, d.hour,d.minute)
        start = tomorrow.isoformat()
        end = (tomorrow + timedelta(hours=1)).isoformat()
        event_result = service.events().insert(calendarId='primary',body={
        "summary": rem[0],
        "description": rem[0],
        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
        }).execute()
        print("created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])
    except Exception as e:
        print("Error in adding to calendar",e)

def open_popup():
    top= Toplevel(voice_rec)
    top.geometry("360x180")
    top.title("Child Window")
    #Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)
    var1 = IntVar()
    Checkbutton(top, text="male", variable=var1).grid(row=0, sticky=W)
    var2 = IntVar()
    Checkbutton(top, text="female", variable=var2).grid(row=1, sticky=W)
    mainloop()



def add_checked_rem(rlist,remlist):
    global intvars
    global top
    #print(intvars,"jhbhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    #print("len  ",len(intvars))
    if len(intvars)>0:
        for i in range(len(intvars)):
            if intvars[i].get()==1:
                print("remkinder to be added","*"*100,remlist[rlist[i]])
                a=remlist[rlist[i]]
                add_date=parse(a, fuzzy_with_tokens=True)
                add_date=add_date[0]
                add_rem([rlist[i],add_date])
                #print(add_rem([rlist[i],add_date]),"nfdjvjfdhvbjhfdbvhjdfbvhfjvbhfbvhjbjvbdfvbhjgfbbvbgfb","****************",rlist[i],a)
                #([rlist[i],remlist[rlist[i]]])#

        print("added reminders","-"*1000)
    top.destroy()
    #return "added"

def processing(mytext):
    if True:
        try:
            if True:
                #request.method=='POST':
                #result = request.form

                #example = result['message']
                
                # example = "Hey Snigdha, how are you? It's been a long time. Yeah I am good. How is everything at your place ? Yeah everything's fine. All of our friends are planning something. Will it be possible for you to attend a get-together on 4 October?. Oh yes. I will definetly come. When does it start? The meet starts at 10 AM. Please come along with your family. Yeah sure. See you there. Alright bye"
                # example = "Hello doctor. Hello. Take a seat. Tell me what your problem is. I have been suffering from fever for the past 2 days. Okay, let me check your temperature. It's 103 degrees. You have high fever. Take this medicine at 2 PM today. If the fever does not subdue, take a corona test tomorrow. Meet me at 3 PM this wednesday."
                sen_doc = nlp(mytext)
                #print("here6 after nlp")
                sentences = list(sen_doc.sents)
                # print(sentences)
                present_perfect=['had been','have been','has been']
                rem_list = {}
                #print("sentences --------------",sentences)
                for sentence in sentences:
                    print("-------------sentence--","*"*50,sentence)
                    pp = False
                    for i in present_perfect:
                        #print(sentence,str(sentence).find(i),i)
                        if str(sentence).find(i)!=-1:
                            pp = True
                            break
                    #print("before dtect past sentence")
                    if pp:
                        continue
                    sent = sentence
                    strue= (sent.root.tag_ == "VBD" or
                            any(w.dep_ == "aux" and w.tag_ == "VBD" for w in sent.root.children))
                    if strue == True :
                        continue
                    #print("after detect")
                    date = False
                    time = False
                    ent1 = ""
                    ent2 = ""
                    list1 = []
                    list2 = []
                    pobj=''
                    notpobj = ['AM','PM','am','pm','January','january','February','february','March','march','April','april','May','may','June','june','July','july','August','august','September','september','October','october','November','november','December','december']
                    words = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
                    #rem = {'appointment': 'Your appointment at', 'meet': 'Your meeting at ', 'meeting': 'Your meeting at',
                    #       'medicine': 'Take medicines at', 'medicines': 'Take medicines at', 'come': 'Your Meeting at','tablet': 'Take medicines at',
                    #       'party' : 'Attend Party at', }
                    rem={}
                    for ent in sentence.ents:

                        #print(ent.text,ent.label_)
                        if ent.label_ == "DATE":
                            date_words = ent.text.split(" ")
                            #print(ent.text)
                            if (ent.text.casefold() == 'today'):
                                list1.append(str(dateTime.date.today()))
                            elif (ent.text .casefold() == 'tomorrow'):
                                list1.append(str(dateTime.date.today() + dateTime.timedelta(days=1)))
                            elif ((date_words[0].casefold() == 'this') and date_words[1] in words):
                                n = int(dateTime.datetime.today().weekday())
                                week=date_words[1]
                                wee=0
                                if (week == 'sunday'):
                                    wee =6
                                elif (week == 'monday'):
                                    wee =0
                                elif (week == 'tuesday'):
                                    wee =1
                                elif (week == 'wednesday'):
                                    wee= 2
                                elif (week == 'thursday'):
                                    wee =3
                                elif (week == 'friday'):
                                    wee= 4
                                elif (week == 'saturday'):
                                    wee= 5



                                #w = int(getweek(date_words[1]))
                                w=wee
                                list1.append(str(dateTime.date.today() + dateTime.timedelta(days=w - n)))
                            elif (date_words[0].casefold() == 'next' and date_words[1] in words):
                                num = 6 - int(dateTime.datetime.today().weekday())

                                week=date_words[1]
                                wee=0
                                if (week == 'sunday'):
                                    wee =6
                                elif (week == 'monday'):
                                    wee =0
                                elif (week == 'tuesday'):
                                    wee =1
                                elif (week == 'wednesday'):
                                    wee= 2
                                elif (week == 'thursday'):
                                    wee =3
                                elif (week == 'friday'):
                                    wee= 4
                                elif (week == 'saturday'):
                                    wee= 5

                                num = num + wee + 1
                                list1.append(str(dateTime.date.today() + dateTime.timedelta(days=num)))
                            elif (date_words[0] in words):
                                n = int(dateTime.datetime.today().weekday())

                                week=date_words[0]
                                wee=0
                                if (week == 'sunday'):
                                    wee =6
                                elif (week == 'monday'):
                                    wee =0
                                elif (week == 'tuesday'):
                                    wee =1
                                elif (week == 'wednesday'):
                                    wee= 2
                                elif (week == 'thursday'):
                                    wee =3
                                elif (week == 'friday'):
                                    wee= 4
                                elif (week == 'saturday'):
                                    wee= 5
                                w = wee
                                list1.append(str(dateTime.date.today() + dateTime.timedelta(days=w - n)))
                            else:
                                list1.append(ent.text)
                            #print(ent.text)
                            ent1 = ent.text
                            date = True
                            print("here some")
                        if ent.label_ == "TIME":
                            list1.append(ent.text)
                            ent2 = ent.text
                            time = True
                    mysample=""
                    if date or time:
                        for token in sentence:
                            if (token.pos_ =="PROPN" or token.pos_ =="VERB" or token.pos_ =="NOUN" ):
                                
                                print("token tezt",token.text)
                                if token.dep_=="pobj":
                                    if token.text=="p.m." or token.text=="PM" or token.text=='P.M.' or token.text=="a.m." or token.text=="AM":
                                        print("token ",'&'*100,token.text)
                                        continue
                                mysample=mysample+" "+token.lemma_
                                print("tpken chars.......",token)
                                print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
                            if token.dep_ == "ROOT" or token.dep_ == 'dobj' or token.dep_ == 'pobj' or token.dep_ == 'compound' or token.dep_ == 'nsubjpass':
                                if (token.dep_=='pobj' or token.dep_ == 'compound') and (token.text not in notpobj):
                                    pobj=pobj+' '+token.text

                                if token.dep_ != 'pobj':
                                    list2.append(token.text)

                                #print(token.text,":",ent1,ent2)
                            #print (token.text, token.tag_, token.head.text, token.dep_)
                    if len(list1) > 0 and len(list2) > 0:
                        key = ' '.join(list2)
                        key1=''
                        flag = False
                        words_in_key = key.split(" ")
                        for word in words_in_key:
                            #print(word)
                            if word.casefold() in rem:
                                flag = True
                                key1 = rem[word.casefold()]#+' '+str(pobj)
                                break
                        value = ' '.join(list1)
                        print("value",value,"value"*50)
                        print("mysample",mysample,"mysample"*50)
                        #print(key1)
                        if flag:
                            #nowdt=datetime.now().strftime('%H:%M:%S')
                            nowdt=str(datetime.now())

                            rem_list[key1] = value
                            #print(str(pobj),"ssssssssssssssssssssssssssssssssssssss")
                        else:
                            #nowdt=datetime.now().strftime('%H:%M:%S')
                            nowdt=str(datetime.now())
                            #rem_list[key] = value
                            rem_list[mysample]=value
                            #print(str(pobj),"gggggggggggggggggggggg")
                    print("rem_list:",rem_list) 
                    r_list={}
                if len(rem_list)>0:
                    global top
                    top= Toplevel(voice_rec)
                    top.geometry("360x180")
                    top.title("Child Window")
                    #Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)
                    global intvars
                    remcount=0
                    for rem in rem_list.keys():
                        a=rem_list[rem]
                        try:
                            add_date=parse(a, fuzzy_with_tokens=True)
                            add_date=add_date[0]
                            intvars.append(IntVar())
                            Checkbutton(top, text=rem + " " + a, variable=intvars[remcount]).grid(row=remcount, sticky=W)
                            r_list[remcount]=rem
                            remcount+=1
                            #print("adding remainder to calendar")
                            #print("reminder",a)
                            #add_rem([rem,add_date])
                            #print("added remainder in calendar")
                        except Exception as e:
                            print("unable to add the generated reminder date {0}".format(str(e)))
                        #ok_btn = Button(top, text="Ok", command=lambda m=3:add_checked_rem())
                        #ok_btn = Button(top, text = 'OK',command = add_checked_rem(r_list,rem_list)).grid(row=remcount+1, sticky=W)
                    ok_btn = Button(top, text = 'OK',command = lambda:add_checked_rem(r_list,rem_list)).grid(row=remcount+1,sticky=W)
                        #play_btn = Button(voice_rec, text="Play Recording", command=lambda:add_checked_rem(r_list,rem_list)).grid(row=remcount+1,sticky)
                        #ok_btn.pack()

                else:
                    open_popup()
                    print(rem_list)
                    print("remlist empty")

        except Exception as e:
            print("Error",e)



def addpunctuation(mytext):
    url = "http://bark.phon.ioc.ee/punctuator"
    #global mytext
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data=f"text={mytext} "

    resp = requests.post(url, headers=headers, data=data)
    #print(resp.text)
    mytext=resp.text
    return mytext

def recognizing_speech(myfile):
    AUDIO_FILE = myfile

    # use the audio file as the audio source

    r = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        #reads the audio file. Here we use record instead of
        #listen*
        print(type(source),"*"*590)
        audio = r.record(source)

    try:
        import app
        #mytext = r.recognize_google(audio)
        mytext = app.toText(audio)
        print("The audio file contains: " + mytext)
        #mytext = addpunctuation(mytext)
        #print("Added punctuation",mytext)
        processing(mytext)

    except sr.UnknownValueError:
        print("AssemblyAI could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from AssemblyAI service; {0}".format(e))

t1=object()
def threading_rec(x):
   global t1
   if x == 1:
       #If recording is selected, then the thread is activated
       t1=threading.Thread(target= record_audio)
       t1.start()
   elif x == 2:
       #To stop, set the flag to false
       global recording
       recording = False
       t1.join()
       #recognizing_speech("trial.wav")
       messagebox.showinfo(message="Recording finished")
   elif x == 3:
       #To play a recording, it must exist.
       if file_exists:
           #Read the recording if it exists and play it
           recognizing_speech("trial.wav")
       else:
           #Display and error if none is found
           messagebox.showerror(message="Record something to process")
#Fit data into queue
def callback(indata, frames, time, status):
   q.put(indata.copy())
#Recording function

def record_audio():
   #Declare global variables   
   global recording
   #Set to True to record
   recording= True  
   global file_exists
   #Create a file to save the audio
   messagebox.showinfo(message="Recording Audio. Speak into the mic")
   with sf.SoundFile("trial.wav", mode='w', samplerate=44100,
                       channels=2) as file:
   #Create an input stream to record audio without a preset time
           with sd.InputStream(samplerate=44100, channels=2, callback=callback):
               while recording == True:
                   #Set the variable to True to allow playing the audio later
                   file_exists =True
                   #write into file
                   file.write(q.get())
#Define the user interface for Voice Recorder using Python
voice_rec = Tk()
voice_rec.geometry("360x200")
voice_rec.title("Voice Recorder")
voice_rec.config(bg="#107dc2")
#Create a queue to contain the audio data
q = queue.Queue()
#Declare variables and initialise them
recording = False
file_exists = False
 #Label to display app title in Python Voice Recorder Project
title_lbl  = Label(voice_rec, text="Voice Recorder", bg="#107dc2",font=20).place(x=120,y=10)
 
#Button to record audio
record_btn = Button(voice_rec, text="Record Audio", command=lambda m=1:threading_rec(m))
#Stop button
stop_btn = Button(voice_rec, text="Stop Recording", command=lambda m=2:threading_rec(m))
#Play button
play_btn = Button(voice_rec, text="Process", command=lambda m=3:threading_rec(m))


#Position buttons
record_btn.place(x=100,y=50)
stop_btn.place(x=200,y=50)
play_btn.place(x=160,y=90)
voice_rec.mainloop()
