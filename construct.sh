# This copies a local aws credential file from this directory, such that they 
# can be easily save time on exporting them independently. The credentials file
# is ignored by git, and as such will not be includede in any commits made.
cp credentials ~/.aws/credentials

: '
# Begin setting up S3 Storage of the Client
echo "Creating S3 Bucket..."
aws s3api create-bucket --acl public-read --region us-east-1 --bucket tic-tac-client 
echo "Uploading Client File..."
aws s3api put-object --acl public-read --bucket tic-tac-client \
    --key ticTacClient.jar \
    --body ./client/ticTacClient.jar
'

# Set up a VPC/Subnet for our database & VMs to connect through
# This also establishes the VPC_ID Shell variable
echo "Creating VPC..."
export VPC_ID=`aws ec2 create-vpc --cidr-block 192.168.0.0/16 --region us-east-1 \
    | grep "VpcId" \
    | cut -d "\"" -f 4`
echo "{
    \"VpcId\": \"$VPC_ID\"
}"
echo "Putting VPC_ID in the 'vpc' file..."
echo $VPC_ID > vpc

echo "Done."