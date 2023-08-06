# This is a copy-paste from the Airflow repository
# the version 1.10 of the KubernetesPodOperator does
# not have init_containers which we need for some integrations
#
# I pulled some dependencies into the same file so it's self
# contained (and we can remove it with a future Airflow update)

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Executes task in a Kubernetes POD"""
import copy
import hashlib
import inspect
import json
import os
import re
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime as dt
from functools import reduce
from typing import Dict, List, Optional, Tuple, Union

import kubernetes.client.models as k8s
import tenacity
import yaml
from airflow.configuration import conf
from airflow.contrib.kubernetes.pod import Port
from airflow.contrib.kubernetes.pod_runtime_info_env import PodRuntimeInfoEnv
from airflow.contrib.kubernetes.secret import Secret
from airflow.exceptions import AirflowConfigException, AirflowException
from airflow.models import BaseOperator
from airflow.settings import pod_mutation_hook
from airflow.utils.decorators import apply_defaults
from airflow.utils.helpers import validate_key
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.state import State
from airflow.version import version as airflow_version
from kubernetes import client, watch
from kubernetes.client.api_client import ApiClient
from kubernetes.client.models.v1_pod import V1Pod
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream as kubernetes_stream
from requests.exceptions import BaseHTTPError

# -- kube_client

try:
    from kubernetes import config, client
    from kubernetes.client.rest import ApiException  # pylint: disable=unused-import
    from kubernetes.client.api_client import ApiClient
    from kubernetes.client import Configuration
    from airflow.contrib.kubernetes.refresh_config import (  # pylint: disable=ungrouped-imports
        load_kube_config,
        RefreshConfiguration,
    )

    has_kubernetes = True

    def _get_kube_config(
        in_cluster: bool, cluster_context: Optional[str], config_file: Optional[str]
    ) -> Optional[Configuration]:
        if in_cluster:
            # load_incluster_config set default configuration with config populated by k8s
            config.load_incluster_config()
            return None
        else:
            # this block can be replaced with just config.load_kube_config once
            # refresh_config module is replaced with upstream fix
            cfg = RefreshConfiguration()
            load_kube_config(
                client_configuration=cfg,
                config_file=config_file,
                context=cluster_context,
            )
            return cfg

    def _get_client_with_patched_configuration(
        cfg: Optional[Configuration],
    ) -> client.CoreV1Api:
        """
        This is a workaround for supporting api token refresh in k8s client.
        The function can be replace with `return client.CoreV1Api()` once the
        upstream client supports token refresh.
        """
        if cfg:
            return client.CoreV1Api(api_client=ApiClient(configuration=cfg))
        else:
            return client.CoreV1Api()


except ImportError as e:
    # We need an exception class to be able to use it in ``except`` elsewhere
    # in the code base
    ApiException = BaseException
    has_kubernetes = False
    _import_err = e


def get_kube_client(
    in_cluster: bool = conf.getboolean("kubernetes", "in_cluster"),
    cluster_context: Optional[str] = None,
    config_file: Optional[str] = None,
) -> client.CoreV1Api:
    """
    Retrieves Kubernetes client
    :param in_cluster: whether we are in cluster
    :type in_cluster: bool
    :param cluster_context: context of the cluster
    :type cluster_context: str
    :param config_file: configuration file
    :type config_file: str
    :return kubernetes client
    :rtype client.CoreV1Api
    """

    if not has_kubernetes:
        raise _import_err

    if not in_cluster:
        if cluster_context is None:
            cluster_context = conf.get("kubernetes", "cluster_context", fallback=None)
        if config_file is None:
            config_file = conf.get("kubernetes", "config_file", fallback=None)

    client_conf = _get_kube_config(in_cluster, cluster_context, config_file)
    return _get_client_with_patched_configuration(client_conf)


# -- PodLauncher


class PodStatus:
    """Status of the PODs"""

    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    SUCCEEDED = "succeeded"


class PodLauncher(LoggingMixin):
    """Launches PODS"""

    def __init__(
        self,
        kube_client: client.CoreV1Api = None,
        in_cluster: bool = True,
        cluster_context: Optional[str] = None,
        extract_xcom: bool = False,
    ):
        """
        Creates the launcher.
        :param kube_client: kubernetes client
        :param in_cluster: whether we are in cluster
        :param cluster_context: context of the cluster
        :param extract_xcom: whether we should extract xcom
        """
        super().__init__()
        self._client = kube_client or get_kube_client(
            in_cluster=in_cluster, cluster_context=cluster_context
        )
        self._watch = watch.Watch()
        self.extract_xcom = extract_xcom

    def run_pod_async(self, pod: V1Pod, **kwargs):
        """Runs POD asynchronously"""
        pod_mutation_hook(pod)

        sanitized_pod = self._client.api_client.sanitize_for_serialization(pod)
        json_pod = json.dumps(sanitized_pod, indent=2)

        self.log.debug("Pod Creation Request: \n%s", json_pod)
        try:
            resp = self._client.create_namespaced_pod(
                body=sanitized_pod, namespace=pod.metadata.namespace, **kwargs
            )
            self.log.debug("Pod Creation Response: %s", resp)
        except Exception as e:
            self.log.exception(
                "Exception when attempting " "to create Namespaced Pod: %s", json_pod
            )
            raise e
        return resp

    def delete_pod(self, pod: V1Pod):
        """Deletes POD"""
        try:
            self._client.delete_namespaced_pod(
                pod.metadata.name, pod.metadata.namespace, body=client.V1DeleteOptions()
            )
        except ApiException as e:
            # If the pod is already deleted
            if e.status != 404:
                raise

    def start_pod(self, pod: V1Pod, startup_timeout: int = 120):
        """
        Launches the pod synchronously and waits for completion.
        :param pod:
        :param startup_timeout: Timeout for startup of the pod (if pod is pending for too long, fails task)
        :return:
        """
        resp = self.run_pod_async(pod)
        curr_time = dt.now()
        if resp.status.start_time is None:
            while self.pod_not_started(pod):
                delta = dt.now() - curr_time
                if delta.total_seconds() >= startup_timeout:
                    raise AirflowException("Pod took too long to start")
                time.sleep(1)
            self.log.debug("Pod not yet started")

    def monitor_pod(self, pod: V1Pod, get_logs: bool) -> Tuple[State, Optional[str]]:
        """
        Monitors a pod and returns the final state
        :param pod: pod spec that will be monitored
        :type pod : V1Pod
        :param get_logs: whether to read the logs locally
        :return:  Tuple[State, Optional[str]]
        """
        if get_logs:
            logs = self.read_pod_logs(pod)
            for line in logs:
                self.log.info(line)
        result = None
        if self.extract_xcom:
            while self.base_container_is_running(pod):
                self.log.info(
                    "Container %s has state %s", pod.metadata.name, State.RUNNING
                )
                time.sleep(2)
            result = self._extract_xcom(pod)
            self.log.info(result)
            result = json.loads(result)
        while self.pod_is_running(pod):
            self.log.info("Pod %s has state %s", pod.metadata.name, State.RUNNING)
            time.sleep(2)
        return self._task_status(self.read_pod(pod)), result

    def _task_status(self, event):
        self.log.info(
            "Event: %s had an event of type %s", event.metadata.name, event.status.phase
        )
        status = self.process_status(event.metadata.name, event.status.phase)
        return status

    def pod_not_started(self, pod: V1Pod):
        """Tests if pod has not started"""
        state = self._task_status(self.read_pod(pod))
        return state == State.QUEUED

    def pod_is_running(self, pod: V1Pod):
        """Tests if pod is running"""
        state = self._task_status(self.read_pod(pod))
        return state not in (State.SUCCESS, State.FAILED)

    def base_container_is_running(self, pod: V1Pod):
        """Tests if base container is running"""
        event = self.read_pod(pod)
        status = next(
            iter(filter(lambda s: s.name == "base", event.status.container_statuses)),
            None,
        )
        if not status:
            return False
        return status.state.running is not None

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(),
        reraise=True,
    )
    def read_pod_logs(self, pod: V1Pod, tail_lines: int = 10):
        """Reads log from the POD"""
        try:
            return self._client.read_namespaced_pod_log(
                name=pod.metadata.name,
                namespace=pod.metadata.namespace,
                container="base",
                follow=True,
                tail_lines=tail_lines,
                _preload_content=False,
            )
        except BaseHTTPError as e:
            raise AirflowException(
                "There was an error reading the kubernetes API: {}".format(e)
            )

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(),
        reraise=True,
    )
    def read_pod_events(self, pod):
        """Reads events from the POD"""
        try:
            return self._client.list_namespaced_event(
                namespace=pod.metadata.namespace,
                field_selector="involvedObject.name={}".format(pod.metadata.name),
            )
        except BaseHTTPError as e:
            raise AirflowException(
                "There was an error reading the kubernetes API: {}".format(e)
            )

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(),
        reraise=True,
    )
    def read_pod(self, pod: V1Pod):
        """Read POD information"""
        try:
            return self._client.read_namespaced_pod(
                pod.metadata.name, pod.metadata.namespace
            )
        except BaseHTTPError as e:
            raise AirflowException(
                "There was an error reading the kubernetes API: {}".format(e)
            )

    def _extract_xcom(self, pod: V1Pod):
        resp = kubernetes_stream(
            self._client.connect_get_namespaced_pod_exec,
            pod.metadata.name,
            pod.metadata.namespace,
            container=PodDefaults.SIDECAR_CONTAINER_NAME,
            command=["/bin/sh"],
            stdin=True,
            stdout=True,
            stderr=True,
            tty=False,
            _preload_content=False,
        )
        try:
            result = self._exec_pod_command(
                resp, "cat {}/return.json".format(PodDefaults.XCOM_MOUNT_PATH)
            )
            self._exec_pod_command(resp, "kill -s SIGINT 1")
        finally:
            resp.close()
        if result is None:
            raise AirflowException(
                "Failed to extract xcom from pod: {}".format(pod.metadata.name)
            )
        return result

    def _exec_pod_command(self, resp, command):
        if resp.is_open():
            self.log.info("Running command... %s\n", command)
            resp.write_stdin(command + "\n")
            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    return resp.read_stdout()
                if resp.peek_stderr():
                    self.log.info(resp.read_stderr())
                    break
        return None

    def process_status(self, job_id, status):
        """Process status information for the JOB"""
        status = status.lower()
        if status == PodStatus.PENDING:
            return State.QUEUED
        elif status == PodStatus.FAILED:
            self.log.error("Event with job id %s Failed", job_id)
            return State.FAILED
        elif status == PodStatus.SUCCEEDED:
            self.log.info("Event with job id %s Succeeded", job_id)
            return State.SUCCESS
        elif status == PodStatus.RUNNING:
            return State.RUNNING
        else:
            self.log.error("Event: Invalid state %s on job %s", status, job_id)
            return State.FAILED


# -- append_to_pod


class K8SModel(ABC):
    """
    These Airflow Kubernetes models are here for backwards compatibility
    reasons only. Ideally clients should use the kubernetes api
    and the process of
        client input -> Airflow k8s models -> k8s models
    can be avoided. All of these models implement the
    `attach_to_pod` method so that they integrate with the kubernetes client.
    """

    @abstractmethod
    def attach_to_pod(self, pod: k8s.V1Pod) -> k8s.V1Pod:
        """
        :param pod: A pod to attach this Kubernetes object to
        :type pod: kubernetes.client.models.V1Pod
        :return: The pod with the object attached
        """


def append_to_pod(pod: k8s.V1Pod, k8s_objects: Optional[List[K8SModel]]):
    """
    :param pod: A pod to attach a list of Kubernetes objects to
    :type pod: kubernetes.client.models.V1Pod
    :param k8s_objects: a potential None list of K8SModels
    :type k8s_objects: Optional[List[K8SModel]]
    :return: pod with the objects attached if they exist
    """
    if not k8s_objects:
        return pod
    return reduce(lambda p, o: o.attach_to_pod(p), k8s_objects, pod)


# -- pod


class Resources(K8SModel):
    """
    Stores information about resources used by the Pod.
    :param request_memory: requested memory
    :type request_memory: str
    :param request_cpu: requested CPU number
    :type request_cpu: float | str
    :param request_ephemeral_storage: requested ephermeral storage
    :type request_ephemeral_storage: str
    :param limit_memory: limit for memory usage
    :type limit_memory: str
    :param limit_cpu: Limit for CPU used
    :type limit_cpu: float | str
    :param limit_gpu: Limits for GPU used
    :type limit_gpu: int
    :param limit_ephemeral_storage: Limit for ephermeral storage
    :type limit_ephemeral_storage: float | str
    """

    __slots__ = (
        "request_memory",
        "request_cpu",
        "limit_memory",
        "limit_cpu",
        "limit_gpu",
    )

    def __init__(
        self,
        request_memory=None,
        request_cpu=None,
        request_ephemeral_storage=None,
        limit_memory=None,
        limit_cpu=None,
        limit_gpu=None,
        limit_ephemeral_storage=None,
    ):
        self.request_memory = request_memory
        self.request_cpu = request_cpu
        self.request_ephemeral_storage = request_ephemeral_storage
        self.limit_memory = limit_memory
        self.limit_cpu = limit_cpu
        self.limit_gpu = limit_gpu
        self.limit_ephemeral_storage = limit_ephemeral_storage

    def is_empty_resource_request(self):
        """Whether resource is empty"""
        return not self.has_limits() and not self.has_requests()

    def has_limits(self):
        """Whether resource has limits"""
        return (
            self.limit_cpu is not None
            or self.limit_memory is not None
            or self.limit_gpu is not None
            or self.limit_ephemeral_storage is not None
        )

    def has_requests(self):
        """Whether resource has requests"""
        return (
            self.request_cpu is not None
            or self.request_memory is not None
            or self.request_ephemeral_storage is not None
        )

    def to_k8s_client_obj(self) -> k8s.V1ResourceRequirements:
        """Converts to k8s client object"""
        return k8s.V1ResourceRequirements(
            limits={
                "cpu": self.limit_cpu,
                "memory": self.limit_memory,
                "nvidia.com/gpu": self.limit_gpu,
                "ephemeral-storage": self.limit_ephemeral_storage,
            },
            requests={
                "cpu": self.request_cpu,
                "memory": self.request_memory,
                "ephemeral-storage": self.request_ephemeral_storage,
            },
        )

    def attach_to_pod(self, pod: k8s.V1Pod) -> k8s.V1Pod:
        """Attaches to pod"""
        cp_pod = copy.deepcopy(pod)
        resources = self.to_k8s_client_obj()
        cp_pod.spec.containers[0].resources = resources
        return cp_pod


# --

# -- Volume Mount


class VolumeMount(K8SModel):
    """
    Initialize a Kubernetes Volume Mount. Used to mount pod level volumes to
    running container.
    :param name: the name of the volume mount
    :type name: str
    :param mount_path:
    :type mount_path: str
    :param sub_path: subpath within the volume mount
    :type sub_path: str
    :param read_only: whether to access pod with read-only mode
    :type read_only: bool
    """

    def __init__(self, name, mount_path, sub_path, read_only):
        self.name = name
        self.mount_path = mount_path
        self.sub_path = sub_path
        self.read_only = read_only

    def to_k8s_client_obj(self) -> k8s.V1VolumeMount:
        """
        Converts to k8s object.
        :return Volume Mount k8s object
        """
        return k8s.V1VolumeMount(
            name=self.name,
            mount_path=self.mount_path,
            sub_path=self.sub_path,
            read_only=self.read_only,
        )

    def attach_to_pod(self, pod: k8s.V1Pod) -> k8s.V1Pod:
        """
        Attaches to pod
        :return Copy of the Pod object
        """
        cp_pod = copy.deepcopy(pod)
        volume_mount = self.to_k8s_client_obj()
        cp_pod.spec.containers[0].volume_mounts = (
            pod.spec.containers[0].volume_mounts or []
        )
        cp_pod.spec.containers[0].volume_mounts.append(volume_mount)
        return cp_pod


# -- Volume


class Volume(K8SModel):
    """
    Adds Kubernetes Volume to pod. allows pod to access features like ConfigMaps
    and Persistent Volumes
    :param name: the name of the volume mount
    :type name: str
    :param configs: dictionary of any features needed for volume.
        We purposely keep this vague since there are multiple volume types with changing
        configs.
    :type configs: dict
    """

    def __init__(self, name, configs):
        self.name = name
        self.configs = configs

    def to_k8s_client_obj(self) -> Dict[str, str]:
        """Converts to k8s object"""
        return {"name": self.name, **self.configs}

    def attach_to_pod(self, pod: k8s.V1Pod) -> k8s.V1Pod:
        cp_pod = copy.deepcopy(pod)
        volume = self.to_k8s_client_obj()
        cp_pod.spec.volumes = pod.spec.volumes or []
        cp_pod.spec.volumes.append(volume)
        return cp_pod


# -- pod_generator

MAX_POD_ID_LEN = 253

MAX_LABEL_LEN = 63


class PodDefaults:
    """
    Static defaults for Pods
    """

    XCOM_MOUNT_PATH = "/airflow/xcom"
    SIDECAR_CONTAINER_NAME = "airflow-xcom-sidecar"
    XCOM_CMD = 'trap "exit 0" INT; while true; do sleep 30; done;'
    VOLUME_MOUNT = k8s.V1VolumeMount(name="xcom", mount_path=XCOM_MOUNT_PATH)
    VOLUME = k8s.V1Volume(name="xcom", empty_dir=k8s.V1EmptyDirVolumeSource())
    SIDECAR_CONTAINER = k8s.V1Container(
        name=SIDECAR_CONTAINER_NAME,
        command=["sh", "-c", XCOM_CMD],
        image="alpine",
        volume_mounts=[VOLUME_MOUNT],
        resources=k8s.V1ResourceRequirements(requests={"cpu": "1m",}),
    )


def make_safe_label_value(string):
    """
    Valid label values must be 63 characters or less and must be empty or begin and
    end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_),
    dots (.), and alphanumerics between.

    If the label value is greater than 63 chars once made safe, or differs in any
    way from the original value sent to this function, then we need to truncate to
    53 chars, and append it with a unique hash.
    """
    safe_label = re.sub(r"^[^a-z0-9A-Z]*|[^a-zA-Z0-9_\-\.]|[^a-z0-9A-Z]*$", "", string)

    if len(safe_label) > MAX_LABEL_LEN or string != safe_label:
        safe_hash = hashlib.md5(string.encode()).hexdigest()[:9]
        safe_label = safe_label[: MAX_LABEL_LEN - len(safe_hash) - 1] + "-" + safe_hash

    return safe_label


class PodGenerator:
    """
    Contains Kubernetes Airflow Worker configuration logic

    Represents a kubernetes pod and manages execution of a single pod.
    Any configuration that is container specific gets applied to
    the first container in the list of containers.

    :param image: The docker image
    :type image: Optional[str]
    :param name: name in the metadata section (not the container name)
    :type name: Optional[str]
    :param namespace: pod namespace
    :type namespace: Optional[str]
    :param volume_mounts: list of kubernetes volumes mounts
    :type volume_mounts: Optional[List[Union[k8s.V1VolumeMount, dict]]]
    :param envs: A dict containing the environment variables
    :type envs: Optional[Dict[str, str]]
    :param cmds: The command to be run on the first container
    :type cmds: Optional[List[str]]
    :param args: The arguments to be run on the pod
    :type args: Optional[List[str]]
    :param labels: labels for the pod metadata
    :type labels: Optional[Dict[str, str]]
    :param node_selectors: node selectors for the pod
    :type node_selectors: Optional[Dict[str, str]]
    :param ports: list of ports. Applies to the first container.
    :type ports: Optional[List[Union[k8s.V1ContainerPort, dict]]]
    :param volumes: Volumes to be attached to the first container
    :type volumes: Optional[List[Union[k8s.V1Volume, dict]]]
    :param image_pull_policy: Specify a policy to cache or always pull an image
    :type image_pull_policy: str
    :param restart_policy: The restart policy of the pod
    :type restart_policy: str
    :param image_pull_secrets: Any image pull secrets to be given to the pod.
        If more than one secret is required, provide a comma separated list:
        secret_a,secret_b
    :type image_pull_secrets: str
    :param init_containers: A list of init containers
    :type init_containers: Optional[List[k8s.V1Container]]
    :param service_account_name: Identity for processes that run in a Pod
    :type service_account_name: Optional[str]
    :param resources: Resource requirements for the first containers
    :type resources: Optional[Union[k8s.V1ResourceRequirements, dict]]
    :param annotations: annotations for the pod
    :type annotations: Optional[Dict[str, str]]
    :param affinity: A dict containing a group of affinity scheduling rules
    :type affinity: Optional[dict]
    :param hostnetwork: If True enable host networking on the pod
    :type hostnetwork: bool
    :param tolerations: A list of kubernetes tolerations
    :type tolerations: Optional[list]
    :param security_context: A dict containing the security context for the pod
    :type security_context: Optional[Union[k8s.V1PodSecurityContext, dict]]
    :param configmaps: Any configmap refs to envfrom.
        If more than one configmap is required, provide a comma separated list
        configmap_a,configmap_b
    :type configmaps: List[str]
    :param dnspolicy: Specify a dnspolicy for the pod
    :type dnspolicy: Optional[str]
    :param schedulername: Specify a schedulername for the pod
    :type schedulername: Optional[str]
    :param pod: The fully specified pod. Mutually exclusive with `path_or_string`
    :type pod: Optional[kubernetes.client.models.V1Pod]
    :param pod_template_file: Path to YAML file. Mutually exclusive with `pod`
    :type pod_template_file: Optional[str]
    :param extract_xcom: Whether to bring up a container for xcom
    :type extract_xcom: bool
    :param priority_class_name: priority class name for the launched Pod
    :type priority_class_name: str
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        image: Optional[str] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        volume_mounts: Optional[List[Union[k8s.V1VolumeMount, dict]]] = None,
        envs: Optional[Dict[str, str]] = None,
        cmds: Optional[List[str]] = None,
        args: Optional[List[str]] = None,
        labels: Optional[Dict[str, str]] = None,
        node_selectors: Optional[Dict[str, str]] = None,
        ports: Optional[List[Union[k8s.V1ContainerPort, dict]]] = None,
        volumes: Optional[List[Union[k8s.V1Volume, dict]]] = None,
        image_pull_policy: Optional[str] = None,
        restart_policy: Optional[str] = None,
        image_pull_secrets: Optional[str] = None,
        init_containers: Optional[List[k8s.V1Container]] = None,
        service_account_name: Optional[str] = None,
        resources: Optional[Union[k8s.V1ResourceRequirements, dict]] = None,
        annotations: Optional[Dict[str, str]] = None,
        affinity: Optional[dict] = None,
        hostnetwork: bool = False,
        tolerations: Optional[list] = None,
        security_context: Optional[Union[k8s.V1PodSecurityContext, dict]] = None,
        configmaps: Optional[List[str]] = None,
        dnspolicy: Optional[str] = None,
        schedulername: Optional[str] = None,
        pod: Optional[k8s.V1Pod] = None,
        pod_template_file: Optional[str] = None,
        extract_xcom: bool = False,
        priority_class_name: Optional[str] = None,
    ):
        self.validate_pod_generator_args(locals())

        if pod_template_file:
            self.ud_pod = self.deserialize_model_file(pod_template_file)
        else:
            self.ud_pod = pod

        self.pod = k8s.V1Pod()
        self.pod.api_version = "v1"
        self.pod.kind = "Pod"

        # Pod Metadata
        self.metadata = k8s.V1ObjectMeta()
        self.metadata.labels = labels
        self.metadata.name = name
        self.metadata.namespace = namespace
        self.metadata.annotations = annotations

        # Pod Container
        self.container = k8s.V1Container(name="base")
        self.container.image = image
        self.container.env = []

        if envs:
            if isinstance(envs, dict):
                for key, val in envs.items():
                    self.container.env.append(k8s.V1EnvVar(name=key, value=val))
            elif isinstance(envs, list):
                self.container.env.extend(envs)

        configmaps = configmaps or []
        self.container.env_from = []
        for configmap in configmaps:
            self.container.env_from.append(
                k8s.V1EnvFromSource(
                    config_map_ref=k8s.V1ConfigMapEnvSource(name=configmap)
                )
            )

        self.container.command = cmds or []
        self.container.args = args or []
        self.container.image_pull_policy = image_pull_policy
        self.container.ports = ports or []
        self.container.resources = resources
        self.container.volume_mounts = volume_mounts or []

        # Pod Spec
        self.spec = k8s.V1PodSpec(containers=[])
        self.spec.security_context = security_context
        self.spec.tolerations = tolerations
        self.spec.dns_policy = dnspolicy
        self.spec.scheduler_name = schedulername
        self.spec.host_network = hostnetwork
        self.spec.affinity = affinity
        self.spec.service_account_name = service_account_name
        self.spec.init_containers = init_containers
        self.spec.volumes = volumes or []
        self.spec.node_selector = node_selectors
        self.spec.restart_policy = restart_policy
        self.spec.priority_class_name = priority_class_name

        self.spec.image_pull_secrets = []

        if image_pull_secrets:
            for image_pull_secret in image_pull_secrets.split(","):
                self.spec.image_pull_secrets.append(
                    k8s.V1LocalObjectReference(name=image_pull_secret)
                )

        # Attach sidecar
        self.extract_xcom = extract_xcom

    def gen_pod(self) -> k8s.V1Pod:
        """Generates pod"""
        result = self.ud_pod

        if result is None:
            result = self.pod
            result.spec = self.spec
            result.metadata = self.metadata
            result.spec.containers = [self.container]

        result.metadata.name = self.make_unique_pod_id(result.metadata.name)

        if self.extract_xcom:
            result = self.add_sidecar(result)

        return result

    @staticmethod
    def add_sidecar(pod: k8s.V1Pod) -> k8s.V1Pod:
        """Adds sidecar"""
        pod_cp = copy.deepcopy(pod)
        pod_cp.spec.volumes = pod.spec.volumes or []
        pod_cp.spec.volumes.insert(0, PodDefaults.VOLUME)
        pod_cp.spec.containers[0].volume_mounts = (
            pod_cp.spec.containers[0].volume_mounts or []
        )
        pod_cp.spec.containers[0].volume_mounts.insert(0, PodDefaults.VOLUME_MOUNT)
        pod_cp.spec.containers.append(PodDefaults.SIDECAR_CONTAINER)

        return pod_cp

    @staticmethod
    def from_obj(obj) -> Optional[k8s.V1Pod]:
        """Converts to pod from obj"""
        if obj is None:
            return None

        if isinstance(obj, PodGenerator):
            return obj.gen_pod()

        if not isinstance(obj, dict):
            raise TypeError(
                "Cannot convert a non-dictionary or non-PodGenerator "
                "object into a KubernetesExecutorConfig"
            )

        # We do not want to extract constant here from ExecutorLoader because it is just
        # A name in dictionary rather than executor selection mechanism and it causes cyclic import
        namespaced = obj.get("KubernetesExecutor", {})

        if not namespaced:
            return None

        resources = namespaced.get("resources")

        if resources is None:
            requests = {
                "cpu": namespaced.get("request_cpu"),
                "memory": namespaced.get("request_memory"),
                "ephemeral-storage": namespaced.get("ephemeral-storage"),
            }
            limits = {
                "cpu": namespaced.get("limit_cpu"),
                "memory": namespaced.get("limit_memory"),
                "ephemeral-storage": namespaced.get("ephemeral-storage"),
            }
            all_resources = list(requests.values()) + list(limits.values())
            if all(r is None for r in all_resources):
                resources = None
            else:
                resources = k8s.V1ResourceRequirements(requests=requests, limits=limits)
        namespaced["resources"] = resources
        return PodGenerator(**namespaced).gen_pod()

    @staticmethod
    def reconcile_pods(
        base_pod: k8s.V1Pod, client_pod: Optional[k8s.V1Pod]
    ) -> k8s.V1Pod:
        """
        :param base_pod: has the base attributes which are overwritten if they exist
            in the client pod and remain if they do not exist in the client_pod
        :type base_pod: k8s.V1Pod
        :param client_pod: the pod that the client wants to create.
        :type client_pod: k8s.V1Pod
        :return: the merged pods

        This can't be done recursively as certain fields some overwritten, and some concatenated.
        """
        if client_pod is None:
            return base_pod

        client_pod_cp = copy.deepcopy(client_pod)
        client_pod_cp.spec = PodGenerator.reconcile_specs(
            base_pod.spec, client_pod_cp.spec
        )

        client_pod_cp.metadata = merge_objects(
            base_pod.metadata, client_pod_cp.metadata
        )
        client_pod_cp = merge_objects(base_pod, client_pod_cp)

        return client_pod_cp

    @staticmethod
    def reconcile_specs(
        base_spec: Optional[k8s.V1PodSpec], client_spec: Optional[k8s.V1PodSpec]
    ) -> Optional[k8s.V1PodSpec]:
        """
        :param base_spec: has the base attributes which are overwritten if they exist
            in the client_spec and remain if they do not exist in the client_spec
        :type base_spec: k8s.V1PodSpec
        :param client_spec: the spec that the client wants to create.
        :type client_spec: k8s.V1PodSpec
        :return: the merged specs
        """
        if base_spec and not client_spec:
            return base_spec
        if not base_spec and client_spec:
            return client_spec
        elif client_spec and base_spec:
            client_spec.containers = PodGenerator.reconcile_containers(
                base_spec.containers, client_spec.containers
            )
            merged_spec = extend_object_field(base_spec, client_spec, "volumes")
            return merge_objects(base_spec, merged_spec)

        return None

    @staticmethod
    def reconcile_containers(
        base_containers: List[k8s.V1Container], client_containers: List[k8s.V1Container]
    ) -> List[k8s.V1Container]:
        """
        :param base_containers: has the base attributes which are overwritten if they exist
            in the client_containers and remain if they do not exist in the client_containers
        :type base_containers: List[k8s.V1Container]
        :param client_containers: the containers that the client wants to create.
        :type client_containers: List[k8s.V1Container]
        :return: the merged containers

        The runs recursively over the list of containers.
        """
        if not base_containers:
            return client_containers
        if not client_containers:
            return base_containers

        client_container = client_containers[0]
        base_container = base_containers[0]
        client_container = extend_object_field(
            base_container, client_container, "volume_mounts"
        )
        client_container = extend_object_field(base_container, client_container, "env")
        client_container = extend_object_field(
            base_container, client_container, "env_from"
        )
        client_container = extend_object_field(
            base_container, client_container, "ports"
        )
        client_container = extend_object_field(
            base_container, client_container, "volume_devices"
        )
        client_container = merge_objects(base_container, client_container)

        return [client_container] + PodGenerator.reconcile_containers(
            base_containers[1:], client_containers[1:]
        )

    @staticmethod
    def construct_pod(
        dag_id: str,
        task_id: str,
        pod_id: str,
        try_number: int,
        date: str,
        command: List[str],
        kube_executor_config: Optional[k8s.V1Pod],
        worker_config: k8s.V1Pod,
        namespace: str,
        worker_uuid: str,
    ) -> k8s.V1Pod:
        """
        Construct a pod by gathering and consolidating the configuration from 3 places:
            - airflow.cfg
            - executor_config
            - dynamic arguments
        """
        dynamic_pod = PodGenerator(
            namespace=namespace,
            labels={
                "airflow-worker": worker_uuid,
                "dag_id": dag_id,
                "task_id": task_id,
                "execution_date": date,
                "try_number": str(try_number),
                "airflow_version": airflow_version.replace("+", "-"),
                "kubernetes_executor": "True",
            },
            cmds=command,
            name=pod_id,
        ).gen_pod()

        # Reconcile the pods starting with the first chronologically,
        # Pod from the airflow.cfg -> Pod from executor_config arg -> Pod from the K8s executor
        pod_list = [worker_config, kube_executor_config, dynamic_pod]

        return reduce(PodGenerator.reconcile_pods, pod_list)

    @staticmethod
    def deserialize_model_file(path: str) -> k8s.V1Pod:
        """
        :param path: Path to the file
        :return: a kubernetes.client.models.V1Pod

        Unfortunately we need access to the private method
        ``_ApiClient__deserialize_model`` from the kubernetes client.
        This issue is tracked here; https://github.com/kubernetes-client/python/issues/977.
        """
        api_client = ApiClient()
        if os.path.exists(path):
            with open(path) as stream:
                pod = yaml.safe_load(stream)
        else:
            pod = yaml.safe_load(path)

        # pylint: disable=protected-access
        return api_client._ApiClient__deserialize_model(pod, k8s.V1Pod)

    @staticmethod
    def make_unique_pod_id(dag_id):
        """
        Kubernetes pod names must be <= 253 chars and must pass the following regex for
        validation
        ``^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$``

        :param dag_id: a dag_id with only alphanumeric characters
        :return: ``str`` valid Pod name of appropriate length
        """
        if not dag_id:
            return None

        safe_uuid = uuid.uuid4().hex
        safe_pod_id = dag_id[: MAX_POD_ID_LEN - len(safe_uuid) - 1] + "-" + safe_uuid

        return safe_pod_id

    @staticmethod
    def validate_pod_generator_args(given_args):
        """
        :param given_args: The arguments passed to the PodGenerator constructor.
        :type given_args: dict
        :return: None

        Validate that if `pod` or `pod_template_file` are set that the user is not attempting
        to configure the pod with the other arguments.
        """
        pod_args = list(inspect.signature(PodGenerator).parameters.items())

        def predicate(k, v):
            """
            :param k: an arg to PodGenerator
            :type k: string
            :param v: the parameter of the given arg
            :type v: inspect.Parameter
            :return: bool

            returns True if the PodGenerator argument has no default arguments
            or the default argument is None, and it is not one of the listed field
            in `non_empty_fields`.
            """
            non_empty_fields = {
                "pod",
                "pod_template_file",
                "extract_xcom",
                "service_account_name",
                "image_pull_policy",
                "restart_policy",
            }

            return (
                v.default is None or v.default is v.empty
            ) and k not in non_empty_fields

        args_without_defaults = {
            k: given_args[k] for k, v in pod_args if predicate(k, v) and given_args[k]
        }

        if given_args["pod"] and given_args["pod_template_file"]:
            raise AirflowConfigException(
                "Cannot pass both `pod` and `pod_template_file` arguments"
            )
        if args_without_defaults and (
            given_args["pod"] or given_args["pod_template_file"]
        ):
            raise AirflowConfigException(
                "Cannot configure pod and pass either `pod` or `pod_template_file`. Fields {} passed.".format(
                    list(args_without_defaults.keys())
                )
            )


