from utils import io_utils
from utils import paths
import openai
import numpy as np
import pandas as pd
import os
import json
from tqdm import tqdm
import random

# create OpenAI client
openai_creds_uri = paths.get_project_root() / 'src' / 'utils' / 'openai_creds.json'
openai_creds = io_utils.read_json(openai_creds_uri)
client = openai.OpenAI(api_key = openai_creds['OPENAI_API_KEY'])

def estimate_tokens(s):
    """Estimate number of tokens in a given string (~n chars/token)"""
    # https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
    n = 3.8
    s = str(s)
    replace_chars = ['\n','\t',' ']
    for char in replace_chars:
        s = s.replace(char, '')
    return int(np.ceil(len(s)/n))

def query_openai(query, instructions, temperature=0, model='gpt-4o-mini', top_p=1.0): #'gpt-4.1'
    """Query openai with given parameters, returns the response"""
    
    response = client.responses.create(
        model = 'gpt-4.1',
        input = query,
        instructions = instructions,
        temperature = temperature,
        top_p = top_p
    )
    return response
    
def construct_query_instructions(source='reddit', shot=0):
    """Reads and formats instructions for openai api"""
    instructions_uri = paths.get_project_root() / 'src' / 'llm' / 'instructions.json'
    all_instructions = io_utils.read_json(instructions_uri)
    if source not in all_instructions.keys():
        source = 'reddit'
    instructions_dict = io_utils.read_json(instructions_uri)[source]
    
    # Identity
    instructions = "# Identity\n"
    instructions += instructions_dict['identity']
    instructions += '\n\n'
    
    # Instructions
    instructions += "# Instructions"
    instructions_list = instructions_dict['instructions']
    for instr in instructions_list:
        instructions += f"\n* {instr}"
    
    # Examples
    if shot > 0:
        instructions += "\n\n# Examples"
    examples = instructions_dict['examples']
    if shot > len(examples):
        shot = len(examples)
    for _ in range(shot):
        i = random.choice(range(len(examples)))
        example = examples.pop(i)
        instructions += f"\n\n<user_query> {example['user_query']} </user_query>\n"
        instructions += f"<assistant_response> {example['assistant_response']} </assistant_response>"
        
    return instructions

def collected_preprocessed_batch(source='reddit', batch_size=5):
    """Batch collect preprocessed csvs into one df"""
    
    # get list of csvs to combine and last_processed csv
    csvs = [csv for csv in os.listdir(paths.get_data_raw_path()) if f"{source}_preprocessed" in csv]
    last_processed_uri = paths.get_project_root() / 'src' / 'llm' / 'last_processed.json'
    last_processed = io_utils.read_json(last_processed_uri)

    if (last_processed[source] == '') or (last_processed[source] not in csvs):
        start = 0
    else:
        start = csvs.index(last_processed[source]) + 1
    end = start + batch_size
    if end > len(csvs):
        csvs = csvs[start:]
    else:
        csvs = csvs[start:end]
    
    if len(csvs) == 0:
        return None
     
    # read each csv, combine into one df
    dfs = [
        pd.read_csv(paths.get_data_raw_path() / csv) for csv in csvs
    ]
    combined = pd.concat(dfs).reset_index(drop=True)
    
    # update new list
    last_processed[source] = csvs[-1]
    io_utils.write_json(last_processed, last_processed_uri)
    
    return combined
    
def under_token_limit(s, limit=2048):
    """Returns if the string is under the token limit"""
    if s is None:
        s = ''
    return estimate_tokens(s) <= limit

def process_data(df, filename, prompt_limit=2048):
    """Given a preprocessed df, process each row and save+return it"""
    
    # add new columns
    # existing columns should be ['score', 'created_utc', 'text']
    new_columns = ['processed', 'skipped', 'is_rivian', 'is_issue', 'system', 'severity', 'firsthand']
    for col in new_columns:
        df[col] = pd.Series([np.nan for x in range(len(df.index))])
    df['processed'] = False
    
    # process each row
    for i, row in tqdm(df.iterrows()):
        try:
            # skip if prompt is too large
            if estimate_tokens(df.loc[i, 'text']) > prompt_limit:
                df.loc[i,'processed'] = True
                df.loc[i,'skipped'] = True
                continue

            # query
            instructions = construct_query_instructions()
            query = row.text
            response_string = query_openai(query, instructions)

            # convert string response to dict/json then add answers to dj
            response = json.loads(response_string.output_text)
            df.loc[i,'is_rivian'] = response['is_rivian']
            df.loc[i,'is_issue'] = response['is_issue']
            df.loc[i,'system'] = response['system']
            df.loc[i,'severity'] = response['severity']
            df.loc[i,'firsthand'] = response['firsthand']
            df.loc[i,'skipped'] = False
            df.loc[i,'processed'] = True

        except:
            continue

    # save and return
    df.to_csv(paths.get_data_processed_path() / filename, index=False)
    return df
    

if __name__ == "__main__":
    
    # Batch up some preprocessed files
    source = 'reddit'
    df = collected_preprocessed_batch(source)
    last_processed_uri = paths.get_project_root() / 'src' / 'llm' / 'last_processed.json'
    last_processed = io_utils.read_json(last_processed_uri)[source]
    filename = last_processed.replace('preprocessed', 'processed')
    
    # Then process
    process_data(df, filename)
    