import os
import re
import sys
import argparse
import shutil

def get_pdf_files(directory, latex_pdf_file):
    """Get all PDF files in the specified directory, excluding the LaTeX-generated PDF."""
    return {f for f in os.listdir(directory) if f.endswith('.pdf') and f != latex_pdf_file}

def get_used_figures(latex_file):
    """Extract used figures (PDFs) from the LaTeX file."""
    with open(latex_file, 'r') as file:
        content = file.read()
    
    pattern = re.compile(r'\\includegraphics(?:\[.*?\])?{(.+?\.pdf)}')
    used_figures = set(match.group(1) for match in pattern.finditer(content))
    
    return used_figures

def get_used_bib_files(latex_file):
    """Extract used bibliography files from the LaTeX file."""
    with open(latex_file, 'r') as file:
        content = file.read()
    
    pattern = re.compile(r'\\(?:bibliography|addbibresource){(.+?)}')
    bib_files = set()
    for match in pattern.finditer(content):
        bib_base_names = match.group(1).split(',')
        for bib_base_name in bib_base_names:
            bib_base_name = bib_base_name.strip()
            if not bib_base_name.endswith(".bib"):
                bib_base_name += ".bib"
            bib_files.add(bib_base_name)
    
    return bib_files

def get_bbl_file(latex_file):
    """Get the corresponding BBL file if it exists; otherwise, print an error and exit."""
    bbl_file = os.path.splitext(latex_file)[0] + ".bbl"
    if not os.path.exists(bbl_file):
        print(f"Error: The BBL file '{bbl_file}' does not exist. Run BibTeX first.")
        sys.exit(1)
    return {bbl_file}

def find_unused_figures(latex_file):
    """Find and return PDF files that are not used in the LaTeX file."""
    latex_pdf_file = os.path.basename(latex_file).replace('.tex', '.pdf')
    pdf_files = get_pdf_files(os.getcwd(), latex_pdf_file)
    used_figures = get_used_figures(latex_file)
    return pdf_files - used_figures

def print_used_figures(latex_file):
    """Print the used PDF figures in the LaTeX file."""
    used_figures = get_used_figures(latex_file)
    print("\n".join(used_figures) if used_figures else "No PDF figures used in the LaTeX file.")

def print_unused_figures(latex_file):
    """Print the unused PDF figures in the LaTeX file."""
    unused_figures = find_unused_figures(latex_file)
    print("\n".join(unused_figures) if unused_figures else "All PDF figures are used.")

def package_latex_project(latex_file, output_folder=None):
    """Create a folder containing all used figures, the LaTeX file, bibliography files, and BBL file."""
    base_dir = os.getcwd()
    base_name = os.path.splitext(os.path.basename(latex_file))[0]
    
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    files_to_copy = {latex_file} | get_used_figures(latex_file) | get_used_bib_files(latex_file) | get_bbl_file(latex_file)
    files_to_copy = {f for f in files_to_copy if os.path.exists(f)}
    
    if output_folder:
        for file in files_to_copy:
            shutil.copy(file, os.path.join(output_folder, os.path.basename(file)))
        print(f"Files copied to folder: {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find used/unused PDF figures and package LaTeX project files.")
    parser.add_argument("latex_file", help="Path to the LaTeX file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--used", action="store_true", help="Print used PDF figures.")
    group.add_argument("--unused", action="store_true", help="Print unused PDF figures.")
    group.add_argument("--package", metavar="FOLDER", help="Copy used files to the specified folder.")

    args = parser.parse_args()
    
    if not os.path.isfile(args.latex_file):
        print(f"Error: The file '{args.latex_file}' does not exist.")
        sys.exit(1)
    
    if args.used:
        print_used_figures(args.latex_file)
    elif args.unused:
        print_unused_figures(args.latex_file)
    elif args.package:
        package_latex_project(args.latex_file, output_folder=args.package)