def merge_objects(base_obj, client_obj):
    """
    :param base_obj: has the base attributes which are overwritten if they exist
        in the client_obj and remain if they do not exist in the client_obj
    :param client_obj: the object that the client wants to create.
    :return: the merged objects
    """
    if not base_obj:
        return client_obj
    if not client_obj:
        return base_obj

    client_obj_cp = copy.deepcopy(client_obj)

    for base_key in base_obj.to_dict().keys():
        base_val = getattr(base_obj, base_key, None)
        if not getattr(client_obj, base_key, None) and base_val:
            setattr(client_obj_cp, base_key, base_val)
    return client_obj_cp


def extend_object_field(base_obj, client_obj, field_name):
    """
    :param base_obj: an object which has a property `field_name` that is a list
    :param client_obj: an object which has a property `field_name` that is a list.
        A copy of this object is returned with `field_name` modified
    :param field_name: the name of the list field
    :type field_name: str
    :return: the client_obj with the property `field_name` being the two properties appended
    """
    client_obj_cp = copy.deepcopy(client_obj)
    base_obj_field = getattr(base_obj, field_name, None)
    client_obj_field = getattr(client_obj, field_name, None)

    if (not isinstance(base_obj_field, list) and base_obj_field is not None) or (
        not isinstance(client_obj_field, list) and client_obj_field is not None
    ):
        raise ValueError("The chosen field must be a list.")

    if not base_obj_field:
        return client_obj_cp
    if not client_obj_field:
        setattr(client_obj_cp, field_name, base_obj_field)
        return client_obj_cp

    appended_fields = base_obj_field + client_obj_field
    setattr(client_obj_cp, field_name, appended_fields)
    return client_obj_cp


