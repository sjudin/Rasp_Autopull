import subprocess as sp

data = {
  "name": "web",
  "active": True,
  "events": [
    "push"
  ],
  "config": {
    "url": "http://95.80.44.88:5000/github_webhooks",
    "content_type": "json"
  }
}

print(str(data).replace("'",'"'))

proc = sp.Popen(['curl', '--trace-ascii', '/dev/stdout', '-u', 'sjudin', '-d', '@data.json', '-X', 'POST', 'https://api.github.com/repos/sjudin/test_repo/hooks'])
proc.communicate()
