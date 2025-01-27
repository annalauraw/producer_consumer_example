# Producer-consumer architecture example

This repository contains some example code to illustrate and discuss a producer-consumer pipeline architecture. It is the reduction of a more complex application. The code is incomplete and not intended to be run as is. 

### What the program does

- fetch bibliographic data from an API called *Bibliography Service* and write it to a first queue
- enrich the book metadata from the first queue and write it to a second queue
- take the enriched book metadata from the second queue and import it into a Zotero group library via Web API

### Classes

- Bibliography_Service_Fetcher_Thread
- Book_Items_Enricher
- Book_Items_Enricher_Thread
- Zotero_Importer
- Zotero_Items_Import_Thread

### Discussion

Two central methods in the data processing workflow are Book_Items_Enricher::process_single_item() and Zotero_Importer::post_single_item(). They are called from the run() method of their associated thread objects. Data is passed back and forth between e.g. Book_Items_Enricher and Book_Items_Enricher_Thread objects. Is this a sensible architecture for a multi-threaded application with a producer-consumer logic? Or are there better ways to set this up, especially regarding code readability and maintainability?

### Dependencies

- requests

Developed with Python 3.11