Organizing BibTeX file before submission to a journal.

# Contents
- [citekeys.py](citekeys.py): Script to print citekeys present in a BibTeX file.
- [clean-bib.py](clean-bib.py): Script to clean a BibTeX file by removing unused citekeys.
- [journal-names.py](journal-names.py): Script to print journal names present in a BibTeX file.
- [journal-name-sub.py](journal-name-sub.py): Script to substitute long journal names with their short forms.
- [pages-field.py](pages-field.py): Script to add pages fields to entries in a BibTeX file.
- [fix title case py](fix-title-case.py): This retains the case of the title of the bibliography entry. This is only needed if one is using `biblatex`. For `biber` this is not required.
- [unused_figs py](unused_figs.py): prints the unused figures in a tex file, which can be piped into `xargs rm` or `xargs mv` to delete or move them. There is also option to package files to a new folder, easier for submissions.
- [bibdeduplicate.py](bibdeduplicate.py): Detects duplicate bibliography entries (same work, different citekeys) and interactively lets you choose which to keep.
