import boto3
from datetime import datetime, timedelta
import pytz
import json
import requests
import csv

def get_ip_info(ip, access_token):
    """ Get country, region, and city information for an IP address using ipinfo.io. """
    try:
        response = requests.get(f"https://ipinfo.io/{ip}?token={access_token}")
        if response.status_code == 200:
            data = response.json()
            return data.get('country'), data.get('region'), data.get('city')
        else:
            return "Unknown", "Unknown", "Unknown"
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        return "Unknown", "Unknown", "Unknown"

def list_events_for_user(search_key, search_value, days, region, ipinfo_access_token):
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

    for page in page_iterator:  # Correct usage of page_iterator
        for event in page['Events']:
            total_events += 1
            event_data = json.loads(event.get('CloudTrailEvent', '{}'))
            ip_address = event_data.get('sourceIPAddress')
            event_name = event_data.get('eventName')
            event_time = event.get('EventTime')

            if ip_address:
                if ip_address not in ip_address_stats:
                    ip_address_stats[ip_address] = {
                        'count': 0, 'events': set(),
                        'last_event_time': event_time, 'first_event_time': event_time,
                        'location': get_ip_info(ip_address, ipinfo_access_token)
                    }
                ip_address_stats[ip_address]['count'] += 1
                ip_address_stats[ip_address]['events'].add(event_name)
                if ip_address_stats[ip_address]['last_event_time'] < event_time:
                    ip_address_stats[ip_address]['last_event_time'] = event_time
                if ip_address_stats[ip_address]['first_event_time'] > event_time:
                    ip_address_stats[ip_address]['first_event_time'] = event_time

    return ip_address_stats, total_events

def save_to_csv(ip_address_stats, filename):
    """ Save the IP address statistics to a CSV file. """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['IP Address', 'Country', 'Region', 'City', 'Event Count', 'First Event Time', 'Last Event Time', 'Events']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for ip, stats in ip_address_stats.items():
            writer.writerow({
                'IP Address': ip,
                'Country': stats['location'][0],
                'Region': stats['location'][1],
                'City': stats['location'][2],
                'Event Count': stats['count'],
                'First Event Time': stats['first_event_time'],
                'Last Event Time': stats['last_event_time'],
                'Events': ', '.join(stats['events'])
            })

# User input
search_type = input("Search by 'email' or 'accessKeyId': ").lower()
search_value = input(f"Enter the {search_type}: ")
days = int(input("Enter the number of days to analyze: "))
aws_region = input("Enter the AWS region for the search: ")
ipinfo_access_token = input("Enter your IPInfo access token: ")
output_csv = input("Do you want to save the results to a CSV file? (yes/no): ").lower()

# Determining the search key based on user choice
search_key = 'Username' if search_type == 'email' else 'AccessKeyId'

# Using the function to retrieve the user's events
ip_address_stats, total_events = list_events_for_user(search_key, search_value, days, aws_region, ipinfo_access_token)

# Outputting the results
print(f"Total events analyzed: {total_events}")
if output_csv == 'yes':
    csv_filename = f"cloudtrail_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    save_to_csv(ip_address_stats, csv_filename)
    print(f"Results saved to {csv_filename}")
else:
    for ip_address, stats in ip_address_stats.items():
        country, region, city = stats['location']
        events_list = ', '.join(stats['events'])
        print(f"{ip_address}: Country = {country}, Region = {region}, City = {city}, Events = {events_list}, Count = {stats['count']}, First Event Time = {stats['first_event_time']}, Last Event Time = {stats['last_event_time']}")
