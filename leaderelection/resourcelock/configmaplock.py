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
import logging
from typing import Optional, Tuple, Union
from uuid import UUID

from kubernetes_asyncio import client
from kubernetes_asyncio.client import CoreV1Api
from kubernetes_asyncio.client.rest import ApiException

from leaderelectionrecord import get_lock_object, LeaderElectionRecord

logging.basicConfig(level=logging.INFO)


class ConfigMapLock:
    def __init__(self, name: str, namespace: str, identity: UUID, k8s_api: CoreV1Api):
        """
        :param name: name of the lock
        :param namespace: namespace
        :param identity: A unique identifier that the candidate is using
        """
        self.api_instance = k8s_api
        self.leader_electionrecord_annotationkey = 'control-plane.alpha.kubernetes.io/leader'
        self.name = name
        self.namespace = namespace
        self.identity = str(identity)
        self.configmap_reference = None
        self.lock_record = {
            'holderIdentity': None,
            'leaseDurationSeconds': None,
            'acquireTime': None,
            'renewTime': None
        }

    # get returns the election record from a ConfigMap Annotation
    async def get(self) -> Tuple[bool, Union[Optional[LeaderElectionRecord], Exception]]:
        """
        :return: 'True, election record' if object found else 'False, exception response'
        """
        try:
            api_response = await self.api_instance.read_namespaced_config_map(self.name, self.namespace)

            # If an annotation does not exist - add the leader_electionrecord_annotationkey
            annotations = api_response.metadata.annotations
            if annotations is None or annotations == '':
                api_response.metadata.annotations = {self.leader_electionrecord_annotationkey: ''}
                self.configmap_reference = api_response
                return True, None

            # If an annotation exists but, the leader_electionrecord_annotationkey does not then add it as a key
            if not annotations.get(self.leader_electionrecord_annotationkey):
                api_response.metadata.annotations = {self.leader_electionrecord_annotationkey: ''}
                self.configmap_reference = api_response
                return True, None

            lock_record = get_lock_object(json.loads(annotations[self.leader_electionrecord_annotationkey]))

            self.configmap_reference = api_response
            return True, lock_record
        except ApiException as e:
            return False, e

    async def create(self, election_record: LeaderElectionRecord) -> bool:
        """
        :param election_record: Annotation string
        :return: 'True' if object is created else 'False' if failed
        """
        body = client.V1ConfigMap(
            metadata={
                "name": self.name,
                "annotations": {
                    self.leader_electionrecord_annotationkey: election_record.to_json()
                }
            }
        )

        try:
            api_response = await self.api_instance.create_namespaced_config_map(self.namespace, body, pretty=True)
            return True
        except ApiException as e:
            logging.info("Failed to create lock as {}".format(e))
            return False

    async def update(self, updated_record: LeaderElectionRecord) -> bool:
        """
        :param updated_record: the updated election record
        :return: True if update is succesful False if it fails
        """
        try:
            # Set the updated record
            self.configmap_reference.metadata.annotations[self.leader_electionrecord_annotationkey] = updated_record.to_json()
            api_response = await self.api_instance.replace_namespaced_config_map(
                name=self.name, namespace=self.namespace,
                body=self.configmap_reference)
            return True
        except ApiException as e:
            logging.info("Failed to update lock as {}".format(e))
            return False