# -- KubernetesPodOperator


class KubernetesPodOperator(
    BaseOperator
):  # pylint: disable=too-many-instance-attributes
    """
    Execute a task in a Kubernetes Pod

    .. note::
        If you use `Google Kubernetes Engine <https://cloud.google.com/kubernetes-engine/>`__, use
        :class:`~airflow.providers.google.cloud.operators.kubernetes_engine.GKEPodOperator`, which
        simplifies the authorization process.

    :param namespace: the namespace to run within kubernetes.
    :type namespace: str
    :param image: Docker image you wish to launch. Defaults to hub.docker.com,
        but fully qualified URLS will point to custom repositories.
    :type image: str
    :param name: name of the pod in which the task will run, will be used (plus a random
        suffix) to generate a pod id (DNS-1123 subdomain, containing only [a-z0-9.-]).
    :type name: str
    :param cmds: entrypoint of the container. (templated)
        The docker images's entrypoint is used if this is not provided.
    :type cmds: list[str]
    :param arguments: arguments of the entrypoint. (templated)
        The docker image's CMD is used if this is not provided.
    :type arguments: list[str]
    :param ports: ports for launched pod.
    :type ports: list[airflow.kubernetes.pod.Port]
    :param volume_mounts: volumeMounts for launched pod.
    :type volume_mounts: list[airflow.kubernetes.volume_mount.VolumeMount]
    :param volumes: volumes for launched pod. Includes ConfigMaps and PersistentVolumes.
    :type volumes: list[airflow.kubernetes.volume.Volume]
    :param env_vars: Environment variables initialized in the container. (templated)
    :type env_vars: dict
    :param secrets: Kubernetes secrets to inject in the container.
        They can be exposed as environment vars or files in a volume.
    :type secrets: list[airflow.kubernetes.secret.Secret]
    :param in_cluster: run kubernetes client with in_cluster configuration.
    :type in_cluster: bool
    :param cluster_context: context that points to kubernetes cluster.
        Ignored when in_cluster is True. If None, current-context is used.
    :type cluster_context: str
    :param reattach_on_restart: if the scheduler dies while the pod is running, reattach and monitor
    :type reattach_on_restart: bool
    :param labels: labels to apply to the Pod.
    :type labels: dict
    :param startup_timeout_seconds: timeout in seconds to startup the pod.
    :type startup_timeout_seconds: int
    :param get_logs: get the stdout of the container as logs of the tasks.
    :type get_logs: bool
    :param image_pull_policy: Specify a policy to cache or always pull an image.
    :type image_pull_policy: str
    :param annotations: non-identifying metadata you can attach to the Pod.
        Can be a large range of data, and can include characters
        that are not permitted by labels.
    :type annotations: dict
    :param resources: A dict containing resources requests and limits.
        Possible keys are request_memory, request_cpu, limit_memory, limit_cpu,
        and limit_gpu, which will be used to generate airflow.kubernetes.pod.Resources.
        See also kubernetes.io/docs/concepts/configuration/manage-compute-resources-container
    :type resources: dict
    :param affinity: A dict containing a group of affinity scheduling rules.
    :type affinity: dict
    :param config_file: The path to the Kubernetes config file. (templated)
        If not specified, default value is ``~/.kube/config``
    :type config_file: str
    :param node_selectors: A dict containing a group of scheduling rules.
    :type node_selectors: dict
    :param image_pull_secrets: Any image pull secrets to be given to the pod.
        If more than one secret is required, provide a
        comma separated list: secret_a,secret_b
    :type image_pull_secrets: str
    :param service_account_name: Name of the service account
    :type service_account_name: str
    :param is_delete_operator_pod: What to do when the pod reaches its final
        state, or the execution is interrupted.
        If False (default): do nothing, If True: delete the pod
    :type is_delete_operator_pod: bool
    :param hostnetwork: If True enable host networking on the pod.
    :type hostnetwork: bool
    :param tolerations: A list of kubernetes tolerations.
    :type tolerations: list tolerations
    :param configmaps: A list of configmap names objects that we
        want mount as env variables.
    :type configmaps: list[str]
    :param security_context: security options the pod should run with (PodSecurityContext).
    :type security_context: dict
    :param pod_runtime_info_envs: environment variables about
        pod runtime information (ip, namespace, nodeName, podName).
    :type pod_runtime_info_envs: list[airflow.kubernetes.pod_runtime_info_env.PodRuntimeInfoEnv]
    :param dnspolicy: dnspolicy for the pod.
    :type dnspolicy: str
    :param schedulername: Specify a schedulername for the pod
    :type schedulername: str
    :param full_pod_spec: The complete podSpec
    :type full_pod_spec: kubernetes.client.models.V1Pod
    :param init_containers: init container for the launched Pod
    :type init_containers: list[kubernetes.client.models.V1Container]
    :param log_events_on_failure: Log the pod's events if a failure occurs
    :type log_events_on_failure: bool
    :param do_xcom_push: If True, the content of the file
        /airflow/xcom/return.json in the container will also be pushed to an
        XCom when the container completes.
    :type do_xcom_push: bool
    :param pod_template_file: path to pod template file
    :type pod_template_file: str
    :param priority_class_name: priority class name for the launched Pod
    :type priority_class_name: str
    """

    template_fields = (
        "cmds",
        "arguments",
        "env_vars",
        "config_file",
        "pod_template_file",
    )

    @apply_defaults
    def __init__(
        self,  # pylint: disable=too-many-arguments,too-many-locals
        namespace: Optional[str] = None,
        image: Optional[str] = None,
        name: Optional[str] = None,
        cmds: Optional[List[str]] = None,
        arguments: Optional[List[str]] = None,
        ports: Optional[List[Port]] = None,
        volume_mounts: Optional[List[VolumeMount]] = None,
        volumes: Optional[List[Volume]] = None,
        env_vars: Optional[Dict] = None,
        secrets: Optional[List[Secret]] = None,
        in_cluster: Optional[bool] = None,
        cluster_context: Optional[str] = None,
        labels: Optional[Dict] = None,
        reattach_on_restart: bool = True,
        startup_timeout_seconds: int = 120,
        get_logs: bool = True,
        image_pull_policy: str = "IfNotPresent",
        annotations: Optional[Dict] = None,
        resources: Optional[Dict] = None,
        affinity: Optional[Dict] = None,
        config_file: Optional[str] = None,
        node_selectors: Optional[Dict] = None,
        image_pull_secrets: Optional[str] = None,
        service_account_name: str = "default",
        is_delete_operator_pod: bool = False,
        hostnetwork: bool = False,
        tolerations: Optional[List] = None,
        configmaps: Optional[List] = None,
        security_context: Optional[Dict] = None,
        pod_runtime_info_envs: Optional[List[PodRuntimeInfoEnv]] = None,
        dnspolicy: Optional[str] = None,
        schedulername: Optional[str] = None,
        full_pod_spec: Optional[k8s.V1Pod] = None,
        init_containers: Optional[List[k8s.V1Container]] = None,
        log_events_on_failure: bool = False,
        do_xcom_push: bool = False,
        pod_template_file: Optional[str] = None,
        priority_class_name: Optional[str] = None,
        *args,
        **kwargs
    ):
        if kwargs.get("xcom_push") is not None:
            raise AirflowException(
                "'xcom_push' was deprecated, use 'do_xcom_push' instead"
            )
        super().__init__(*args, resources=None, **kwargs)

        self.pod = None
        self.do_xcom_push = do_xcom_push
        self.image = image
        self.namespace = namespace
        self.cmds = cmds or []
        self.arguments = arguments or []
        self.labels = labels or {}
        self.startup_timeout_seconds = startup_timeout_seconds
        self.env_vars = env_vars or {}
        self.ports = ports or []
        self.volume_mounts = volume_mounts or []
        self.volumes = volumes or []
        self.secrets = secrets or []
        self.in_cluster = in_cluster
        self.cluster_context = cluster_context
        self.reattach_on_restart = reattach_on_restart
        self.get_logs = get_logs
        self.image_pull_policy = image_pull_policy
        self.node_selectors = node_selectors or {}
        self.annotations = annotations or {}
        self.affinity = affinity or {}
        self.resources = self._set_resources(resources)
        self.config_file = config_file
        self.image_pull_secrets = image_pull_secrets
        self.service_account_name = service_account_name
        self.is_delete_operator_pod = is_delete_operator_pod
        self.hostnetwork = hostnetwork
        self.tolerations = tolerations or []
        self.configmaps = configmaps or []
        self.security_context = security_context or {}
        self.pod_runtime_info_envs = pod_runtime_info_envs or []
        self.dnspolicy = dnspolicy
        self.schedulername = schedulername
        self.full_pod_spec = full_pod_spec
        self.init_containers = init_containers or []
        self.log_events_on_failure = log_events_on_failure
        self.priority_class_name = priority_class_name
        self.pod_template_file = pod_template_file
        self.name = self._set_name(name)

    @staticmethod
    def create_labels_for_pod(context) -> dict:
        """
        Generate labels for the pod to track the pod in case of Operator crash

        :param context: task context provided by airflow DAG
        :return: dict
        """
        labels = {
            "dag_id": context["dag"].dag_id,
            "task_id": context["task"].task_id,
            "execution_date": context["ts"],
            "try_number": context["ti"].try_number,
        }
        # In the case of sub dags this is just useful
        if context["dag"].is_subdag:
            labels["parent_dag_id"] = context["dag"].parent_dag.dag_id
        # Ensure that label is valid for Kube,
        # and if not truncate/remove invalid chars and replace with short hash.
        for label_id, label in labels.items():
            safe_label = make_safe_label_value(str(label))
            labels[label_id] = safe_label
        return labels

    def execute(self, context) -> Optional[str]:
        try:
            if self.in_cluster is not None:
                client = get_kube_client(
                    in_cluster=self.in_cluster,
                    cluster_context=self.cluster_context,
                    config_file=self.config_file,
                )
            else:
                client = get_kube_client(
                    cluster_context=self.cluster_context, config_file=self.config_file
                )

            # Add combination of labels to uniquely identify a running pod
            labels = self.create_labels_for_pod(context)

            label_selector = self._get_pod_identifying_label_string(labels)

            pod_list = client.list_namespaced_pod(
                self.namespace, label_selector=label_selector
            )

            if len(pod_list.items) > 1:
                raise AirflowException(
                    "More than one pod running with labels: "
                    "{label_selector}".format(label_selector=label_selector)
                )

            launcher = PodLauncher(kube_client=client, extract_xcom=self.do_xcom_push)

            if (
                len(pod_list.items) == 1
                and self._try_numbers_do_not_match(context, pod_list.items[0])
                and self.reattach_on_restart
            ):
                self.log.info(
                    "found a running pod with labels %s but a different try_number"
                    "Will attach to this pod and monitor instead of starting new one",
                    labels,
                )
                final_state, _, result = self.create_new_pod_for_operator(
                    labels, launcher
                )
            elif len(pod_list.items) == 1:
                self.log.info(
                    "found a running pod with labels %s."
                    "Will monitor this pod instead of starting new one",
                    labels,
                )
                final_state, result = self.monitor_launched_pod(launcher, pod_list[0])
            else:
                final_state, _, result = self.create_new_pod_for_operator(
                    labels, launcher
                )
            if final_state != State.SUCCESS:
                raise AirflowException(
                    "Pod returned a failure: {state}".format(state=final_state)
                )
            return result
        except AirflowException as ex:
            raise AirflowException("Pod Launching failed: {error}".format(error=ex))

    @staticmethod
    def _get_pod_identifying_label_string(labels):
        filtered_labels = {
            label_id: label
            for label_id, label in labels.items()
            if label_id != "try_number"
        }
        return ",".join(
            [
                label_id + "=" + label
                for label_id, label in sorted(filtered_labels.items())
            ]
        )

    @staticmethod
    def _try_numbers_do_not_match(context, pod):
        return pod.metadata.labels["try_number"] != context["ti"].try_number

    @staticmethod
    def _set_resources(resources):
        if not resources:
            return []
        return [Resources(**resources)]

    def _set_name(self, name):
        if self.pod_template_file or self.full_pod_spec:
            return None
        validate_key(name, max_length=220)
        return re.sub(r"[^a-z0-9.-]+", "-", name.lower())

    def create_new_pod_for_operator(
        self, labels, launcher
    ) -> Tuple[State, k8s.V1Pod, Optional[str]]:
        """
        Creates a new pod and monitors for duration of task

        @param labels: labels used to track pod
        @param launcher: pod launcher that will manage launching and monitoring pods
        @return:
        """
        if not (self.full_pod_spec or self.pod_template_file):
            # Add Airflow Version to the label
            # And a label to identify that pod is launched by KubernetesPodOperator
            self.labels.update(
                {
                    "airflow_version": airflow_version.replace("+", "-"),
                    "kubernetes_pod_operator": "True",
                }
            )
            self.labels.update(labels)
        pod = PodGenerator(
            image=self.image,
            namespace=self.namespace,
            cmds=self.cmds,
            args=self.arguments,
            labels=self.labels,
            name=self.name,
            envs=self.env_vars,
            extract_xcom=self.do_xcom_push,
            image_pull_policy=self.image_pull_policy,
            node_selectors=self.node_selectors,
            annotations=self.annotations,
            affinity=self.affinity,
            image_pull_secrets=self.image_pull_secrets,
            service_account_name=self.service_account_name,
            hostnetwork=self.hostnetwork,
            tolerations=self.tolerations,
            configmaps=self.configmaps,
            security_context=self.security_context,
            dnspolicy=self.dnspolicy,
            schedulername=self.schedulername,
            init_containers=self.init_containers,
            restart_policy="Never",
            priority_class_name=self.priority_class_name,
            pod_template_file=self.pod_template_file,
            pod=self.full_pod_spec,
        ).gen_pod()

        # noinspection PyTypeChecker
        pod = append_to_pod(
            pod,
            self.pod_runtime_info_envs
            + self.ports
            + self.resources
            + self.secrets
            + self.volumes
            + self.volume_mounts,
        )

        self.pod = pod

        try:
            launcher.start_pod(pod, startup_timeout=self.startup_timeout_seconds)
            final_state, result = launcher.monitor_pod(pod=pod, get_logs=self.get_logs)
        except AirflowException:
            if self.log_events_on_failure:
                for event in launcher.read_pod_events(pod).items:
                    self.log.error("Pod Event: %s - %s", event.reason, event.message)
            raise
        finally:
            if self.is_delete_operator_pod:
                launcher.delete_pod(pod)
        return final_state, pod, result

    def monitor_launched_pod(self, launcher, pod) -> Tuple[State, Optional[str]]:
        """
        Montitors a pod to completion that was created by a previous KubernetesPodOperator

        @param launcher: pod launcher that will manage launching and monitoring pods
        :param pod: podspec used to find pod using k8s API
        :return:
        """
        try:
            (final_state, result) = launcher.monitor_pod(pod, get_logs=self.get_logs)
        finally:
            if self.is_delete_operator_pod:
                launcher.delete_pod(pod)
        if final_state != State.SUCCESS:
            if self.log_events_on_failure:
                for event in launcher.read_pod_events(pod).items:
                    self.log.error("Pod Event: %s - %s", event.reason, event.message)
            raise AirflowException(
                "Pod returned a failure: {state}".format(state=final_state)
            )
        return final_state, result
