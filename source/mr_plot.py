import gitlab
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configuration: Replace with your GitLab URL and access token
GITLAB_URL = "https://gitlab.scitec.com"  # Replace with your GitLab instance URL
ACCESS_TOKEN = "your_access_token_here"  # Replace with your GitLab personal access token
PROJECT_ID = "your_project_id_here"  # Replace with the project ID or path

# Initialize GitLab connection
gl = gitlab.Gitlab(GITLAB_URL, private_token=ACCESS_TOKEN)

# Fetch the project
project = gl.projects.get(PROJECT_ID)

# Fetch the merge requests (pagination handles large responses)
merge_requests = project.mergerequests.list(all=True)

# Prepare data for plotting
timestamps = []

for mr in merge_requests:
    created_at = mr.created_at
    # Convert the created_at string to a datetime object
    created_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamps.append(created_datetime)

# Create a DataFrame from the timestamps
df = pd.DataFrame(timestamps, columns=["created_at"])

# Round down each datetime to the nearest 24-hour period
df['date'] = df['created_at'].dt.floor('D')

# Count the number of MRs per day
merge_requests_per_day = df['date'].value_counts().sort_index()

# Plotting
plt.figure(figsize=(10, 6))
merge_requests_per_day.plot(kind='bar', color='skyblue')
plt.title('Merge Requests Per Day')
plt.xlabel('Date')
plt.ylabel('Number of Merge Requests')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Show the plot
plt.show()

