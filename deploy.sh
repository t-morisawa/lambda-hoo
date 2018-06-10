DIRNAME=lambda-hoo-`date +'%s'`
DIRPATH=/tmp/$DIRNAME
mkdir $DIRPATH
cp -p *.py $DIRPATH
cp -pr venv/lib/python3.6/site-packages/* $DIRPATH

# ディレクトリへ移動
pushd $DIRPATH
zip -r ../$DIRNAME.zip ./*

# Lambdaにアップロード
# aws lambda create-function \
#     --function-name lambda-hoo  \
#     --region ap-northeast-1 \
#     --zip-file fileb://../$DIRNAME.zip \
#     --handler get_chiebukuro.handler \
#     --runtime python3.6 \
#     --timeout 60 \
#     --role arn:aws:iam::047480778460:role/service-role/lambda-hoo-test \
#     --memory-size 128

# Lambdaにアップロード
aws lambda update-function-code \
    --function-name lambda-hoo \
    --zip-file fileb://../$DIRNAME.zip \
    --publish

aws events put-rule \
    --name lambda-hoo-scheduled \
    --schedule-expression 'cron(0/15 * * * ? *)'

aws events put-targets --rule lambda-hoo-scheduled --targets "Id"="1","Arn"="arn:aws:lambda:ap-northeast-1:047480778460:function:lambda-hoo"

# 元のディレクトリに戻る
pushd
