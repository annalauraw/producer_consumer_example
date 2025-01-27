from zotero_import_from_bibliography_service import import_from_bibliography_service

# number of bibliography issue 
issue_year = '2025'
issue_month = '01'
# French National Bibliography
bib_series = 'BNF'
issue = f'{issue_year}_{issue_month}'

import_from_bibliography_service(
    bib_series = bib_series,
    issue = issue,
)