import argparse
import re

def extract_citekeys(bib_filename):
    with open(bib_filename, 'r') as bib_file:
        content = bib_file.read()

    # Regular expression to match citation keys
    pattern = re.compile(r'@.*?\{(.*?),', re.DOTALL)
    citekeys = pattern.findall(content)

    return citekeys

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Extract citation keys from a BibTeX file')
    
    # Add argument for the BibTeX file name
    parser.add_argument('--bib', dest='bib_filename', help='BibTeX file name', required=True)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Extract and print all citation keys
    citekeys = extract_citekeys(args.bib_filename)
    for citekey in citekeys:
        print(citekey)
