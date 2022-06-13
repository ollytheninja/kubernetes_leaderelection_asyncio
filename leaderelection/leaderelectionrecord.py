# Copyright 2021 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from typing import Dict


class LeaderElectionRecord:
    # Annotation used in the lock object
    def __init__(self, holder_identity: str, lease_duration: str, acquire_time: str, renew_time: str):
        self.holder_identity = holder_identity
        self.lease_duration = lease_duration
        self.acquire_time = acquire_time
        self.renew_time = renew_time

    def to_dict(self) -> Dict[str, str]:
        out = {
            'holderIdentity': self.holder_identity,
            'leaseDurationSeconds': self.lease_duration,
            'acquireTime': self.acquire_time,
            'renewTime': self.renew_time
        }
        return out

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def get_lock_object(lock_record: Dict) -> LeaderElectionRecord:
    return LeaderElectionRecord(
        lock_record.get('holderIdentity'),
        lock_record.get('leaseDurationSeconds'),
        lock_record.get('acquireTime'),
        lock_record.get('renewTime'),
    )
