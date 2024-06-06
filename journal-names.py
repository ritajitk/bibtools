#!/usr/bin/env python

'''
Given a bib_filename this prints all the journals present in the BibTeX file.
This is useful to check if all the journal names are in the same type-setting format.

For example, there can be multiple entries with "Physical Review Letter" and "Phys. Rev. Lett."
Then you can substitute in vim with %s:Physical Review Letter:Phys. Rev. Lett.:g
'''
import argparse
import bibtexparser

def extract_journal_names(bib_filename):
    with open(bib_filename, 'r') as bib_file:
        bib_database = bibtexparser.load(bib_file)

    journals = set()
    for entry in bib_database.entries:
        if 'journal' in entry:
            journals.add(entry['journal'])

    return sorted(journals)

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Print all journal names present in a BibTeX file')
    
    # Add argument for the BibTeX file name
    parser.add_argument('--bib', dest='bib_filename', help='BibTeX file name', required=True)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Extract and sort journal names
    journals = extract_journal_names(args.bib_filename)
    print("Journal Names:")
    for journal in journals:
        print("-", journal)
