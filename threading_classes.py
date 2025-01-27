from threading import Thread, Event
from queue import Queue
import request_functions as r


class Bibliography_Service_Fetcher_Thread(Thread):
    """
    Fetches book items from the bibliography service API and puts them into the input queue
    for the Book_Items_Enricher_Thread instances.
    """
    def __init__(
                self, 
                name: str, 
                output_queue: Queue,
                bs_endpoint: str,
                issue_params: dict,
            ):
        super().__init__(name=name, daemon=False)
        self.__queue = output_queue
        self.bs_endpoint = bs_endpoint
        self.issue_params = issue_params

    def run(self):

        # fetch Zotero items from the bibliography service API
        # and put them into the output queue
        r.get_book_items_from_bs(
            books_endpoint=self.bs_endpoint,
            queue=self.__queue,
            issue_params=self.issue_params,
        )

class Book_Items_Enricher_Thread(Thread):
    
    """
    Enriches book items from an input queue and puts them into an output queue.
    To be used in conjunction with Book_Items_Enricher::process_single_item().
    """
        
    def __init__(
            self, 
            name: str, 
            input_queue: Queue,
            output_queue: Queue,
            enricher_obj    # a Book_Items_Enricher instance
        ):
        super().__init__(name=name, daemon=False)
        self.__input_queue = input_queue
        self.__output_queue = output_queue
        self.enricher = enricher_obj
        self.__stop_event = Event()

    def stop(self):
        if not self.__stop_event.is_set():
            self.__stop_event.set()

    def run(self):
        while not self.__stop_event.is_set() or not self.__input_queue.empty():
            book_item = self.__input_queue.get(block=True, timeout=1)
            # call the Book_Items_Enricher instance's method to enrich
            # the book item
            enriched_book_item = self.enricher.process_single_item(book_item)
            self.__output_queue.put(enriched_book_item, block=True, timeout=1)


class Zotero_Items_Import_Thread(Thread):
    
    """
    Consumes enriched book items from an input queue and imports them 
    into a Zotero library.
    To be used in conjunction with Zotero_Importer::post_single_item().
    """
        
    def __init__(
            self, 
            name: str, 
            zotero_importer_obj: object,    # an instance of Zotero_Importer 
            queue: Queue, 
        ):
        super().__init__(name=name, daemon=False)
        self.zotero_importer = zotero_importer_obj
        self.__queue = queue
        self.__stop_event = Event()

    def __str__(self):
        return self.name

    def stop(self):
        if not self.__stop_event.is_set():
            self.__stop_event.set()

    def run(self):
        while not self.__stop_event.is_set() or not self.__queue.empty():
            enriched_book_item = self.__queue.get(block=True, timeout=1)
            self.zotero_importer.post_single_item(enriched_book_item)