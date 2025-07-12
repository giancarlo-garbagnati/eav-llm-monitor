import os
from utils import io_utils
from utils import paths
import praw
import pandas as pd
from datetime import datetime

""" Praw resources
https://praw.readthedocs.io/en/stable/index.html
https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html
https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html
"""

# praw setup
reddit_creds_uri = paths.get_project_root() / 'src' / 'utils' / 'reddit_creds.json'
reddit_creds = io_utils.read_json(reddit_creds_uri)
reddit = praw.Reddit(
    client_id = reddit_creds['REDDIT_CLIENT_ID'],
    client_secret = reddit_creds['REDDIT_SECRET'],
    user_agent = reddit_creds['REDDIT_USER_AGENT']
)

data_datetime_fmt = '%Y%m%d_%H%M%S'

def scrape_reddit(subreddits, search_terms, last_update=None, limit=100):
    """Scrapes various subreddits for various terms and returns as a df"""
    if last_update is None:
        last_update = datetime(2005, 6, 23, 0, 0, 0) # beginning of reddit
    
    results = []
    
    for sub in subreddits:
        for term in search_terms:
            print(f'Searching r/{sub} for "{term}"...')
            for post in reddit.subreddit(sub).search(term, sort='new', limit=limit):
                post_timestamp = datetime.fromtimestamp(post.created_utc)
                if post_timestamp > last_update:
                    results.append({
                        'subreddit': sub,
                        'title': post.title,
                        'selftext': post.selftext,
                        'score': post.score,
                        'created_utc': post_timestamp,
                        'url': post.url,
                        'permalink': f"https://www.reddit.com{post.permalink}"
                    })
                    
    return pd.DataFrame(results)

def find_latest_reddit_timestamp():
    """Find the latest timestamp from the reddit raw data files"""
    latest_data_csv = [csv for csv in os.listdir(paths.get_data_raw_path()) if 'reddit' in csv]
    if len(latest_data_csv) == 0:
        return None
    latest_data_csv = max(latest_data_csv)
    datetime_str = latest_data_csv.replace('reddit_raw_','').replace('.csv', '')
    return datetime.strptime(datetime_str, data_datetime_fmt)

if __name__ == "__main__":
    subreddits = ['rivian', 'electricvehicles', 'ElectricCars']
    subreddits += ['CarRepair', 'autorepair', 'MechanicAdvice']
    subreddits += ['DIYAutoRepair', 'AutoMechanics']
    
    search_terms = ['broke down', 'issue', 'charging problem', 'reliability', 'won’t start']
    
    df = scrape_reddit(subreddits, search_terms, last_update = find_latest_reddit_timestamp())
    
    timestamp = datetime.now().strftime(data_datetime_fmt)
    filename = paths.get_data_raw_path() / f'reddit_raw_{timestamp}.csv'
    if len(df) > 0:
        df.to_csv(filename, index=False)
    print('Reddit finished scraping')
    print(f'{timestamp}')
    if len(df) > 0:
        print(f'{len(df)} results, saved as {filename}')
    else:
        print(f'{len(df)} results, not saved')