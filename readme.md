# Auto deployment utility for Raspberry

## How it works
WebHookHandler.py runs a flask server on port 13507 that recieves webhooks from github whenever a repo has been pushed to. You need to manually register the webhook on github.
The correct endpoint to send the post request to is
```
http://<your_url_or_ip>:5000/github_webhooks
```
Redis is then used to notify gitpull_service that a new push has been made and that it is time to pull that repository.
gitpull_service checks if the repo is tracked in the file "repos" and if it is, it pulls the repo. Done!

In order for this to work, gpull and gclone are simple wrappers for git pull and git clone.
gpull is just git pull but it accepts an argument that is a path to a repo that is should pull.
gclone clones a repo and adds the repo to "repos" so that it can be tracked by gpull_service.

## Setup
add gclone and gpull to the path, they have no dependencies outside of python3s standard library. Set up a python3 virtual environment from requirements.txt
make sure that a redis-server is running on port 6379, it is preferable is to set it up to run as a service: https://gist.github.com/mkocikowski/aeca878d58d313e902bb
copy webhook_handler.service into /etc/systemd/system/:
```
sudo cp webhook_handler.service /etc/systemd/system
sudo cp gpull_service.service /etc/systemd/system
```
Enable the services
```
sudo systemctl enable webhook_handler.service
sudo systemctl enable gpull_service.service
```
Then start them
```
sudo systemctl start webhook_handler.service
sudo systemctl start gpull_service.service
```

NOTE: In order for this to work, you need to be able to pull from the repos without a login prompt, this can be done with: (https://stackoverflow.com/questions/5343068/is-there-a-way-to-skip-password-typing-when-using-https-on-github)
```
git config --global credential.helper store
```

## Usage
Clone a repo with:
```
gclone -w -s  <service_name.service> -b <branch_name> <clone_url>
```
This will add it to the list of watched repos, the -s flag is used if you want to specify a systemctl service that you wish to RESTART each time you push to the repo, -s is optional. -w is used if you want to add a webhook to the github repository, if this flag is set you will be prompted for your github password when cloning. -b is used to specify a branch that you want to track, defaults to master.
Now you are pretty much ready to go, just push to your repo from anywhere and it will pull to your pi automatically!


## Todo
* Figure out better way to pull repos without password
* Create config file
* Make install bash script
* Add firewall setting for port 5000 to only accept connections from github ip:s

