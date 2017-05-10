from slackclient import SlackClient
from utils import wit_response
from DocumentAPI.handleQuestions import handle_question,handle_greetings
import os
import time
BOT_TOKEN = "xoxb-175784139376-zBIAYRgv7yR4bX3R8Es7UeAz"
CHANNEL_NAME = "general"
EXAMPLE_COMMAND = ""
# instantiate Slack & Twilio clients
slack_client = SlackClient(BOT_TOKEN)
BOT_ID = "U55P243B2"
READ_WEBSOCKET_DELAY = 1
AT_BOT = "<@" + BOT_ID + ">"

def handle_command(command,channel):
    categories = parse_wit(command)
    print categories
    if(categories.has_key('subjectname')):
       msg = handle_question(categories)
    else:
       msg = handle_greetings(categories)

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=msg, as_user=True)

def parse_wit(slack_rtm_output):
    output_list = slack_rtm_output
    print output_list
    return wit_response(output_list)

def parse_slack_output(slack_rtm_output):

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None



if __name__ == "__main__":

    if slack_client.rtm_connect():
        print("StarterBot connected and running!")

        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
         print("Connection failed. Invalid Slack token or bot ID?")



    #         for slack_message in slack_client.rtm_read():
    #             message = slack_message.get("text")
    #             user = slack_message.get("user")
    #             if not message or not user:
    #                 continue
    #             slack_client.rtm_send_message(CHANNEL_NAME, handle_command(message))
    #         #time.sleep(READ_WEBSOCKET_DELAY)
    # else:
    #     print("Connection failed. Invalid Slack token")
