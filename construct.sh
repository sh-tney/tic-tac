# Begin setting up S3 Storage of the Client
echo "Creating S3 Bucket..."
aws s3api create-bucket --acl public-read --bucket tic-tac-client --region us-east-1
echo "Uploading Client File..."
aws s3api put-object --acl public-read --bucket tic-tac-client \
    --key ticTacClient.jar \
    --body ./client/ticTacClient.jar

echo "Done."