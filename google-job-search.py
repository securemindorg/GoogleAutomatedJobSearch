# @author: Josh
# data: 12/11/24
# Usage: python google-job-search.py jobtitle 
# this script once running, continues to run and returns the new results every 24hrs if enabled
# Requirements: requests, json

import requests
import json, re
import sys, csv
import datetime, time

jobtitle = sys.argv[1]
joblocation = "New York, NY"
daterange = "m1" # month = m, day = d
googleapikey = "xxxxxxxxx" # follow the readme to get this
googlesearchid = "xxxxxxxxxxxx" # also follow the readme to get this

def search_google_jobs(api_key, cse_id, query, location=None, filters=None):
    """
    Search for jobs using Google's Custom Search JSON API.

    Parameters:
        api_key (str): Your Google Custom Search API key.
        cse_id (str): The Custom Search Engine ID configured for jobs.
        query (str): The search query (e.g., job title, skills).
        location (str): Optional location to refine the search.
        filters (dict): Additional filters (e.g., company, date).

    Returns:
        list: A list of job details matching the criteria.
    """
    base_url = "https://www.googleapis.com/customsearch/v1"

    # Construct the search query
    search_query = query
    if location:
        search_query += f" in {location}"

    params = {
        "key": api_key,
        "cx": cse_id,
        "q": search_query,
        "gl": "us",  # Target geographic location (e.g., 'us' for United States) must be lowercase
    }

    # Add filters to the query if provided
    if filters:
        for key, value in filters.items():
            params[key] = value

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        jobs = []
        for item in data.get("items", []):
            job = {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            }
            jobs.append(job)
        return jobs
    else:
	# if not status status 200 then throw error
        print(f"Error: {response.status_code} - {response.text}")
        return []

# This function does not work with most sites so ignore it for now
def filter_new_jobs(jobs, last_run_time):
    """
    Filter jobs to return only those posted in the last 24 hours.

    Parameters:
        jobs (list): The list of job details.
        last_run_time (datetime): The timestamp of the last script run.

    Returns:
        list: A filtered list of new jobs.
    """
    new_jobs = []
    for job in jobs:
        snippet = job.get("snippet", "")
        # Debugging: Print the snippet to verify the date format
        print(f"Processing snippet: {snippet}")
        
        # Updated regex pattern for more robust date matching
        date_match = re.search(r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\\s\\d{1,2},\\s\\d{4}", snippet)
        
        if date_match:
            try:
                job_date = datetime.datetime.strptime(date_match.group(), "%b %d, %Y")
                print(f"Matched date: {job_date}")
                if job_date >= last_run_time:
                    new_jobs.append(job)
            except ValueError as e:
                print(f"Date parsing error: {e}")
        else:
            print("No date found in snippet.")

    return new_jobs

def export_jobs_to_csv(jobs, file_name="jobs.csv"):
    """
    Export job details to a CSV file.

    Parameters:
        jobs (list): A list of job details.
        file_name (str): The name of the output CSV file.
    """
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "link", "snippet"])
        writer.writeheader()
        writer.writerows(jobs)
    print(f"Jobs exported to {file_name}")

if __name__ == "__main__":

    API_KEY = googleapikey
    CSE_ID = googlesearchid

    # Define the job search parameters
    search_query = jobtitle
    job_location = joblocation
    additional_filters = {
        "dateRestrict": daterange,  # Jobs posted within the last month
    }

    # Keep track of the last run time
    last_run_time = datetime.datetime.now() - datetime.timedelta(days=1)

    while True:
        print("Running job search...")

        # Search for jobs
        jobs = search_google_jobs(API_KEY, CSE_ID, search_query, job_location, additional_filters)
        print(jobs)

        # Filter for new jobs only
        #new_jobs = filter_new_jobs(jobs, last_run_time)

        # Update the last run time
        last_run_time = datetime.datetime.now()

        # Print the new job details
        #if new_jobs:
        #    for idx, job in enumerate(new_jobs, start=1):
        #        print(f"Job {idx}:")
        #        print(f"Title: {job['title']}")
        #        print(f"Link: {job['link']}")
        #        print(f"Description: {job['snippet']}")
        #        print("-" * 40)
        #else:
        #    print("No new jobs found.")

        # Wait for 24 hours before running again
        #time.sleep(86400)

        for idx, job in enumerate(jobs, start=1):
            print(f"Job {idx}:")
            print(f"Title: {job['title']}")
            print(f"Link: {job['link']}")
            print(f"Description: {job['snippet']}")
            print("-" * 40)

        # Export the jobs to a CSV file
        export_jobs_to_csv(jobs)


