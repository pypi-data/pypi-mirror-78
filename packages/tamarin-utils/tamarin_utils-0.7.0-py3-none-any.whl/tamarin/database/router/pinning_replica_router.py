from .utils import get_replica, this_thread_is_pinned, PRIMARY_DB_ALIAS
from .replica_router import ReplicaRouter


class PinningReplicaRouter(ReplicaRouter):
    """Router that sends reads to master if a certain flag is set. Writes
    always go to master.
    Typically, we set a cookie in middleware for certain request HTTP methods
    and give it a max age that's certain to be longer than the replication lag.
    The flag comes from that cookie.
    """

    def db_for_read(self, model, **hints):
        """Send reads to replicas in round-robin unless this thread is "stuck" to
        the master."""
        return PRIMARY_DB_ALIAS if this_thread_is_pinned() else get_replica()
