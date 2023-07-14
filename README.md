# Automatic-Remainder-Generation
## Steps To Run

To start using the program, clone the repository 
- Clone the repo
```
git clone https://github.com/aniket-gupta/techcrunch-assignment.git
```
- Go to mini_project/experiments folder
```
cd <path to git repo in your local>/mini_project/experiments
```
- run the following command

```
pip install -r requirements.txt
``` 
If you face any problems in installing pyAudio try this:
```
pip install pipwin
pipwin install pyaudio

```
Run the following command to start the app
```
python main5.py
```
- The app should be runnning at localhost:5882. Try below API
```
  'http://localhost:5882/'
```
- Now the home page will be displayed
- Click on record button to start the server process which starts recording 
- Recorded voice is converted to text from which reminders are generated and added to google calendar
- Check the logs of the flask app 
- Check calendar to verify that the reminders are set.

Set up:
- https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/
- Use the above link to set up connection with google calendar api
