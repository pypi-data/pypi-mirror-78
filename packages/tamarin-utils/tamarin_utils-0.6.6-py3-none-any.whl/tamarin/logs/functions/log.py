from ..todo import LogToDo


def log(response, status_code, index: str, doc, args=None, params=None, headers=None):
    metadata = response.get('metadata')
    status = response.get('status')
    todo = LogToDo(response, status_code, index, doc, args, headers, params)
    results = todo.process()
    transaction = {
        'status': status,
        'index': index,
    }
    for result in results:
        transaction.update(result)
    metadata.update({
        'transaction': transaction
    })
    return response, status_code
