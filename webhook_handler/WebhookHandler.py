from flask import Flask, request
import json
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
CHANNEL_NAME = 'rasp_autopull'

@app.route('/github_webhooks', methods=['POST'])
def webhook_handler():
	print('POST REQUEST RECIEVED')
	r.publish(CHANNEL_NAME, json.dumps(request.get_json(force=True)))
	
        # Send data to github pull service

	return ('', 204) 

if __name__ == "__main__":
	app.run(host="192.168.0.100", port=13507)
