
# Create a cognitive moderator chatbot for anger detection, natural language understanding and explicit images removal
In this developer journey, we will create a chatbot using IBM Functions and Watson Services. 
The chatbot flow will be enhanced by using Visual Recognition and Natural Language Understanding to identify and remove explicit images and or detect anger and ugly messages 

When the reader has completed this journey, they will understand how to:

* Create a chatbot that integrates with Slack via IBM Functions
* Use Watson Visual Recognition to detect explicit images (in beta)
* Use Watson Natural Understanding to detect emotions in a conversation
* Identify entities with Watson Natural Language Understanding

![](doc/source/images/architecture.png)

## Flow
TDB

## With Watson

Want to take your Watson app to the next level? Looking to leverage Watson Brand assets? Join the [With Watson](https://www.ibm.com/watson/with-watson) program which provides exclusive brand, marketing, and tech resources to amplify and accelerate your Watson embedded commercial solution.

## Included components

* [IBM Functions](https://console.bluemix.net/openwhisk/): IBM Cloud Functions (based on Apache OpenWhisk) is a Function-as-a-Service (FaaS) platform which executes functions in response to incoming events and costs nothing when not in use.
* [IBM Watson Visual Recognition](https://www.ibm.com/watson/services/visual-recognition/): Quickly and accurately tag, classify and train visual content using machine learning.
* [IBM Watson Natural Language Understanding](https://www.ibm.com/watson/developercloud/natural-language-understanding.html): Analyze text to extract meta-data from content such as concepts, entities, keywords, categories, sentiment, emotion, relations, semantic roles, using natural language understanding.

## Featured technologies

TBD

## Watch the Video

TBD

## Steps

### Configuration steps for the IBM Cloud
Use the ``Deploy to IBM Cloud`` button **OR** create the services and run locally.
...
...

### Configuration steps for the Slack Application

Create the Slack Application
* Create a slack app as described in the following link: https://api.slack.com/slack-apps#creating_apps
* From the tab Basic Information under Settings take note of the "Verification Token" since it will be required later
* Navigate to the OAuth & Permissions tab under Features
* Under the Permissions Scopes section add the following permissions:
  - channels:history
  - chat:write:bot
  - files:read
  - files:write:user
* Click Save Changes
* Click Install App to Team then Authorize 
* Then write down the "OAuth Access Token" as it will be needed later

Update the code with the generated above tokens
* Replace in the IBM Function "ProcessMessage" code the tokens saved above
  - VERIFICATION_TOKEN = # Slack verification token
  - ACCESS_TOKEN =  # Slack OAuth access token
they are needed to allow the interaction with the Slack messages

Retrieve the Action Web API URL
* Go to the IBM Functions APIs section that describes the API that invoke the action: https://console.bluemix.net/openwhisk/apimanagement and copy the route of the IBM Functions Action called "ProcessMessage".

Update the Slack Application with the Action URL
* Return to the Slack app settings page for the Slack app created earlier
* Navigate to the Event Subscriptions tab under Features and enable events
* In the Request URL field enter the Web API IBM Functions copied above
* Click Add Workspace Event and select message.channels
* Click Save Changes
In this way all the messages posted on Slack will be processed by the IBM Function code.
