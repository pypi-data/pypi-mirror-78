import json
import threading
from .engineapi.api import get_engine_api
from ._loggerfactory import _LoggerFactory, session_id, instrumentation_key, log_directory, verbosity, HBI_MODE


log = _LoggerFactory.get_logger('rslex_executor')


class _RsLexExecutor:
    def __init__(self):
        self._pending_executions = {}

    def await_result(self, execution_id, callback, fail_on_error, fail_on_mixed_types, fail_on_out_of_range_datetime):
        self._pending_executions[execution_id] = \
            (callback, fail_on_error, fail_on_mixed_types, fail_on_out_of_range_datetime)

    def _load_pending_execution(self, execution_id):
        if execution_id is None:
            return None, False, False, False
        else:
            return self._pending_executions.pop(execution_id)

    def execute_rslex_script(self, request, writer):
        try:
            from azureml.dataprep.rslex._rslex_loader import run_lariat
            script = request.get('script')
            execution_id = request.get('executionId')
            callback, fail_on_error, fail_on_mixed_types, fail_on_out_of_range_datetime = \
                self._load_pending_execution(execution_id)

            error = None
            result = run_lariat(script,
                                callback is not None,
                                fail_on_error,
                                fail_on_mixed_types,
                                fail_on_out_of_range_datetime,
                                get_rslex_context())
            message = result.message
            if message != '':
                error = message
            else:
                if callback is not None:
                    callback(result.batches)
                writer.write(json.dumps({'result': 'success', 'partitionCount': result.n_partitions}) + '\n')
        except Exception as e:
            error = repr(e)
        finally:
            if error is not None:
                writer.write(json.dumps({'result': 'error', 'error': error}) + '\n')
                log.info('Execution failed with rslex.\nFallback to clex.')


_rslex_executor = None
_rslex_context = None
_rslex_context_lock = threading.Lock()


def get_rslex_executor():
    global _rslex_executor
    if _rslex_executor is None:
        _rslex_executor = _RsLexExecutor()
    get_rslex_context()

    return _rslex_executor


def get_rslex_context(caller_session_id: str = None):
    global _rslex_context
    if _rslex_context is None:
        try:
            # Acquire lock on mutable access to _rslex_context
            _rslex_context_lock.acquire()
            # Was _rslex_context set while we held the lock?
            if _rslex_context is not None:
                return _rslex_context
            # Create new RsLexContext
            import atexit
            from azureml.dataprep.rslex._rslex_loader import create_rslex_context
            engine_api = get_engine_api()
            run_info = _LoggerFactory._try_get_run_info()
            _rslex_context = create_rslex_context(
                engine_api._engine_server_port,
                engine_api._engine_server_secret,
                log_directory,
                instrumentation_key,
                verbosity,
                HBI_MODE,
                session_id,
                caller_session_id if caller_session_id is not None else "",
                json.dumps(run_info) if run_info is not None else ""
            )
            atexit.register(_release_rslex_context)
        except Exception as e:
            log.error('get_rslex_context failed with {}'.format(e))
            raise
        finally:
            if _rslex_context_lock.locked():
                _rslex_context_lock.release()
    return _rslex_context


def _release_rslex_context():
    global _rslex_context
    if _rslex_context is not None:
        # Acquire lock on mutable access to _rslex_context
        _rslex_context_lock.acquire()
        # Was _rslex_context unset while we held the lock?
        if _rslex_context is None:
            return
        context = _rslex_context
        _rslex_context = None
        _rslex_context_lock.release()
        from azureml.dataprep.rslex._rslex_loader import release_rslex_context
        release_rslex_context(context)


def use_rust_execution(use: bool):
    get_engine_api().use_rust_execution(use)
    if use is True:
        get_rslex_context()


def ensure_rslex_handler(requests_channel):
    requests_channel.register_handler('execute_rslex_script',
                                      lambda r, w, _: get_rslex_executor().execute_rslex_script(r, w))
