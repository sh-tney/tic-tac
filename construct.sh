# This copies a local aws credential file from this directory, such that they 
# can be easily save time on exporting them independently. The credentials file
# is ignored by git, and as such will not be includede in any commits made.
cp credentials ~/.aws/credentials

echo "Done."