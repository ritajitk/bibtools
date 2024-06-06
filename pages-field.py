import bibtexparser
import argparse
import requests
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from requests.exceptions import RequestException, JSONDecodeError

def get_article_metadata(doi):
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        
        # Check if the response content is empty
        if not response.content:
            print(f"Empty response content for {doi}")
            return None
        
        # Try to decode the JSON content
        data = response.json()
        return data
    
    except RequestException as e:
        print(f"Request failed: {e} for {doi}")
        return None
    
    except JSONDecodeError as e:
        print(f"Failed to decode JSON: {e} for {doi}")
        return None

def process_bib_file(input_file, output_file):
    # Read the BibTeX file
    with open(input_file, 'r') as bibtex_file:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    # Iterate over each entry
    for entry in bib_database.entries:
        # Skip entries that already have a 'pages' field
        if 'pages' in entry:
            continue
        
        # Process only entries with a 'doi' field 
        if 'doi' in entry:
            doi = entry['doi']
            citekey = entry['ID']
            # If it is arxiv DOI then skip
            if doi.startswith('10.48550'):
                print(f"ArXiv Preprint: {citekey}. Skipping...")
                continue

            # starting with '10.1103' For physical review family of journal
            if entry['doi'].startswith('10.1103'):
                # Extract the last part of the DOI
                last_part = doi.split(".")[-1]
                # Append the page number to the BibTeX entry
                entry['pages'] = last_part.title()

            # For other DOI fetch info from web.
            else:
                pages=None
                metadata = get_article_metadata(doi)
                if metadata:
                    if "article-number" in metadata.keys():
                        pages=metadata["article-number"]
                    elif "page" in metadata.keys():
                        pages=metadata["page"]
                    if pages==None:
                        print(f"Pages field not found for citekey: {citekey}")
                        continue

                    entry['pages'] = pages

                else:
                    print(f"No metadata found for citekey: {citekey}")


    # Write the updated BibTeX entries to a new file
    writer = BibTexWriter()
    with open(output_file, 'w') as bibtex_file:
        bibtex_file.write(writer.write(bib_database))

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Process input and output BibTeX files')
    
    # Add arguments
    parser.add_argument('--input', dest='input_file', help='Input BibTeX file', required=True)
    parser.add_argument('--output', dest='output_file', help='Output BibTeX file', required=True)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process the BibTeX file
    process_bib_file(args.input_file, args.output_file)
