from Bio import Entrez, Medline
import pandas as pd
from datetime import datetime
import time
import sys
import re
import string
import os

# debug2 = True # Set to True to print debug messages, False to disable

def fetch_records_from_pubmed(query, max, email):
    """
    Query PubMed using E-utilities and fetch the results.

    Parameters:
    - query: The search term or query.
    - max: Maximum number of results to fetch.
    - email: Your email address (to identify yourself to NCBI).

    Returns:
    - A string containing the MEDLINE formatted records.
    """
    Entrez.email = email

    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max, field="title")  # Append &field=title
        record = Entrez.read(handle)
        pmid_list = record["IdList"]

        # Fetch records
        handle = Entrez.efetch(db="pubmed", id=','.join(pmid_list), rettype="medline", retmode="text")
        data = handle.read()
        handle.close()
        return data

    except Exception as e:
        print(f"Error fetching records for query: {query}. Error: {e}")
        return ""


def sanitize_filename(query):
    """
    Generate a sanitized filename based on the prompt by replacing or removing invalid characters and truncating to 20 characters.
    """
    # Create a simple filename with a timestamp and the first few characters of the query
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_query = ''.join(c for c in query if c.isalnum())[:20]  # Keep first 20 alphanumeric characters
    return f"pubmed_data_{sanitized_query}_{timestamp}.txt"


def parse_medline_data(data):
    """
    Parse MEDLINE formatted data to extract desired fields.

    Parameters:
    - data: String containing the MEDLINE formatted records.

    Returns:
    - A pandas DataFrame containing the parsed data.
    """
    data_records = []
    pmids = Medline.parse(data.splitlines())

    for record in pmids:
        authors = record.get('AU', [])
        authors_formatted = "; ".join([f"{a.split(' ')[-1]}, {' '.join(a.split(' ')[:-1])}" for a in authors])

        dic = {
            'PMID': record.get('PMID', ''),
            'Year': record.get('DP', '').split()[0] if 'DP' in record else '',  # Extracting year from date
            'Authors': authors_formatted,
            'Title': record.get('TI', ''),
            'Abstract': record.get('AB', ''),
            'Journal': record.get('TA', ''),
            'Keywords': "; ".join(record.get('OT', [])),
            'Article Type': "; ".join(record.get('PT', [])),
            'Volume': record.get('VI', ''),
            'Issue': record.get('IP', ''),
            'DOI': record.get('LID', '').split()[0] if 'LID' in record and 'doi' in record.get('LID', '').lower() else ''  # Extracting DOI
        }
        data_records.append(dic)

    return pd.DataFrame(data_records)



def pubmedbatchquery(o='./', q=None, e="your_email@example.com", m=5):
    output_directory = o
    queries = q
    
    # If no queries are provided as an argument
    if queries is None:
        # Attempt to get queries from a file provided as a command line argument
        try:
            if len(sys.argv) > 1:
                with open(sys.argv[1], 'r') as f:
                    queries = [line.strip() for line in f]
        except (FileNotFoundError, IndexError):
            # If no valid file is provided or another error occurs, use the interactive input method
            query_input = input("Enter your PubMed search queries (comma-separated): ")
            queries = [q.strip() for q in query_input.split(",")]

    # Check if queries list is empty
    if not queries:
        print("No queries provided. Exiting...")
        return

    all_dataframes = []
    summary_data = []

    for idx, query in enumerate(queries, start=1):

        # set query = adjusted_query if article types include too many editorials, news, or comments
        adjusted_query = query + " NOT Editorial[Publication Type] NOT News[Publication Type] NOT Comment[Publication Type]"


        print("\n----------------------------\n")
        print(f"Fetching records for query: {query}")

        medline_data = fetch_records_from_pubmed(query, m, e)

        # Save raw data for backup with the query as part of the filename
        filename = sanitize_filename(query)
        with open(os.path.join(output_directory, filename), 'w', encoding='utf-8') as f:
            f.write(medline_data)

        # Parse data
        df = parse_medline_data(medline_data)
        df.insert(0, 'Query Number', idx)  # Insert the query number as the first column
        df.insert(1, 'Query', query)  # Insert the query text as the second column
        all_dataframes.append(df)

        # Add data to the summary list
        summary_data.append({
            'Query': query,
            'Filename': filename,
            'Number of Results': len(df)
        })

        # Introduce a delay for rate limiting
        time.sleep(0.5)

    # Combine all dataframes for the master spreadsheet
    final_df = pd.concat(all_dataframes, ignore_index=True)

    # Save master spreadsheet to a timestamped excel file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    master_output_file = os.path.join(output_directory, f'PubMedMasterSpreadsheet_{timestamp}.xlsx')
    try:
        final_df.to_excel(master_output_file, index=False)
        print(f'Master spreadsheet saved as {master_output_file}')
        return master_output_file
    except Exception as e:
        print(f'Failed to save master spreadsheet {master_output_file}. Error: {e}')


    # Save the summary data to a timestamped TSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_output_file = f'Summary_{timestamp}.tsv'
    try:
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(os.path.join(output_directory, summary_output_file), sep='\t', index=False)
        print(f'Summary saved as {summary_output_file}')
    except Exception as e:
        print(f'Failed to save summary {summary_output_file}. Error: {e}')
