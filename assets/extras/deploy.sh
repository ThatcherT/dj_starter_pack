# helper to deploy files to aws
rsync -r --delete --progress -e "ssh -i <PEM_FILE_NAME>" . ec2-user@<ec2-IP_ADDRESS>.us-west-2.compute.amazonaws.com:app
