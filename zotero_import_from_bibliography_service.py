from zotero_importer import Zotero_Importer
from book_items_enricher import Book_Items_Enricher
from threading_classes import Bibliography_Service_Fetcher_Thread
from queue import Queue


def import_from_bibliography_service(
    bib_series: str,
    issue: str,
):

    importer = Zotero_Importer(
        bib_series=bib_series,
        issue_nr=issue,
        # Zotero book items to be imported
        zotero_items_queue=Queue(maxsize=100)
    )

    # queue for book items fetched from the bibliography service API
    book_items_bs_queue = Queue(maxsize=100)

    # params for the request to the bibliography_service API
    issue_params = {
        'bibseries': bib_series,
        'issue': issue,
    }

    # fill the queue with the issue's book objects from the bibliography service API
    book_items_fetcher_thread = Bibliography_Service_Fetcher_Thread(
        name='Zotero_Items_Fetcher',
        output_queue=book_items_bs_queue,
        bs_endpoint='http://localhost/bibliographies/api/v1/books/zotero/',
        issue_params=issue_params
    )

    book_items_fetcher_thread.start()

    # add some additional information to the book items
    enricher = Book_Items_Enricher(
        input_items_queue=book_items_bs_queue,
        output_items_queue=importer.zotero_items_queue,
    )

    enricher.enrich_book_items()

    importer.import_book_items()