import boto3
from datetime import datetime

def lambda_handler(event, context):
    print("Received event:", event)

    ec2_client = boto3.client('ec2')
    instance_id = event.get('detail', {}).get('instance-id')

    if not instance_id:
        print("No instance ID found in event")
        return

    try:
        # Optional: Add filter to tag only instances with 'kanakamanoj' in Name
        instance_desc = ec2_client.describe_instances(InstanceIds=[instance_id])
        name_tag = next((tag['Value'] for tag in instance_desc['Reservations'][0]['Instances'][0].get('Tags', [])
                         if tag['Key'] == 'Name'), None)

        if name_tag and "kanakamanoj" not in name_tag.lower():
            print(f"Skipping tagging for instance {instance_id} as Name tag doesn't contain 'kanakamanoj'")
            return

        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        ec2_client.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'LaunchDate', 'Value': current_date},
                {'Key': 'Owner', 'Value': 'KanakaManoj'}
            ]
        )
        print(f"Tagged instance {instance_id} successfully.")
    except Exception as e:
        print(f"Error tagging instance: {str(e)}")
