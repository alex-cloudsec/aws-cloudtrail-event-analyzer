import boto3
from datetime import datetime, timedelta
import pytz

def list_events_for_user(email, days, region):
    # Creating a CloudTrail client with specified region
    client = boto3.client('cloudtrail', region_name=region)

    # Calculating the time range for the logs
    end_time = datetime.now(pytz.utc)
    start_time = end_time - timedelta(days=days)

    # Retrieving and filtering CloudTrail events
    response = client.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'Username',
                'AttributeValue': email
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    events = response.get('Events', [])
    event_names = set()

    for event in events:
        event_data = event.get('CloudTrailEvent', '{}')
        event_name = event.get('EventName')
        event_names.add(event_name)

    return event_names

# Getting user input
user_email = input("Enter the user's email: ")
days = int(input("Enter the number of days to analyze: "))
aws_region = input("Enter the AWS region for the search: ")

# Using the function to retrieve the user's events
events = list_events_for_user(user_email, days, aws_region)
for event_name in events:
    print(event_name)
