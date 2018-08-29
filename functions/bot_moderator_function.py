import sys
import os
import urllib
import json
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

VERIFICATION_TOKEN = 'MgIF0jmaV53frVWpSnWimIYJ' # Slack verification token
ACCESS_TOKEN = 'xoxp-381284086564-381284086836-382410955590-fa298875bb7d59352086204ec34b066b' # Slack OAuth access token

SUPPORTED_IMAGES = ['image/jpeg', 'image/jpg', 'image/png']

def main(event):
    print('Validating message...')
    print(event)
    if not verify_token(event):  # Ignore event if verification token presented doesn't match
        return

    if event.get('challenge') is not None:  # Respond to Slack event subscription verification challenge
        print('Event with verification challenge- responding accordingly...')
        challenge = event['challenge']
        return {'challenge': challenge}
        
    event_details = event['event']
    channel = event_details['channel']
    
    if contain_image(event):  # Ignore event if Slack message doesn't contain any images
        file_details = event_details['file']
        image_url = file_details['url_private']
            
        file_id = file_details['id']
        
        print('Downloading image...')
        image_bytes = download_image(image_url)
        print('Saving image locally ...')
        with open('./file.jpg', 'wb') as jpgFile:
           jpgFile.write(image_bytes)
            
        print('Checking image for explicit content...' + image_url)
            
        visual_recognition = VisualRecognitionV3(
            '2018-03-19',
            iam_api_key='G7id_UP6ehtq-pPeMvuVxD3eLYEo2Ort3dU5vyxW6Ou3')
        
        with open('./file.jpg', 'rb') as images_file:
            classes = visual_recognition.classify(
                images_file,
                threshold='0.6',
                classifier_ids='default,explicit')
            
        print('image classified for explicit content')
                
        print(json.dumps(classes, indent=2))
        is_explicit = False
            
        for i in classes['images'][0]['classifiers']:
            if i['classifier_id'] == 'explicit':
                print(i['classes'][0]['class'])
                if i['classes'][0]['class'] == 'explicit':
                    is_explicit = True            
        
        if is_explicit:
            print('Image displays explicit content- deleting from Slack Shared Files...')
            delete_image(file_id)
            print('Posting message to channel to notify users of file deletion...')
            post_message(channel,"File removed due to contain explicit content")
            
        return {"payload": "Done"}
        
    message_text = event_details.get('text')
    event_subtype = event_details.get('subtype')
    
    # skip reply messages sent from bot
    if event_subtype=='bot_message':
        return {"payload": "Done"}
    
    if message_text:
        print('Text Message:'+message_text)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            username='5d615c68-44d4-4d4b-9610-8478ed3f8d1f',
            password='e2rdtEpIYvlk',
            version='2018-03-16')

        response = natural_language_understanding.analyze(
        text=message_text,
        features=Features(
                entities=EntitiesOptions(
                emotion=True,
                sentiment=True,
                limit=2),
            keywords=KeywordsOptions(
                emotion=True,
                sentiment=True,
                limit=2))
            )
        
        print('response:'+json.dumps(response, indent=2))
        
        keyword = response.get('keywords')
        #print('keywords:'+keyword)
        
        if keyword:
            print('keywords:'+keyword[0]['text'])
            disgust = response['keywords'][0]['emotion']['disgust']
            anger = response['keywords'][0]['emotion']['anger']
            if disgust>.5 or anger>.5:
                post_message(channel,"please be more polite ...")
    
    return {"payload": "Done"}


def verify_token(event):
    if event['token'] != VERIFICATION_TOKEN:
        print('Presented with invalid token- ignoring message...')
        return False
    return True

def post_message(channel, text):
    url = 'https://slack.com/api/chat.postMessage'
    data = urllib.parse.urlencode(
        (
            ("token", ACCESS_TOKEN),
            ("channel", channel),
            ("text", text)
        )
    )
    data = data.encode("ascii")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    request = urllib.request.Request(url, data, headers)
    urllib.request.urlopen(request)

def contain_image(event):
    event_details = event['event']
    file_subtype = event_details.get('subtype')

    if file_subtype != 'file_share':
        print('Not a file event- ignoring event...')
        return False

    file_details = event_details['file']
    mime_type = file_details['mimetype']
    file_size = file_details['size']
    
    if mime_type not in SUPPORTED_IMAGES:
        print('File is not an image- ignoring event...')
        return False

    return True


def download_image(url):
    request = urllib.request.Request(url, headers={'Authorization': 'Bearer %s' % ACCESS_TOKEN})
    return urllib.request.urlopen(request).read()


def delete_image(file_id):
    url = 'https://slack.com/api/files.delete'
    data = urllib.parse.urlencode(
        (
            ("token", ACCESS_TOKEN),
            ("file", file_id)
        )
    )
    data = data.encode("ascii")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    request = urllib.request.Request(url, data, headers)
    urllib.request.urlopen(request)
