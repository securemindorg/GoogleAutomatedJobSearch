# Google Jobs Search Script

This project provides a Python script to search for job postings using Google's Custom Search JSON API. The results can be filtered and exported to a CSV file for further use.

## Features

- Search for job postings based on a query and location.
- Filter results using parameters such as date.
- Export job details to a CSV file.

## Prerequisites

- Python 3.7 or higher
- A Google Cloud account
- Access to the Google Custom Search JSON API

## Setup Instructions

### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Log in with your Google account if not already logged in.
3. Click the **Select a Project** dropdown in the top navigation bar.
4. Click **New Project** to create a new project.
5. Provide a name for your project (e.g., "Job Search API") and click **Create**.

### Step 2: Enable the Custom Search JSON API
1. Navigate to **APIs & Services > Library** in the Google Cloud Console.
2. Search for **Custom Search JSON API**.
3. Click on the API and click **Enable**.

### Step 3: Create API Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials** and select **API Key**.
3. Copy the generated API key and store it securely.

### Step 4: Set Up a Custom Search Engine (CSE)
1. Go to the [Custom Search Engine Control Panel](https://cse.google.com/cse/).
2. Click **Add** to create a new search engine.
3. Enter a placeholder site to search (e.g., `www.example.com`) and click **Create**.
   - You can later configure the CSE to emphasize job-related domains.
4. After creating the CSE, go to the **Control Panel** for the new engine.
5. Copy the **Search Engine ID (CSE ID)** displayed at the top.

### Step 5: Configure the Script
1. Replace `your_google_api_key` in the script with your Google API key.
2. Replace `your_custom_search_engine_id` with your CSE ID.

## Running the Script

1. Install required dependencies:
   ```bash
   pip install requests
   ```

2. Run the script:
   ```bash
   python google-job-search.py jobtitle 
   ```

3. The script will:
   - Search for job postings.
   - Print job details to the console.
   - Export the results to a CSV file named `jobs.csv`.

## Customization

### Modify Search Parameters
Update the following variables in the script to customize the job search:
- joblocation = "New York, NY"
- daterange = "m1" # month = m, day = d
- googleapikey = "xxxxxxxx" # follow the readme to get this
- googlesearchid = "xxxxxxxxx"

### Change Output File Name
Update the `file_name` parameter in the `export_jobs_to_csv` function to change the name of the output CSV file.

## Example Output

Sample job details printed to the console:
```
Job 1:
Title: Data Scientist
Link: https://example.com/job1
Description: Nov 14, 2024 ...
----------------------------------------
```

## Notes

- Ensure the API key and CSE ID are kept private to avoid unauthorized use.
- The free tier of the Custom Search JSON API allows up to 100 queries per day. Enable billing for increased limits.
- Customize the CSE to emphasize job-related domains (e.g., `linkedin.com`, `indeed.com`).

## License

This project is open-source and available under the MIT License.

