# Delete the S3 Bucket for the Client
echo "Deleting S3 Bucket Files..."
aws s3api delete-object --bucket tic-tac-client \
    --key ticTacClient.jar 
echo "Deleting S3 Bucket..."
aws s3api delete-bucket --bucket tic-tac-client --region us-east-1

echo "Done."