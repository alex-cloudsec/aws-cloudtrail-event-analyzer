import boto3
from datetime import datetime, timedelta
import pytz
import json

def list_ip_addresses_for_event(email, event_name, days, region):
    # Creating a CloudTrail client with specified region
    client = boto3.client('cloudtrail', region_name=region)

    # Calculating the time range for the logs
    end_time = datetime.now(pytz.utc)
    start_time = end_time - timedelta(days=days)

    # Creating a paginator for the lookup_events method
    paginator = client.get_paginator('lookup_events')

    # Retrieving and filtering CloudTrail events using paginator
    page_iterator = paginator.paginate(
        LookupAttributes=[
            {
                'AttributeKey': 'Username',
                'AttributeValue': email
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    ip_address_stats = {}
    total_events = 0

    for page in page_iterator:
        for event in page['Events']:
            event_data = json.loads(event.get('CloudTrailEvent', '{}'))
            if event_data.get('eventName') == event_name:
                total_events += 1
                ip_address = event_data.get('sourceIPAddress')

                if ip_address:
                    ip_address_stats[ip_address] = ip_address_stats.get(ip_address, 0) + 1

    return ip_address_stats, total_events

# Getting user input
user_email = input("Enter the IAM username: ")
event_name = input("Enter the Event Name to filter: ")
days = int(input("Enter the number of days to analyze: "))
aws_region = input("Enter the AWS region for the search: ")

# Using the function to retrieve the IP addresses for the specified event
ip_address_stats, total_events = list_ip_addresses_for_event(user_email, event_name, days, aws_region)

# Sorting the IP addresses by the count of events in descending order
sorted_ip_addresses = sorted(ip_address_stats.items(), key=lambda x: x[1], reverse=True)

print(f"Total events for '{event_name}' analyzed: {total_events}")
for ip_address, count in sorted_ip_addresses:
    print(f"{ip_address}: Count = {count}")
