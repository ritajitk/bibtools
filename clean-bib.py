#!/usr/bin/env python
'''
It creates a fresh bibfile that has only the entries present in the tex file.

It reads all the citekeys from aux_filename, then reads a bib_filename, that
has more entries than the latex file. Then this script creates an output_bib_file, which
has only those citekeys that are present in the paper.
'''
import argparse
import re
import bibtexparser

def extract_citation_keys(filename):
    citation_keys = set()
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('\\citation'):
                # Extract keys from the \citation line
                keys = line.strip().split('{')[1].rstrip('}').split(',')
                citation_keys.update(keys)
    sorted_keys = sorted(citation_keys)
    return sorted_keys

def read_bib_file(bib_filename):
    with open(bib_filename, 'r') as bib_file:
        bib_database = bibtexparser.load(bib_file)
    return {entry['ID']: entry for entry in bib_database.entries}

def write_new_bib_file(citation_keys, bib_entries, output_filename):
    selected_entries = [bib_entries[key] for key in citation_keys if key in bib_entries]
    new_bib_database = bibtexparser.bibdatabase.BibDatabase()
    new_bib_database.entries = selected_entries

    with open(output_filename, 'w') as output_file:
        bibtexparser.dump(new_bib_database, output_file)

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Create a new BibTeX file with entries from the LaTeX file')
    
    # Add arguments
    parser.add_argument('--aux', dest='aux_filename', help='Auxiliary file name (e.g., main.aux)', required=True)
    parser.add_argument('--bib', dest='bib_filename', help='BibTeX file name (e.g., refs.bib)', required=True)
    parser.add_argument('--output', dest='output_bib_filename', help='Output BibTeX file name (e.g., refs1.bib)', required=True)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Extract citation keys from the LaTeX file
    citation_keys = extract_citation_keys(args.aux_filename)
    print("Citation Keys in", args.aux_filename, ":", citation_keys, len(citation_keys))

    # Read entries from the original BibTeX file
    bib_entries = read_bib_file(args.bib_filename)
    print("Total Entries in inputfile (", args.bib_filename, "):", len(bib_entries))

    # Write the required entries to a new BibTeX file
    write_new_bib_file(citation_keys, bib_entries, args.output_bib_filename)
    print(f"New BibTeX file created: {args.output_bib_filename}")
