### Automatic-Remainder-Generation
This is an NLP application that records user's conversations and extracts reminders from them which are then automatiaclly added to the user's Google Calendar. Speech-to-Text conversion and Text Summarization techniques are used.
#### Steps To Run

To start using the program, clone the repository 
```
git clone https://github.com/ksk-dgkr/Automatic-Remainder-Generation.git
```
Install necessary requirements
```
pip install -r requirements.txt
``` 
Try this in case of issues with pyAudio installation:
```
pip install pipwin
pipwin install pyaudio
```
Run the following command in command prompt
```
python realtk.py
```
The home page will be displayed.
- Click on 'Record Audio' button to start the server process which starts recording.
- Once conversation ends, click on 'Stop Recording' and then on 'Process'.
- Recorded voice is converted to text from which reminders are extracted.
- Generated reminders are displayed.
- Select required reminders by ticking the checkboxes next to them and select 'OK'.
- Check calendar to verify that the selected reminders are set.

Set up:
- https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/
- Use the above link to set up connection with google calendar api
