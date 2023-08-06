from worker import constants

constants.update({
    "global": {
        "app-name": "WorkerTest.StateMixin",
        "app-key": "worker_test-state_mixin",
        "event-type": "wits_stream",
        "query-limit": 3600
    },
    "worker_test-state_mixin": {
        "mongo-tester": {},
        "redis-tester": {},
        "migration-tester": {
            "running_frequency": 0  # just for testing with trigger module
        }
    }
})
