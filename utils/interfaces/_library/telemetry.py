from time import time

from utils.interfaces._core import BaseValidation

TELEMETRY_AGENT_ENDPOINT = "/telemetry/proxy/api/v2/apmtelemetry"
TELEMETRY_INTAKE_ENDPOINT = "/api/v2/apmtelemetry"


# TODO: movethis test logic in test class
class _SeqIdLatencyValidation(BaseValidation):
    """Verify that the messages seq_id s are sent somewhat in-order."""

    MAX_OUT_OF_ORDER_LAG = 0.1  # s
    path_filters = TELEMETRY_AGENT_ENDPOINT
    is_success_on_expiry = True

    def __init__(self):
        super().__init__()
        self.max_seq_id = 0
        self.received_max_time = None

    def check(self, data):
        seq_id = data["request"]["content"]["seq_id"]
        now = time()
        if seq_id > self.max_seq_id:
            self.max_seq_id = seq_id
            self.received_max_time = now
        else:
            if self.received_max_time is not None and (now - self.received_max_time) > self.MAX_OUT_OF_ORDER_LAG:
                self.set_failure(
                    f"Received message with seq_id {seq_id} to far more than"
                    f"100ms after message with seq_id {self.max_seq_id}"
                )


class _NoSkippedSeqId(BaseValidation):
    """Verify that the messages seq_id s are sent somewhat in-order."""

    path_filters = TELEMETRY_AGENT_ENDPOINT
    is_success_on_expiry = True

    def __init__(self):
        super().__init__()
        self.seq_ids = []

    def check(self, data):
        seq_id = data["request"]["content"]["seq_id"]
        self.seq_ids.append((seq_id, data["log_filename"]))

    def final_check(self):
        self.seq_ids.sort()
        for i in range(len(self.seq_ids) - 1):
            diff = self.seq_ids[i + 1][0] - self.seq_ids[i][0]
            if diff == 0:
                self.set_failure(
                    f"Detected 2 telemetry messages with same seq_id {self.seq_ids[i + 1][1]} and {self.seq_ids[i][1]}"
                )
            elif diff > 1:
                self.set_failure(
                    f"Detected non conscutive seq_ids between {self.seq_ids[i + 1][1]} and {self.seq_ids[i][1]}"
                )
