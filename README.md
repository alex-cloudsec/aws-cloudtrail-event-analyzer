# AWS CloudTrail Event Analyzer

## Overview
This Python script is designed to analyze AWS CloudTrail logs, focusing on identifying and analyzing IP addresses associated with user activities. It filters CloudTrail events by username/email or Access Key ID and provides detailed information about IP addresses involved in these events. The script also fetches geolocation data (country, region, city) for each IP address using the ipinfo.io service and offers the option to export the results to a CSV file.

## Features
- Filter CloudTrail events by IAM Username/email or Access Key ID.
- Analyze IP addresses associated with filtered events.
- Fetch geolocation information for each IP address from ipinfo.io.
- Export results to a CSV file.

## Prerequisites
- Python 3.x
- Boto3 library (`pip install boto3`)
- Requests library (`pip install requests`)
- AWS CLI configured with necessary permissions.
- An access token from ipinfo.io.

## Usage
1. **Setup**: Ensure your AWS CLI is properly configured with access to CloudTrail logs.
2. **Running the Script**: Execute the script in a Python environment. You will be prompted to enter:
   - The type of identifier (email or Access Key ID).
   - The value for the identifier.
   - The number of days for which to analyze logs.
   - The AWS region to search.
   - Your ipinfo.io access token.
   - Whether to export the results to a CSV file.
3. **View Results**: The script outputs the IP addresses and associated geolocation information, along with other relevant event details. If chosen, results will be saved in a CSV file.

## Installation
To install the script, clone this repository to your local machine using:
`git clone [repository-url]`

## Dependencies
Install the required dependencies:
`pip install boto3 requests`

## Configuration
1) Before running the script, ensure that your AWS CLI is configured with the appropriate credentials. You can configure it using: `aws configure`
2) Before running the script, ensure your AWS CLI and ipinfo.io token are properly configured.

## Contribution
Contributions are welcome. Please fork the repository and submit a pull request with your enhancements.

## Using
- Export results to CSV file

![image](https://github.com/alex-cloudsec/aws-cloudtrail-event-analyzer/assets/102820548/d3cc3368-56e1-4ff4-be22-b7063d0cd32f)
![image](https://github.com/alex-cloudsec/aws-cloudtrail-event-analyzer/assets/102820548/1264eb82-ae68-4f8b-a27d-0ac9cd0ffacc)

- Show results in Terminal

![image](https://github.com/alex-cloudsec/aws-cloudtrail-event-analyzer/assets/102820548/a56e0527-cc3b-4622-9c0e-b784bf73e11e)


