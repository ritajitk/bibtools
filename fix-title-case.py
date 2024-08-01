import argparse
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def add_braces_to_title(title):
    # Split the title into words and add braces around each word
    braced_words = ["{" + word + "}" for word in title.split()]
    # Join the words back into a single string
    return " ".join(braced_words)

def process_bib_file(input_file, output_file):
    with open(input_file, 'r') as file:
        bib_database = bibtexparser.load(file)

    for entry in bib_database.entries:
        if 'title' in entry:
            entry['title'] = add_braces_to_title(entry['title'])

    writer = BibTexWriter()
    with open(output_file, 'w') as file:
        bibtexparser.dump(bib_database, file, writer)

def main():
    parser = argparse.ArgumentParser(description='Add braces around each word in the title fields of a .bib file to preserve the exact cases.')
    parser.add_argument('--bib', required=True, help='Path to the input .bib file')
    parser.add_argument('--output', required=True, help='Path to the output .bib file')

    args = parser.parse_args()

    process_bib_file(args.bib, args.output)

if __name__ == '__main__':
    main()
