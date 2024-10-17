import gitlab
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
from typing import List

def initialize_gitlab(url: str, token: str) -> gitlab.Gitlab:
    """
    Initialize a GitLab client.

    Args:
        url (str): The GitLab API URL.
        token (str): The personal access token for authentication.

    Returns:
        gitlab.Gitlab: An authenticated GitLab client.
    """
    return gitlab.Gitlab(url, private_token=token)

def fetch_merge_requests(project: gitlab.v4.objects.Project) -> List[gitlab.v4.objects.ProjectMergeRequest]:
    """
    Fetch all merge requests for a given project.

    Args:
        project (gitlab.v4.objects.Project): The GitLab project object.

    Returns:
        List[gitlab.v4.objects.ProjectMergeRequest]: A list of merge request objects.
    """
    return project.mergerequests.list(all=True)

def process_merge_requests(merge_requests: List[gitlab.v4.objects.ProjectMergeRequest]) -> pd.DataFrame:
    """
    Process merge requests and extract creation timestamps.

    Args:
        merge_requests (List[gitlab.v4.objects.ProjectMergeRequest]): A list of merge request objects.

    Returns:
        pd.DataFrame: A DataFrame containing creation timestamps of merge requests.
    """
    timestamps = []
    for mr in merge_requests:
        created_datetime = datetime.strptime(mr.created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamps.append(created_datetime)
    return pd.DataFrame(timestamps, columns=["created_at"])

def prepare_data(df: pd.DataFrame) -> pd.Series:
    """
    Prepare data for plotting by grouping merge requests by day.

    Args:
        df (pd.DataFrame): A DataFrame containing merge request creation timestamps.

    Returns:
        pd.Series: A Series containing the count of merge requests per day.
    """
    df['date'] = df['created_at'].dt.floor('D')
    return df['date'].value_counts().sort_index()

def plot_merge_requests(merge_requests_per_day: pd.Series) -> None:
    """
    Plot the number of merge requests per day.

    Args:
        merge_requests_per_day (pd.Series): A Series containing the count of merge requests per day.
    """
    plt.figure(figsize=(10, 6))
    merge_requests_per_day.plot(kind='bar', color='skyblue')
    plt.title('Merge Requests Per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Merge Requests')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def main(gitlab_url: str, access_token: str, project_id: str) -> None:
    """
    Main function to orchestrate the merge request plotting process.

    Args:
        gitlab_url (str): The GitLab API URL.
        access_token (str): The personal access token for authentication.
        project_id (str): The ID or path of the GitLab project.
    """
    gl = initialize_gitlab(gitlab_url, access_token)
    project = gl.projects.get(project_id)
    merge_requests = fetch_merge_requests(project)
    df = process_merge_requests(merge_requests)
    merge_requests_per_day = prepare_data(df)
    plot_merge_requests(merge_requests_per_day)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot merge requests per day for a GitLab project.")
    parser.add_argument("--url", default="https://gitlab.scitec.com/api/v4", 
                        help="GitLab API URL (default: https://gitlab.scitec.com/api/v4)")
    parser.add_argument("--token", required=True, help="GitLab personal access token")
    parser.add_argument("--project", required=True, help="GitLab project ID or path")
    
    args = parser.parse_args()
    
    main(args.url, args.token, args.project)
