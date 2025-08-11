#!/usr/bin/env python3
"""
BibTeX Duplicate Finder & Deduplicator
"""

import argparse
import bibtexparser
from collections import defaultdict
import re
import sys

USAGE_MESSAGE = """
BibTeX Duplicate Finder & Deduplicator
--------------------------------------

This tool helps you find and resolve duplicate entries in a .bib file.
It can also scan your LaTeX source files to see which duplicates are actually used.

USAGE:
    Show duplicates in a .bib file:
        python dedup.py --bib myrefs.bib --show

    Show only duplicates that are actually cited in LaTeX:
        python dedup.py --bib myrefs.bib --show --tex main.tex appendix.tex

    Interactively deduplicate (choose which key to keep):
        python dedup.py --bib myrefs.bib --deduplicate

    Interactively deduplicate only used keys:
        python dedup.py --bib myrefs.bib --deduplicate --tex main.tex

AFTER DEDUPLICATION:
    - Creates deduplicated.bib with only kept entries
    - Creates replace_keys.sed to update citation keys in .tex files

APPLYING THE SED SCRIPT:
    # Test changes without modifying files:
    sed -f replace_keys.sed main.tex

    # Apply changes to a file:
    sed -i -f replace_keys.sed main.tex

    # Apply changes to all .tex files in current dir:
    sed -i -f replace_keys.sed *.tex

    # Apply changes recursively to all .tex files:
    find . -name "*.tex" -exec sed -i -f replace_keys.sed {} +

REQUIREMENTS:
    pip install bibtexparser
"""

def entry_signature(entry):
    """Return a normalized tuple for detecting duplicates."""
    title = re.sub(r'\W+', '', entry.get("title", "").lower())
    author = re.sub(r'\W+', '', entry.get("author", "").lower())
    year = entry.get("year", "").strip()
    return (title, author, year)

def find_duplicates(entries):
    """Return a dict mapping signature -> list of entries."""
    groups = defaultdict(list)
    for e in entries:
        groups[entry_signature(e)].append(e)
    return {sig: grp for sig, grp in groups.items() if len(grp) > 1}

def extract_used_keys(tex_files):
    """Return a set of citation keys used in the given .tex files."""
    cite_pattern = re.compile(r'\\cite[t|p]?\{([^}]*)\}')
    used_keys = set()
    for tex_file in tex_files:
        with open(tex_file, encoding="utf-8") as f:
            content = f.read()
            for match in cite_pattern.findall(content):
                keys = [k.strip() for k in match.split(',')]
                used_keys.update(keys)
    return used_keys

def show_duplicates(duplicates, used_keys=None):
    """Print duplicate groups, optionally filtered by used keys."""
    if not duplicates:
        print("No duplicates found.")
        return
    print(f"Found {len(duplicates)} possible duplicate groups:\n")
    for sig, entries in duplicates.items():
        if used_keys and not any(e["ID"] in used_keys for e in entries):
            continue
        first_entry = entries[0]
        print(f"--- Duplicate group ---")
        print(f"Title : {first_entry.get('title', '')}")
        print(f"Author: {first_entry.get('author', '')}")
        print(f"Year  : {first_entry.get('year', '')}")
        for e in entries:
            mark = " (USED)" if used_keys and e["ID"] in used_keys else ""
            print(f"Key: {e.get('ID','')} | DOI: {e.get('doi','N/A')} | Year: {e.get('year','N/A')}{mark}")
        print()

def interactive_deduplicate(duplicates, used_keys=None):
    """Interactive deduplication session."""
    kept_entries = []
    replacements = []
    for sig, entries in duplicates.items():
        if used_keys and not any(e["ID"] in used_keys for e in entries):
            kept_entries.extend(entries)
            continue

        first_entry = entries[0]
        print(f"--- Duplicate group ---")
        print(f"Title : {first_entry.get('title', '')}")
        print(f"Author: {first_entry.get('author', '')}")
        print(f"Year  : {first_entry.get('year', '')}")
        for idx, e in enumerate(entries, 1):
            mark = " (USED)" if used_keys and e["ID"] in used_keys else ""
            print(f"{idx}: {e.get('ID','')} | DOI: {e.get('doi','N/A')} | Year: {e.get('year','N/A')}{mark}")

        choice = input("Choose which entry to keep (1, 2, ...), or 's' to skip: ").strip().lower()
        if choice == 's':
            kept_entries.extend(entries)
            continue
        try:
            keep_idx = int(choice) - 1
            keep_key = entries[keep_idx]['ID']
            kept_entries.append(entries[keep_idx])
            for idx, e in enumerate(entries):
                if idx != keep_idx:
                    replacements.append((e['ID'], keep_key))
        except (ValueError, IndexError):
            print("Invalid choice, skipping...")
            kept_entries.extend(entries)

    # Write updated .bib file
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = kept_entries
    with open("deduplicated.bib", "w", encoding="utf-8") as out:
        out.write(bibtexparser.dumps(db))

    # Write sed script
    with open("replace_keys.sed", "w", encoding="utf-8") as sedf:
        for old, new in replacements:
            sedf.write(f"s/\\\\cite{{{old}}}/\\\\cite{{{new}}}/g\n")
            sedf.write(f"s/\\\\citep{{{old}}}/\\\\citep{{{new}}}/g\n")
            sedf.write(f"s/\\\\citet{{{old}}}/\\\\citet{{{new}}}/g\n")

    print("\nSaved deduplicated.bib and replace_keys.sed")

def main():
    parser = argparse.ArgumentParser(
        description=USAGE_MESSAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bib", required=True, help="Path to .bib file")
    parser.add_argument("--show", action="store_true", help="Show duplicate entries")
    parser.add_argument("--deduplicate", action="store_true", help="Interactively deduplicate entries")
    parser.add_argument("--tex", nargs="+", help="Path(s) to .tex file(s) to check for used keys")
    args = parser.parse_args()

    with open(args.bib, encoding="utf-8") as bibfile:
        db = bibtexparser.load(bibfile)

    duplicates = find_duplicates(db.entries)
    used_keys = extract_used_keys(args.tex) if args.tex else None

    if args.show:
        show_duplicates(duplicates, used_keys)
    elif args.deduplicate:
        interactive_deduplicate(duplicates, used_keys)
    else:
        print("Please specify either --show or --deduplicate")
        sys.exit(1)

if __name__ == "__main__":
    main()
