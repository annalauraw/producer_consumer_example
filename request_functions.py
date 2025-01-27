import requests
from queue import Queue
    
def get_bs_response(request_url: str, params: dict|None = None):
    response = requests.get(request_url, headers=None, **params)
    # get the response object as a dictionary
    response_obj = response.json()
    return response_obj
    
def get_book_items_from_bs(books_endpoint: str, queue: Queue, issue_params: dict|None = None) -> list:
    """"
    Get book items from the Bibliography Service API.
    """
    response_obj = get_bs_response(request_url=books_endpoint, params=issue_params)

    for item in response_obj['results']:
        queue.put(item)