# AWS CloudTrail Event Analyzer

## Overview
This Python script is designed to analyze AWS CloudTrail logs. It allows users to search for CloudTrail events based on a specific IAM username or Access Key ID. The script provides detailed information about the activities performed from different IP addresses, including the count of events, types of events executed, and the timestamp of the last event for each IP address.

## Features
- **User-Specific Search**: Filter CloudTrail events by IAM username or Access Key ID.
- **Event Analysis**: Get a detailed breakdown of the activities per IP address, including the count of events and the types of events executed.
- **Date Tracking**: Track the timestamp of the last event executed from each IP address.

## Prerequisites
- Python 3.x
- AWS CLI installed and configured with appropriate permissions.
- Boto3 library installed (`pip install boto3`).

## Usage
1. **Set Up**: Ensure AWS CLI is configured with the necessary access rights to interact with CloudTrail logs.
2. **Run the Script**: Execute the script in a Python environment.
3. **User Input**: When prompted, input the search criteria (username or Access Key ID), the specific event name to filter, the number of days to look back, and the AWS region to search in.
4. **View Results**: The script will output a list of IP addresses with details on the count of events, types of events, and the timestamp of the last event.

## Installation
To install the script, clone this repository to your local machine using:
`git clone [repository-url]`

## Configuration
Before running the script, ensure that your AWS CLI is configured with the appropriate credentials. You can configure it using:
`aws configure`

## Using
- Export results to CSV file

![image](https://github.com/alex-cloudsec/aws-cloudtrail-event-analyzer/assets/102820548/d3cc3368-56e1-4ff4-be22-b7063d0cd32f)
![image](https://github.com/alex-cloudsec/aws-cloudtrail-event-analyzer/assets/102820548/1264eb82-ae68-4f8b-a27d-0ac9cd0ffacc)

- Show results in Terminal

![image](https://github.com/alex-cloudsec/aws-cloudtrail-event-analyzer/assets/102820548/a56e0527-cc3b-4622-9c0e-b784bf73e11e)


