DIRNAME=lambda-hoo-`date +'%s'`
DIRPATH=/tmp/$DIRNAME
mkdir $DIRPATH
cp -p src/* $DIRPATH
cp -pr venv/lib/python3.6/site-packages/* $DIRPATH
pushd $DIRPATH
zip -r ../$DIRNAME.zip ./*

# [FIXME] parameters
AWSID=0123456789012
ROLENAME=foo-role
REGION=ap-northeast-1
EVENTNAME=foo-event
FUNCTIONNAME=foo-function

# create lambda exec roles
aws iam create-role --role-name $ROLENAME --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

# wait for avoid errors below create-function
sleep 10

# upload to Lambda (only first time)
aws lambda create-function \
    --function-name $FUNCTIONNAME  \
    --region $REGION \
    --zip-file fileb://../$DIRNAME.zip \
    --handler slack-post.handler \
    --runtime python3.6 \
    --timeout 60 \
    --role arn:aws:iam::$AWSID:role/$ROLENAME \
    --memory-size 128

# upload to Lambda (after the 2nd time)
# aws lambda update-function-code \
    #     --function-name $FUNCTIONNAME \
    #     --zip-file fileb://../$DIRNAME.zip \
    #     --publish

# [START] set periodic execution
aws events put-rule \
    --name $EVENTNAME \
    --schedule-expression 'cron(0/5 * * * ? *)'
# --schedule-expression 'cron(55 9 * * ? *)'

aws lambda add-permission \
    --function-name $FUNCTIONNAME \
    --statement-id $EVENTNAME \
    --action 'lambda:InvokeFunction' \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:$REGION:$AWSID:rule/$EVENTNAME

aws events put-targets --rule $EVENTNAME --targets "Id"="1","Arn"="arn:aws:lambda:$REGION:$AWSID:function:$FUNCTIONNAME"
# [END] set periodic execution

pushd
