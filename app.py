from dotenv import load_dotenv
from email.mime import image
import os, requests, cv2, logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import numpy as np
from colorblind import colorblind
from bs4 import BeautifulSoup 
import matplotlib.pyplot as plt

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Initialize Slack App
load_dotenv()
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)
logging.basicConfig(level=logging.DEBUG)

# Azure Computer Vision for Alt Text Generation
region = os.environ['AZURE_ACCOUNT_REGION']
key = os.environ['AZURE_ACCOUNT_KEY']
credentials = CognitiveServicesCredentials(key)
azure_client = ComputerVisionClient(
    endpoint="https://" + region + ".api.cognitive.microsoft.com/",
    credentials=credentials
)

def get_image_description(azure_client, image_url, max_candidates=1, language="en"):
    analysis = azure_client.describe_image(image_url, max_candidates, language)
    description = analysis.captions[0].text
    confidence = str(round(analysis.captions[0].confidence*100)) + "%"
    return description, confidence

# Default App Settings
SETTINGS = {
    "img_coloring": "Deuteranopia",
    "img_alt_text": "Enabled",
    "img_resize": "100%",
}

# App Home View
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    client.views_publish(
      user_id=event["user"],
      view={
        "type": "home",
        "callback_id": "home_view",
        "blocks": [
          {
            "type": "header",
            "text": {
              "type": "plain_text",
              "text": ":frame_with_picture:  EASY IMAGE VIEW",
              "emoji": True
            }
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "Make images color-blindness friendly with recoloring and automatically generated image alt text. A convenient way to make visuals more accessible for your teammates."
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "🔢 *HOW TO USE*"
            }
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "In any channel, *react with the 🔎 emoji* to a message's image attachment. This app will then respond in thread with the recolored image and generated alt text."
            }
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "⚙️  *SETTINGS*"
            }
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "Configure the app to your vision. For example, you can choose to have this app generate red/green or blue/yellow color-accessible images below."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Edit App Settings",
                  "emoji": True
                },
                "value": "Configure Button",
                "action_id": "settings"
              }
            ]
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "🙋‍♀️ *TRY IT IN ACTION*"
            }
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "You will be sent a direct message from this bot so you can test out the functionality yourself!"
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Let's Test!",
                  "emoji": True
                },
                "value": "Tutorial Button",
                "action_id": "button_click"
              }
            ]
          }
        ]
}
    ) 
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

# Settings Button Click
@app.action("settings")
def open_settings(ack, body, logger):
  ack() 
  try: 
    app.client.views_open(
      trigger_id=body["trigger_id"],
       view = {
            "type": "modal",
            "callback_id": "view-id",
            "title": {
                "type": "plain_text",
                "text": "Settings",
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
            },
            "blocks": [
                {
                  "type": "divider"
                },
                {
                  "type": "input",
                  "element": {
                    "type": "static_select",
                    "placeholder": {
                      "type": "plain_text",
                      "text": SETTINGS["img_coloring"],
                      "emoji": True
                    },
                    "options": [
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "Deuteranopia",
                          "emoji": True
                        },
                        "value": "Deuteranopia"
                      },
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "Protanopia",
                          "emoji": True
                        },
                        "value": "Protanopia"
                      },
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "Tritanopia",
                          "emoji": True
                        },
                        "value": "Tritanopia"
                      }
                    ],
                    "action_id": "static_select-action"
                  },
                  "label": {
                    "type": "plain_text",
                    "text": "Image Coloring",
                    "emoji": True
                  }
                },
                {
                  "type": "input",
                  "element": {
                    "type": "static_select",
                    "placeholder": {
                      "type": "plain_text",
                      "text": SETTINGS["img_alt_text"],
                      "emoji": True
                    },
                    "options": [
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "Enabled",
                          "emoji": True
                        },
                        "value": "value-0"
                      },
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "Disabled",
                          "emoji": True
                        },
                        "value": "value-1"
                      }
                    ],
                    "action_id": "static_select-action"
                  },
                  "label": {
                    "type": "plain_text",
                    "text": "Alt Text Generation",
                    "emoji": True
                  }
                },
                {
                  "type": "input",
                  "element": {
                    "type": "static_select",
                    "placeholder": {
                      "type": "plain_text",
                      "text": SETTINGS["img_resize"],
                      "emoji": True
                    },
                    "options": [
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "100%",
                          "emoji": True
                        },
                        "value": "value-0"
                      },
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "125%",
                          "emoji": True
                        },
                        "value": "value-1"
                      },
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "150%",
                          "emoji": True
                        },
                        "value": "value-2"
                      },
                      {
                        "text": {
                          "type": "plain_text",
                          "text": "200%",
                          "emoji": True
                        },
                        "value": "value-3"
                      }
                    ],
                    "action_id": "static_select-action"
                  },
                  "label": {
                    "type": "plain_text",
                    "text": "Image Resizing",
                    "emoji": True
                  }
                }
              ]
      }
    )
  except Exception as e: 
    logger.error(f"Error openning settings: {e}")

