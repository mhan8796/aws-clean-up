import boto3
import datetime

DAY = 60
AWS_ACCOUNT = ['']

ec2 = boto3.resource('ec2')

# get the snapshots for EC2 instance for Jira, Crowd, Confluence
lp_ec2_snaps = {}
instances = ec2.instances.filter(
    Filters=[
	    {'Name': 'tag:Name', 'Values': ['*jira*','*crowd*','*confluence*']}
    ]
)
for instance in instances:
    for vol in instance.volumes.all():
    	for snapshot in vol.snapshots.all():
    		lp_ec2_snaps[snapshot] = True

# get all snapshots and delete the ones not from lp_ec2_snaps
snapshots = ec2.snapshots.filter(OwnerIds=AWS_ACCOUNT)
counter = 0
for snapshot in snapshots:
	if not lp_ec2_snaps.get(snapshot):
		# delete snapshot if it is old than 7 days
		current = datetime.datetime.now().date()
		duration = current - snapshot.start_time.date()
		if duration.days > DAY:
			try:
				# DELETE
				#print (snapshot)
				snapshot.delete()
				counter += 1
			except Exception as e: 
				print (e)
				print ('Failed to delete, Skipped')
				continue


print ('total number snapshots deleted: ' + str(counter))