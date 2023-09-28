# LitBatch: API-based Literature Searches

## PubMed Batch Search

This tool facilitates batch searches on PubMed, allowing users to input multiple search queries, either interactively or from a file. The results are parsed and saved in an Excel spreadsheet. Additionally, a summary of the search results, including the number of results per query, is saved in a timestamped TSV file.

### Features:

- **Fetch Records from PubMed**: Uses the E-utilities API to fetch records based on the search query.
- **Parse MEDLINE Data**: Extracts desired fields (PMID, Title, Abstract) from the MEDLINE formatted records.
- **Batch Processing**: Supports both interactive input and file input modes for batch processing of multiple queries.
- **Summary Generation**: Creates a timestamped summary TSV containing information about each query, the filename of the corresponding PubMed output data, and the number of results.
- **Master Spreadsheet**: Consolidates all search results into a timestamped master Excel spreadsheet with an additional field for the query text.

### Usage:

1. **Interactive Mode**: Run the script and paste a comma-separated list of queries when prompted:
    ```bash
    python script_name.py
    ```
2. **File Input Mode**: Prepare a file with one query per line and provide it as an argument:
    ```bash
    python script_name.py queries.txt
    ```

### Dependencies:

- Biopython
- pandas

Install these using pip:

```bash
pip install biopython pandas
```

## Note:
Replace the placeholder email address (`your.email@example.com`) in the `fetch_records_from_pubmed` function with your actual email address before running the script.

Also, the tool parameter is a required parameter when making requests to the NCBI E-utilities API. It is used by NCBI to log and track usage for various reasons, such as monitoring server load, ensuring fair usage, or contacting a user if there's an issue.

As NCBI documentation says about the tool parameter:

*Tool name: the name of the software using the e-utilities. This parameter helps NCBI to track usage and ensures that resources are used fairly, so that the system remains responsive to everyone. If you are posting a series of submissions that will run over an extended period of time, it might be useful to include your email address as part of the tool name (e.g., tool="myTool_myAddress@foo.bar"), to simplify the process of contacting you if a problem arises. A value for this parameter is required.*

You can give it a custom name that represents your software or script. However, as the documentation suggests, if you're making many requests, it might be useful to include your email in the tool name for easier communication. But this is not a strict requirement, and the name itself doesn't have to be something that E-utilities inherently understands. It's more for NCBI's internal tracking and potential communication.

## Product Roadmap

The roadmap outlines potential enhancements and features to further improve the utility and capabilities of our PubMed search script. These represent our vision for the future development of the script, providing users with enhanced functionalities and a more streamlined experience.

### Upcoming Features

1. **Enhance Output Formatting**
    - **What:** Allow users to specify their desired output format (e.g., XML, JSON) using the `retmode` parameter.
    - **Benefit:** Provides flexibility in data format, which can be useful depending on the downstream processing or analysis you plan to do.

2. **Date Filters**
    - **What:** Integrate the `datetype`, `reldate`, `mindate`, and `maxdate` parameters to offer users the ability to filter search results based on various date criteria.
    - **Benefit:** Offers refined search results based on specific date ranges or relative dates, allowing for more targeted data retrieval.

### Feedback

If you have suggestions or feature requests, please submit them to our issue tracker.





