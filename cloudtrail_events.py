import boto3
from datetime import datetime, timedelta
import pytz
import json

def list_events_for_user(search_key, search_value, days, region):
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
                'AttributeKey': search_key,
                'AttributeValue': search_value
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    ip_address_stats = {}
    total_events = 0

    for page in page_iterator:
        for event in page['Events']:
            total_events += 1
            event_data = json.loads(event.get('CloudTrailEvent', '{}'))
            ip_address = event_data.get('sourceIPAddress')
            event_name = event_data.get('eventName')
            event_time = event.get('EventTime')

            if ip_address:
                if ip_address not in ip_address_stats:
                    ip_address_stats[ip_address] = {'count': 0, 'events': set(), 'last_event_time': event_time}
                ip_address_stats[ip_address]['count'] += 1
                ip_address_stats[ip_address]['events'].add(event_name)
                if ip_address_stats[ip_address]['last_event_time'] < event_time:
                    ip_address_stats[ip_address]['last_event_time'] = event_time

    return ip_address_stats, total_events

# Getting user input
search_type = input("Search by 'username' or 'accessKeyId': ").lower()
search_value = input(f"Enter the {search_type}: ")
days = int(input("Enter the number of days to analyze: "))
aws_region = input("Enter the AWS region for the search: ")

# Determining the search key based on user choice
search_key = 'Username' if search_type == 'email' else 'AccessKeyId'

# Using the function to retrieve the user's events
ip_address_stats, total_events = list_events_for_user(search_key, search_value, days, aws_region)

# Sorting the IP addresses by the count of events in descending order
sorted_ip_addresses = sorted(ip_address_stats.items(), key=lambda x: x[1]['count'], reverse=True)

print(f"Total events analyzed: {total_events}")
for ip_address, stats in sorted_ip_addresses:
    events_list = ', '.join(stats['events'])
    print(f"{ip_address}: Count = {stats['count']}, Last Event Time = {stats['last_event_time']}, Events = {events_list}")
