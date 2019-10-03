: '
# Delete the S3 Bucket for the Client 
echo "Deleting S3 Bucket Files..."
aws s3api delete-object --bucket tic-tac-client \
    --key ticTacClient.jar 
echo "Deleting S3 Bucket..."
aws s3api delete-bucket --bucket tic-tac-client --region us-east-1
' 

# Delete the VPC corresponding to the VPC_ID shell variable
echo "Deleting VPC..."
export VPC_ID=`cat vpc`
aws ec2 delete-vpc --region us-east-1 --vpc-id $VPC_ID

echo "Done."