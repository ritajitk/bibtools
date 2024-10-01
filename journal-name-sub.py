#!/usr/bin/env python

'''
This script replaces long journal names present in the bibliography with their short forms.
'''

import argparse
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

# Dictionary mapping long journal names to their short forms
journal_dict = {
    "Physical Review Letters": "Phys. Rev. Lett.",
    "Physical Review B": "Phys. Rev. B",
    "Physical Review A": "Phys. Rev. A",
    "Physical Review X": "Phys. Rev. X",
    "Physical Review Research": "Phys. Rev. Res.",
    "Nano Letters": "Nano Lett.",
    "Nature Communications": "Nat Commun",
    "Nature Reviews Materials": "Nat Rev Mater",
    "Nature Materials": "Nat. Mater.",
    "Nature Nanotechnology": "Nat. Nanotechnol.",
    "Nature Physics": "Nat. Phys.",
    "Proceedings of the National Academy of Sciences": "Proc. Natl. Acad. Sci. U.S.A.",
    "Communications Physics": "Commun Phys",
    "Nature Reviews Physics": "Nat Rev Phys",
    "Reviews of Modern Physics": "Rev. Mod. Phys.",
    "Science Advances": "Sci. Adv.",
    "Scientific Reports": "Sci Rep",
    "Reports on Progress in Physics" : "Rep. Prog. Phys.",
    "Journal of Physics: Condensed Matter" : "J. Phys.: Condens. Matter"
}

def capitalize_title_properly(text):
    small_words = {'of', 'the', 'and', 'in', 'on', 'at', 'by', 'for', 'to', 'with', 'a', 'an'}
    words = text.split()
    capitalized_words = [
        word if (word in small_words and i != 0) else word.capitalize()
        for i, word in enumerate(words)
    ]
    return ' '.join(capitalized_words)

def process_bib_file(input_file, output_file):
    # Read the BibTeX file
    with open(input_file, 'r') as bibtex_file:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    # Iterate over each entry
    for entry in bib_database.entries:
        if 'journal' in entry:
            # Replace journal names with short names if they exist in the dictionary
            long_journal_name = capitalize_title_properly(entry['journal'])
            if long_journal_name in journal_dict:
                entry['journal'] = journal_dict[long_journal_name]

    # Write the updated BibTeX entries to a new file
    writer = BibTexWriter()
    with open(output_file, 'w') as bibtex_file:
        bibtex_file.write(writer.write(bib_database))

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Replace long journal names with short forms in a BibTeX file')
    
    # Add argument for the input BibTeX file name
    parser.add_argument('--input', dest='input_file', help='Input BibTeX file name', required=True)
    
    # Add argument for the output BibTeX file name
    parser.add_argument('--output', dest='output_file', help='Output BibTeX file name', required=True)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process the BibTeX file
    process_bib_file(args.input_file, args.output_file)
