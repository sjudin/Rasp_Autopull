import redis
import subprocess
import json
import pprint 
import time

# This script recieves a webhook signal from a redis channel and 
# pulls new changes if the repository is tracked

# TODO: Move these into config file
CHANNEL_NAME = 'rasp_autopull'
REPOS_PATH = '/home/pi/projects/Rasp_Autopull/'

# Set up redis instance and subscibe to our channel
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe(CHANNEL_NAME)

# Check message, if the repo that comes in is found in repos,
# use gpull with the value at that key in the repos dict
# Run this as a service

# Initial message that we are connected to redis node
print(p.get_message())


while True:
    msg = p.get_message()
    if msg:
        # Get dict of our tracked repos
        tracked_repos = json.loads(open(REPOS_PATH + 'repos').read())

        # Incoming data, since it comes as bytes we need to decode and make it json
        my_json = msg['data'].decode('utf8').replace("'", '"')
        data = json.loads(my_json)

        # pprint.pprint(data)

        # Check if incoming commit is part of a tracked repo
        if data['repository']['name'] in tracked_repos.keys():
            repo = tracked_repos[data['repository']['name']]
            pull_proc = subprocess.Popen(['gpull', repo['path']])

            # If user has related a service to the pull, we restart the service aswell
            if repo['service']:
                pull_proc.wait()
                restart_proc = subprocess.Popen(['sudo', 'systemctl', 'restart', repo['service']]) 
                restart_proc.communicate()
                print('restarted service', repo['service'])

            try:
                outs, errs = pull_proc.communicate(timeout=15)
            except:
                proc.kill()
                outs, errs = pull_proc.communicate()

    # Lets not fry the CPU
    time.sleep(0.1)
