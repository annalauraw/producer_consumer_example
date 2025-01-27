from threading_classes import Book_Items_Enricher_Thread
from queue import Queue 

NR_THREADS = 5

class Book_Items_Enricher:

    """
    Class for enriching Zotero book items.
    """

    def __init__(
            self, 
            input_items_queue: Queue,
            output_items_queue: Queue,
            ):
        self.input_items_queue = input_items_queue
        self.output_items_queue = output_items_queue
        # create threads for enriching book items
        self.enricher_threads = tuple(( Book_Items_Enricher_Thread(
            name=f"Enricher_Thread-{str(i)}", 
            input_queue=self.input_items_queue,
            output_queue=self.output_items_queue,
            enricher_obj=self
        ) for i in range(NR_THREADS) ))

    def process_single_item(self, book_item: dict):
        """
        Enriches a single book item and returns it.
        """
        pass
                 
    def enrich_book_items(self):
        for thread in self.enricher_threads:
            thread.start()