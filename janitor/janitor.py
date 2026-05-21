import boto3
import json

def get_localstack_ec2_client():
    # We configure boto3 to talk directly to our local container port instead of real AWS!
    return boto3.client(
        'ec2',
        region_name='us-east-1',
        aws_access_key_id='mock',
        aws_secret_access_key='mock',
        endpoint_url='http://localhost:4566'
    )

def audit_ebs_volumes():
    ec2 = get_localstack_ec2_client()
    print("🔍 Scanning local cloud environment for orphaned storage volumes...")
    
    # Fetch all EBS volumes in the system
    response = ec2.describe_volumes()
    volumes = response.get('Volumes', [])
    
    orphaned_count = 0
    
    for volume in volumes:
        volume_id = volume['VolumeId']
        size = volume['Size']
        state = volume['State']
        attachments = volume.get('Attachments', [])
        
        # Look for the required "ManagedBy" tracking tag
        tags = volume.get('Tags', [])
        managed_by = "Unknown"
        for tag in tags:
            if tag['Key'] == 'ManagedBy':
                managed_by = tag['Value']
        
        # Condition: If there are ZERO attachments, it's an orphaned resource!
        if len(attachments) == 0:
            orphaned_count += 1
            print(f"\n⚠️  ALERT: Found Unattached (Orphaned) EBS Volume!")
            print(f"   - Volume ID: {volume_id}")
            print(f"   - Size:      {size} GB")
            print(f"   - State:     {state}")
            print(f"   - ManagedBy: {managed_by}")
            
    if orphaned_count == 0:
        print("✅ Clean sweep! No orphaned volumes detected.")
    else:
        print(f"\nAudit complete. Found {orphaned_count} orphaned volume(s).")

if __name__ == "__main__":
    audit_ebs_volumes()