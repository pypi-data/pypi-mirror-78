from ..multiprocessing import Todo
from ..sentry.commands import SentryCommand
from ..elasticsearch.commands import ElasticSearchCommand


class LogToDo(Todo):
    def __init__(self, response, status_code, index, doc, args, headers, params):
        sentry_cmd = SentryCommand(response, status_code)
        elastic_cmd = ElasticSearchCommand(response, status_code, index, doc, args, headers, params)
        commands = [sentry_cmd, elastic_cmd]
        super(LogToDo, self).__init__(commands)
