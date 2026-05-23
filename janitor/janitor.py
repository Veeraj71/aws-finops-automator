import boto3
import json
import sys
from datetime import datetime

def get_localstack_ec2_client():
    return boto3.client(
        'ec2',
        region_name='us-east-1',
        aws_access_key_id='mock',
        aws_secret_access_key='mock',
        endpoint_url='http://localhost:4566'
    )

def run_janitor_campaign(dry_run=True):
    ec2 = get_localstack_ec2_client()
    
    # 1. Gather baseline metadata to match the strict assignment schema requirements
    scan_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Static cost optimization constants (Source: AWS EBS gp3 standard regional pricing table)
    # gp3 volumes cost $0.08 per GB-month
    EBS_GP3_PRICE_PER_GB_MONTH = 0.08 
    
    print("🔍 Scanning LocalStack cloud environment for orphaned infrastructure components...")
    
    try:
        response = ec2.describe_volumes()
    except Exception as e:
        print(f"❌ Connection Failed: Is LocalStack running on port 4566? Details: {str(e)}")
        sys.exit(1)
        
    volumes = response.get('Volumes', [])
    findings = []
    total_orphans = 0
    estimated_monthly_waste_usd = 0.0

    for volume in volumes:
        volume_id = volume['VolumeId']
        size = volume['Size']
        state = volume['State']
        attachments = volume.get('Attachments', [])
        
        # Parse tags safely into a dictionary mapping
        volume_tags = {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])}
        
        # Assignment Condition: Flag EBS volumes in "available" state (unattached)
        if len(attachments) == 0 and state == 'available':
            total_orphans += 1
            
            # Calculate resource metrics based on sizing blueprints
            monthly_cost = float(size * EBS_GP3_PRICE_PER_GB_MONTH)
            estimated_monthly_waste_usd += monthly_cost
            
            # Check for the assignment specific baseline exclusion rule: Protected=true
            is_protected = volume_tags.get('Protected', '').lower() == 'true'
            
            finding = {
                "resource_id": volume_id,
                "resource_type": "ebs_volume",
                "reason": "unattached",
                "age_days": 1,  # Mock age parameter for localized validation runs
                "estimated_monthly_cost_usd": monthly_cost,
                "tags": {
                    "Project": volume_tags.get('Project'),
                    "Environment": volume_tags.get('Environment'),
                    "Owner": volume_tags.get('Owner')
                },
                "suggested_action": "delete",
                "safe_to_auto_delete": not is_protected
            }
            findings.append(finding)
            
            print(f"⚠️  FOUND ORPHAN: Volume {volume_id} ({size} GB) is completely unattached.")
            
            if not dry_run:
                if is_protected:
                    print(f"   🛡️  [PROTECTED] Volume {volume_id} carries Protected=true tag. Skipping deletion.")
                else:
                    print(f"   🔥 Activating remediation... Purging volume {volume_id}...")
                    ec2.delete_volume(VolumeId=volume_id)
                    print(f"   ✅ Successfully purged asset: {volume_id}")

    # Compile compilation report document matching Section 4.4 precisely
    report_data = {
        "scan_timestamp": scan_timestamp,
        "account_id": "000000000000",  # Default LocalStack account format ID
        "region": "us-east-1",
        "summary": {
            "ebs_volumes_total": len(volumes),
            "orphaned_ebs_volumes": total_orphans
        },
        "total_orphans": total_orphans,
        "estimated_monthly_waste_usd": float(round(estimated_monthly_waste_usd, 2)),
        "findings": findings
    }

    # Write report out directly into a single report.json document file at workspace root
    with open('report.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    print("\n💾 Asset telemetry report successfully written out to: ./report.json")
    
    # Assignment Rule 4.2: Exit with non-zero status code if orphans are found in dry-run mode
    if dry_run and total_orphans > 0:
        print(f"🚨 Scan completed. Found {total_orphans} compliance issue(s). Exiting with error fallback.")
        sys.exit(1)
    else:
        print("✅ Clean scan run completed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    execute_remediation = False
    if len(sys.argv) > 1 and sys.argv[1] == '--remediate':
        execute_remediation = True
        
    run_janitor_campaign(dry_run=not execute_remediation)