# Update Settings on Modal Submission
@app.view("view-id")
def view_submission(ack, body, logger):
    ack()
    values = body["view"]["state"]["values"]
    keys = list(values.keys())

    SETTINGS["img_coloring"] = values[keys[0]]["static_select-action"]["selected_option"]["text"]["text"]
    SETTINGS["img_alt_text"] = values[keys[1]]["static_select-action"]["selected_option"]["text"]["text"]
    SETTINGS["img_resize"] = values[keys[2]]["static_select-action"]["selected_option"]["text"]["text"]
    logger.info(SETTINGS)

# Test App Button Click
@app.action("button_click")
def handle_button_click(ack, body, logger):
    ack()
    user_id = body["user"]["id"]
    file_name = "./images/heatmap.png"

    try:
      result = app.client.files_upload(
          channels= user_id,
          initial_comment="React to this image with a 🔎, and let's make this image easily readible!",
          file=file_name,
      )

      try: 
        image_file = result["file"]["id"]
        app.client.files_sharedPublicURL(token=os.environ.get("SLACK_USER_TOKEN"), file=image_file)
      except Exception as e: 
        logger.error("Error making image file public: {}".format(e))

    except Exception as e: 
       logger.error(f"Error uploading file: {e}")

# Respond to Reaction Add in Thread
@app.event("reaction_added")
def handle_reaction(body, event, logger):
    try:
      reaction = event["reaction"]
      if reaction == "mag":
          channel_id = event["item"]["channel"]
          ts=event["item"]["ts"]

          try: 
            result = app.client.conversations_history(channel=channel_id, latest=ts, inclusive=True, limit=1)
            message = result["messages"][0]
          except Exception as e: 
            logger.error("Error getting message: {}".format(e))

          if "files" in message: 
            file_type = message["files"][0]["pretty_type"]

            # Check if File is an Image
            if (file_type != "PNG") and (file_type != "JPEG") and (file_type != "JFIF"):
              # Respond if attachment is not a valid image. 
              app.client.chat_postMessage(
                channel = channel_id,
                thread_ts = ts,
                text="❌ Uh oh, that's not a valid file! Your attachment must be a PNG or JPG.")
            else: 

              # Download Image from Slack 
              image_file = message["files"][0]["id"]
              logger.info(image_file)
              try: 
                app.client.files_sharedPublicURL(token=os.environ.get("SLACK_USER_TOKEN"), file=image_file)
              except Exception as e: 
                logger.error("Error getting public file url: {}".format(e))
                pass

              try: 
                permalink_url = message["files"][0]["permalink_public"]
                html_data = requests.get(permalink_url).content
                soup = BeautifulSoup(html_data, "html.parser")
                image_url = soup.find("img")["src"]
                img_data = requests.get(image_url).content
                description, confidence = get_image_description(azure_client, image_url)
                with open('temp.png', 'wb') as handler: handler.write(img_data)
              except Exception as e: 
                app.client.chat_postMessage(
                  channel = channel_id,
                  thread_ts = ts,
                  text="❌ Oh no, an error occurred! Please contact the admin.")
                logger.error("Error getting image from Slack: {}".format(e))
                return 

              # Send Corrected Image
              app.client.chat_postMessage(
                channel = channel_id,
                thread_ts = ts,
                text="✅ Your image is being processed!")
              original_image = cv2.imread('temp.png', cv2.IMREAD_UNCHANGED)
              original_image = original_image[..., ::-1]

              # Perform Color Correction
              corrected_image = colorblind.hsv_color_correct(original_image, colorblind_type=SETTINGS["img_coloring"].lower())
              cv2.imwrite("easy_image_view_conversion.png", corrected_image)

              # Perform Image Resizing
              scale_factor = float(SETTINGS["img_resize"][:-1]) / 100.0
              if scale_factor != 1: 
                unscaled_image = cv2.imread("easy_image_view_conversion.png", cv2.IMREAD_UNCHANGED)
                new_width = round(unscaled_image.shape[1] * scale_factor)
                new_height = round(unscaled_image.shape[0] * scale_factor)
                rescaled_image = cv2.resize(unscaled_image, (new_width, new_height))
                cv2.imwrite("easy_image_view_conversion.png", rescaled_image) 

              try:
                comment = "Here is the converted image! " + SETTINGS["img_coloring"] + "-friendly."
                if SETTINGS["img_alt_text"]=="Enabled": comment += "\n\nAlt Text: " + description + " (" + confidence + " Confidence)."
                app.client.files_upload(
                    channels=channel_id,
                    thread_ts = ts,
                    initial_comment=comment,
                    file="easy_image_view_conversion.png",
                )
              except Exception as e: 
                logger.error(f"Error uploading file to user's DM: {e}")          
          
          else: 
              # Respond if there is no file attached to message. 
              app.client.chat_postMessage(
                channel = channel_id,
                thread_ts = ts,
                text="❓ Hmmm, there's no image attached to this message to be processed!")
    except Exception as e: 
      logger.error(f"Error handling reaction: {e}")

# Start Slack App with Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()