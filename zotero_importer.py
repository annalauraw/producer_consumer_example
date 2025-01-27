from threading_classes import Zotero_Items_Import_Thread
from queue import Queue

NR_THREADS = 5

class Zotero_Importer:

      """Imports book items into a Zotero group library."""

      def __init__(
                  self, 
                  zotero_items_queue: Queue
            ):
            self.zotero_items_queue = zotero_items_queue
            # create threads for importing book items to Zotero
            self.importer_threads = tuple((
                Zotero_Items_Import_Thread(
                    name=f"Zotero_Importer_Thread-{str(i)}", 
                    queue=self.zotero_items_queue,
                    zotero_importer_obj=self
                ) for i in range(NR_THREADS)
            ))

      def post_single_item(self, book_item: dict):
            """
            Post a book item to a Zotero group library.
            """
            pass

      def import_book_items(self):
            for thread in self.importer_threads:
                thread.start()