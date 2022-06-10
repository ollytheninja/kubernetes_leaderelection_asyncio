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
import asyncio
import os
import uuid

# Authenticate using config file
from kubernetes_asyncio.client import ApiClient, CoreV1Api
from kubernetes_asyncio.config import load_incluster_config

import electionconfig
import leaderelection
from resourcelock.configmaplock import ConfigMapLock


async def main():
    load_incluster_config()

    # A unique identifier for this candidate
    candidate_id = uuid.uuid4()

    # Name of the lock object to be created
    lock_name = os.getenv("LOCK_NAME")

    # Kubernetes namespace
    lock_namespace = os.getenv("LOCK_NAMESPACE")



    # The function that a user wants to run once a candidate is elected as a leader
    def became_leader():
        print("I am now leader")

    # The function that a user wants to run once a candidate is no longer leader
    def stopped_leading():
        print("I am no longer leader")

    async with ApiClient() as api:
        v1 = CoreV1Api(api)

        # A user can choose not to provide any callbacks for what to do when a candidate fails to lead - onStoppedLeading()
        # In that case, a default callback function will be used

        # Create config
        config = electionconfig.Config(ConfigMapLock(lock_name, lock_namespace, candidate_id, v1), lease_duration=17,
                                       renew_deadline=15, retry_period=5, onstarted_leading=became_leader,
                                       onstopped_leading=stopped_leading)

        # Enter leader election
        await leaderelection.LeaderElection(config).run()

    # User can choose to do another round of election or simply exit
    print("Exited leader election")


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
