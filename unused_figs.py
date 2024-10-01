#!/usr/bin/env python

import os
import re
import sys
import argparse

def get_pdf_files(directory, latex_pdf_file):
    """Get all PDF files in the specified directory, excluding the LaTeX-generated PDF."""
    return {f for f in os.listdir(directory) if f.endswith('.pdf') and f != latex_pdf_file}

def get_used_figures(latex_file):
    """Extract used figures (PDFs) from the LaTeX file."""
    with open(latex_file, 'r') as file:
        content = file.read()

    # Regex pattern to find includegraphics commands
    pattern = re.compile(r'\\includegraphics(\[.*?\])?{(.+?\.pdf)}')
    used_figures = set(match.group(2) for match in pattern.finditer(content))

    return used_figures

def find_unused_figures(latex_file):
    """Find and return PDF files that are not used in the LaTeX file."""
    # Get the LaTeX-generated PDF file name (assumes the same base name as the LaTeX file)
    latex_pdf_file = os.path.basename(latex_file).replace('.tex', '.pdf')
    
    # Get PDF files in the current directory, excluding the LaTeX-generated PDF
    pdf_files = get_pdf_files(os.getcwd(), latex_pdf_file)

    # Get used figures from the LaTeX file
    used_figures = get_used_figures(latex_file)

    # Compare the sets
    unused_figures = pdf_files - used_figures

    return unused_figures

def print_used_figures(latex_file):
    """Print the used PDF figures in the LaTeX file."""
    used_figures = get_used_figures(latex_file)
    if used_figures:
        for fig in used_figures:
            print(fig)
    else:
        print("No PDF figures used in the LaTeX file.")

def print_unused_figures(latex_file):
    """Print the unused PDF figures in the LaTeX file."""
    unused_figures = find_unused_figures(latex_file)
    if unused_figures:
        for fig in unused_figures:
            print(fig)
    else:
        print("All PDF figures are used.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find used or unused PDF figures in a LaTeX file.")
    parser.add_argument("latex_file", help="Path to the LaTeX file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--used", action="store_true", help="Print used PDF figures.")
    group.add_argument("--unused", action="store_true", help="Print unused PDF figures.")

    args = parser.parse_args()

    # Check if the LaTeX file exists
    if not os.path.isfile(args.latex_file):
        print(f"Error: The file '{args.latex_file}' does not exist.")
        sys.exit(1)

    # Print used or unused figures based on the command-line option
    if args.used:
        print_used_figures(args.latex_file)
    elif args.unused:
        print_unused_figures(args.latex_file)
