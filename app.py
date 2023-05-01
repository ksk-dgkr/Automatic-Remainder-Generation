from rich import print
from assembly import AssemblyAI

API_KEY = 'a8cfbce7f0c445bcb7dc669e69242d5e'

ai1 = AssemblyAI(API_KEY)

# Example 1.1 Uplaod Media File (By URL)
# media_url = 'https://drive.google.com/file/d/1r9sRDiUbWghlWH7cWuVMkB0imb4FnjEI/view?usp=share_link'
# response_upload_by_url = ai1.upload_audio_by_url(media_url)
# print(response_upload_by_url.json())

#Exampel 1.2 Upload Media File (With A Local File)
def toText(audio):
    media_file_path = r'trial.wav'
    response_upload_by_file = ai1.upload_audio_by_file(media_file_path)
    #print(response_upload_by_file.json())
    response_json_output = response_upload_by_file.json()
    transcript_id = response_json_output['id']
    print("transcript_id:", transcript_id)

    #Step 2. Retrieve Job Status

    while (True):
        response_status = ai1.retrieve_transcript(transcript_id)
        if response_status['status'] == "completed":
            print("status:", response_status['status'])
            print("text:", response_status['text'])
            break
    return response_status['text']