import boto3
import datetime

DAY = 60

rds_client = boto3.client('rds')

# get all the rds snapshots
rds_snapshots = []
marker = None
while True:
	if not marker: 
		response = rds_client.describe_db_snapshots()
	else:
		response = rds_client.describe_db_snapshots(Marker = marker)
	marker = response.get('Marker')
	snapshots = response.get('DBSnapshots')
	rds_snapshots += snapshots
	if not marker:
		break
		
# delete snapshots that are not ours
counter = 0
for rds_snapshot in rds_snapshots:
	# check if it is lp team snapshot
	dbid = rds_snapshot.get('DBInstanceIdentifier')
	if 'jira' in dbid or 'confluence' in dbid or 'crowd' in dbid:
		continue


	# delete ones that longer than 7 days
	snapshot_time = rds_snapshot.get('SnapshotCreateTime').date()
	current = datetime.datetime.now().date()
	if  (current - snapshot_time).days > DAY:
		try:
			# DELETE
			#print (rds_snapshot)
			rds_client.delete_db_snapshot(DBSnapshotIdentifier = rds_snapshot.get('DBSnapshotIdentifier'))
			counter += 1
		except Exception as e: 
			print (e)
			print ('Failed to delete, Skipped')
			continue

print ('total number snapshots deleted: ' + str(counter))
