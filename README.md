# autoTagEC2whenStart
# Assignment 5: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## 📌 Objective

Automatically tag newly launched EC2 instances with the current date and a custom owner tag to ensure better resource tracking and management.

---

## 🛠️ Components Used

- **AWS Lambda**
- **Amazon EC2**
- **Amazon CloudWatch Events (EventBridge)**
- **IAM Role with EC2 Permissions**
- **Python (Boto3 SDK)**

---

### 1. **Create IAM Role for Lambda**

- Go to **IAM > Roles > Create Role**
- **Trusted entity**: AWS service → Lambda
- **Policy**: Attach `AmazonEC2FullAccess`
- Name the role: `KanakaManojLambdaEC2TaggingRole`
- ![image](https://github.com/user-attachments/assets/1b11d6e7-09c8-41fb-925a-c9c1a7ff482a)
- ![image](https://github.com/user-attachments/assets/40a9f25d-779d-4172-bda1-d78b54b06008)

- ![image](https://github.com/user-attachments/assets/1ee5d7ee-b67d-4997-9d70-72a003bb5140)




---

### 2. **Create Lambda Function**

- Go to **AWS Lambda > Create function**
- Name: `AutoTagEC2Instances`
- Runtime: `Python 3.x`
- Role: Use existing role → `KanakaManojLambdaEC2TaggerRole`
- ![image](https://github.com/user-attachments/assets/6ed1b000-a38f-4332-8fb1-f2bcf6bd1511)


#### Paste the below Python code:

```python
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
        # Check instance Name tag for 'kanakamanoj'
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
```
### Create event rule 
- Go to **Awa eventbridge > Create event rule**
- Name: `kanakaManoj-Event-rule`
- Go to CloudWatch > Rules > Create Rule
- Event Source:
    - Event pattern
    - Service name: EC2
    - Event type: EC2 Instance State-change Notification
    - Specific state(s): running
    - Targets: Add Lambda function `AutoTagEC2Instances`

Create the rule (enable it)
![image](https://github.com/user-attachments/assets/2b82798c-5602-46f3-9066-16ff2f92bc22)
![image](https://github.com/user-attachments/assets/872b73c8-4264-4305-919c-ed0f1635fa35)
![image](https://github.com/user-attachments/assets/c4c91c3d-ced5-42e2-86c1-5c4ddea2c7ba)
![image](https://github.com/user-attachments/assets/54e46ada-ca53-41e2-b823-d80349c328dd)

![image](https://github.com/user-attachments/assets/e3ddbc0c-49fc-4284-8564-17c6951ecfc7)
![image](https://github.com/user-attachments/assets/8ce96b0a-9ee7-4461-abd2-66b90d5d7371)

## Test
- instance started
- ![image](https://github.com/user-attachments/assets/9becc98e-6ccc-476f-9e91-8395dae5a03e)
![image](https://github.com/user-attachments/assets/5e07b984-e9d1-4abf-b23c-45ec24a3690a)

![image](https://github.com/user-attachments/assets/32e9f6af-14af-4ea7-8752-e71fd409ec23)

