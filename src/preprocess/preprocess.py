from utils import io_utils
from utils import paths
import pandas as pd
import os


def preprocess_reddit_raw(csvs):
    """Takes a list of reddit_raw csvs, saves preprocessed data, return if successful"""

    preprocessed = None
    data_processed = False
    
    for csv in csvs:
        df = pd.read_csv(paths.get_data_raw_path() / csv)

        # check for empty csvs
        if len(df) == 0:
            continue
        data_processed = True
        
        # drop ['Weekly Roundup']
        df.drop(df[df['title'].apply(lambda s: '[Weekly Roundup]' in s)].index, inplace=True)
        
        # combine subreddit+title+selftext
        df['text'] = df['subreddit'] + '\n' + df['title'] + '\n' + df['selftext']
        
        # drop rows with score < 0
        df.drop(df[df['score']<0].index, inplace=True)
        
        # drop unneeded columns
        df.drop(['subreddit', 'title', 'selftext','url','permalink'], axis=1, inplace=True)

        if preprocessed is None:
            preprocessed = df
        else:
            preprocessed = pd.concat([preprocessed, df])

    if data_processed:
        save_uri = paths.get_data_processed_path() / max(csvs).replace('raw', 'preprocessed')
        preprocessed.to_csv(save_uri, index=False)
    
    return data_processed


if __name__ == "__main__":

    # get last processed csv and preprocess all csvs after
    last_processed_uri = paths.get_project_root() / 'src' / 'preprocess' / 'last_processed.json'
    last_processed = io_utils.read_json(last_processed_uri)

    if 'reddit' not in last_processed.keys():
        last_processed['reddit'] = ''
    
    csvs = [csv for csv in os.listdir(paths.get_data_raw_path()) if 'reddit_raw' in csv]
    
    if (last_processed['reddit'] != '') and (last_processed['reddit'] in csvs):
        csvs = csvs[csvs.index(last_processed['reddit']) + 1:]

    data_processed = preprocess_reddit_raw(csvs)

    # update last_processed.json
    if data_processed:
        last_processed['reddit'] = max(csvs)
        io_utils.write_json(last_processed, last_processed_uri)
    
