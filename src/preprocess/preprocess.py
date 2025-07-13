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
        save_uri = paths.get_data_raw_path() / max(csvs).replace('raw', 'preprocessed')
        preprocessed.to_csv(save_uri, index=False)
    
    return data_processed


if __name__ == "__main__":

    # get last processed csv and preprocess all csvs after
    last_preprocessed_uri = paths.get_project_root() / 'src' / 'preprocess' / 'last_preprocessed.json'
    last_preprocessed = io_utils.read_json(last_preprocessed_uri)

    if 'reddit' not in last_preprocessed.keys():
        last_preprocessed['reddit'] = ''
    
    csvs = [csv for csv in os.listdir(paths.get_data_raw_path()) if 'reddit_raw' in csv]
    
    if (last_preprocessed['reddit'] != '') and (last_preprocessed['reddit'] in csvs):
        csvs = csvs[csvs.index(last_preprocessed['reddit']) + 1:]

    data_processed = preprocess_reddit_raw(csvs)

    # update last_preprocessed.json
    if data_processed:
        last_preprocessed['reddit'] = max(csvs)
        io_utils.write_json(last_preprocessed, last_preprocessed_uri)
    
