# Supported Device
Python 3.6

# how to use
## use in local env
```
pip install bs4
cd src
python slack-post.py
python tweet.py
```

## use in lambda (create: first time)
### 1. fix deploy.sh
fix aws parameters

### 2. fix src/slack-config.json
fill out incoming-webhook url

### 3. use script
```
sh deploy.sh
```

## use in lambda (update: after second time)
comment out "upload to Lambda (after the 2nd time)"
comment in "upload to Lambda (only first time)"
