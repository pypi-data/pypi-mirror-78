from ..todo import LogToDo, LamagramToDo
from django.conf import settings


def log(response, status_code, index: str, doc, args=None, params=None, headers=None):
    metadata = response.get('metadata')
    status = response.get('status')
    todo = LogToDo(response, status_code, index, doc, args, headers, params)
    results = todo.process()
    transaction = {
        'status': status,
        'index': index,
    }
    lamagram_message = [status_code, index]
    for result in results:
        transaction.update(result)
        if result.get('elastic_id'):
            lamagram_message.append(result.get('elastic_id'))
        elif result.get('sentry_code'):
            lamagram_message.append(result.get('sentry_code'))
    chat_id = getattr(settings, 'LAMAGRAM_CHAT_ID', None)
    if chat_id is not None:
        todo = LamagramToDo(chat_id, str.join('\n', lamagram_message), status_code)
        todo.process()

    metadata.update({
        'transaction': transaction
    })
    return response, status_code
