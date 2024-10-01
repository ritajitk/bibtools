#!/usr/bin/env python

import os
import re
import sys

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
    """Find and print PDF files that are not used in the LaTeX file."""
    # Get the LaTeX-generated PDF file name (assumes the same base name as the LaTeX file)
    latex_pdf_file = os.path.basename(latex_file).replace('.tex', '.pdf')
    
    # Get PDF files in the current directory, excluding the LaTeX-generated PDF
    pdf_files = get_pdf_files(os.getcwd(), latex_pdf_file)

    # Get used figures from the LaTeX file
    used_figures = get_used_figures(latex_file)

    # Compare the sets
    unused_figures = pdf_files - used_figures

    if unused_figures:
        for fig in unused_figures:
            print(fig)
    else:
        print("All PDF figures are used.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ",sys.argv[0]," <latex_file.tex>")
        sys.exit(1)

    latex_file_path = sys.argv[1]

    # Check if the LaTeX file exists
    if not os.path.isfile(latex_file_path):
        print(f"Error: The file '{latex_file_path}' does not exist.")
        sys.exit(1)

    # Run the function
    find_unused_figures(latex_file_path)
