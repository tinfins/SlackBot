import os
import datetime as dt
import slack
import pendulum

from flask import abort, Flask, jsonify, request

slack_client = slack.WebClient(os.environ['SLACK_BOT_TOKEN'])
app = Flask(__name__)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']
    return is_token_valid and is_team_id_valid

@app.route('/', methods=['POST'])
def muster():
    data = request.form
    user_id = data['user_id']
    t = dt.datetime.timestamp(dt.datetime.now())
    timeStamp = pendulum.from_timestamp(t, 'US/EASTERN').strftime('%H:%M %m-%d-%Y')
    msg = '<@{}> has mustered @ {}'.format(user_id, timeStamp)

    if not is_request_valid(request):
        abort(400)

    slack_client.chat_postMessage(channel="C010HQ608AU", text=msg,)

    slack_client.chat_postMessage(channel='@{}'.format(user_id), text='you have been accounted for',)
    return ""
