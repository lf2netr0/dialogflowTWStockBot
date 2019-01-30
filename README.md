# A practice of ChatBot using Dialogflow for Python3 (Flask)

## Setup Instructions
### Dialogflow Setup
 1. Create an account on Dialogflow
 1. Create a new Dialogflow agent
 1. Restore the `dialogflow.zip` ZIP file in the root of this repo
   1. Go to your agent's settings and then the *Export and Import* tab
   1. Click the *Restore from ZIP* button
   1. Select the `dialogflow.zip` ZIP file in the root of this repo
   1. Type *RESTORE* and and click the *Restore* button


### Fulfillment Setup

#### LocalServer
 1. Run `pip install -r requirements.txt`
 1. Run `gunicorn -b :8080 main:app`
 1. Sign up and Install [Ngrok](https://ngrok.com/download)
 1. Run `./ngrok http localhost:8080`
 1. Set the fulfillment URL in Dialogflow to your Ngrok URL
 1. Go to your [agent's fulfillment page](https://console.dialogflow.com/api-client/#/agent//fulfillment)
 1. Click the switch to enable webhook for your agent
 1. Enter you Ngrok URL and append `/webhook` (e.g. `https://227aab3d.ngrok.io/webhook`) to the URL field
 1. Click *Save* at the bottom of the page



#### CloudServer
 1. Click on the Google Cloud project ID in your agent's setting to open the Google Cloud console
 1. Deploy fulfillment to Cloud Functions
   1. [Download and authenticate the Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-macos)
   1. Enter `gcp_cloudfunction` folder
   1. Run `gcloud functions deploy webhook --entry-point webhook --runtime python37 --trigger-http`, make a note of the service URL, which will be used in the next step
 1. Set the fulfillment URL in Dialogflow to your Cloud Functions URL
   1. Go to your [agent's fulfillment page](https://console.dialogflow.com/api-client/#/agent//fulfillment)
   1. Click the switch to enable webhook for your agent
   1. Enter you App Engine service URL and append `/webhook` (e.g. `https://translate-10929.appspot.com/webhook`) to the URL field
   1. Click *Save* at the bottom of the page
   
   
## Reference
  1. [Dialogflow Fulfillment Translation Sample for Python (Flask)](https://github.com/dialogflow/fulfillment-translate-python)
  1. [twstock](https://github.com/mlouielu/twstock)
