"""
    Great Expectations Operator based on K8s, runs GE as a pod

    Note that this Operator uses a "patched" version of the KubernetesPodOperator
    which includes many of the recent (post 1.10.10) additions to the KubernetesPodOperator features
    notably the possibility to pass init_containers

    ^ these features should be released in Airflow 2.0 or on the next minor release, in which
    case the "patched" KubernetesPodOperator can be removed
"""
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import kubernetes.client.models as k8s
from earnest.airflow_plugin.operators.kubernetes_pod_operator import (
    KubernetesPodOperator,
    Volume,
    VolumeMount,
)
from jinja2 import Template


# From https://gist.github.com/sekimura/2678967#file-text_strip_margin-py-L3
def strip_margin(text):
    return re.sub("\n[ \t]*\|", "\n", text)


@dataclass
class GEBatchKwargs:
    """
        Class to represent GE Batch Kwargs, in the current state
        it is not flexible enough (batch kwargs can take a table instead of a query for example)
    """

    query: str
    datasource: str
    data_asset_name: str
    schema: str
    snowflake_transient_table: Optional[str] = None

    def to_yaml(self):
        return strip_margin(
            f"""query: {self.query}
               |datasource: {self.datasource}
               |data_asset_name: {self.data_asset_name}
               |schema: {self.schema}"""
            + (
                f"""
               |snowflake_transient_table: {self.snowflake_transient_table}"""
                if self.snowflake_transient_table
                else ""
            )
        )


@dataclass
class GEBatch:
    """
        Represents a GE Batch, which runs against a list of expectation suites
    """

    batch_kwargs: GEBatchKwargs
    expectation_suite_names: List[str]

    def to_yaml(self):
        return Template(
            strip_margin(
                """- batch_kwargs:
                  |{{ batch_kwargs.to_yaml() | indent(4, True) }}
                  |{{ 'expectation_suite_names:' | indent(2, True) }}
                  |{%- for suite in expectation_suite_names %}
                  |{{ ('- ' + suite) | indent(2, True) }}
                  |{%- endfor -%}"""
            )
        ).render(
            expectation_suite_names=self.expectation_suite_names,
            batch_kwargs=self.batch_kwargs,
        )


def ge_batches_to_yaml(batches: List[GEBatch]):
    """
        The "to_yaml" functions create a "GE checkpoint file", ideally the checkpoint feature
        should allow passing the information through the CLI, but it's a pretty new feature
        and it's not flexible enough for our use case yet (hence the need to template the YAML
        from the Airflow logic)
    """
    return Template(
        strip_margin(
            """batches:
              |{% for batch in batches -%}
              |{{ batch.to_yaml() }}
              |{% endfor %}"""
        )
    ).render(batches=batches)


@dataclass
class GEGitSync:
    """
        Git Sync information (in cases where the great_expectations project isn't
        built into the base image). This will be useful for us as we talked about
        having multiple GE projects potentially close the the transformation information.
        (That way, no need to maintain extra images)
    """

    ge_repo: str
    ssh_key_secret_name: str
    image: str = "k8s.gcr.io/git-sync:v3.1.6"
    branch: str = "master"


class GreatExpectationsCheckpointKubernetesPodOperator(KubernetesPodOperator):
    ui_color = "#FFC3A0"

    @staticmethod
    def _checkpoint_yaml(batches: List[GEBatch], validation_operator_name: str):
        return Template(
            strip_margin(
                """validation_operator_name: {{ validation_operator_name }}
                  |{{ batches }}"""
            )
        ).render(
            validation_operator_name=validation_operator_name,
            batches=ge_batches_to_yaml(batches),
        )

    def __init__(
        self,
        task_id: str,
        name: str,
        config_variables_secret_name: str,
        ge_project_subpath: Path,
        batches: List[GEBatch],
        validation_operator_name: str,
        config_variables_file_path: Path,
        image: str = "dmateusp/great_expectations:python-3.7-buster-ge-0.11.9",  # TODO: To be changed to the "official" repo once the core team accepts the contribution
        git_sync: Optional[GEGitSync] = None,
        extra_volumes: Optional[List[Volume]] = None,
        extra_volume_mounts: Optional[List[VolumeMount]] = None,
        **pod_kwargs,
    ):
        """Runs a GreatExpectation checkpoint through a KubernetesPodOperator

        Args:
            task_id (str): The unique task_id (DAG-level)
            name (str): The Kubernetes Pod Name (cannot contain underscores)
            config_variables_secret_name (str): The name of the Kubernetes Secret which contains the GE config variable file
            ge_project_subpath (Path): Path to the GE project from the root of the GitHub directory, or in the image (if GE project was bundled in the image)
            validation_operator_name (str): Name of the validation operator to run
            config_variables_file_path (Path): Path where the config variables file is expected (as configured in the GE project)
            image (str, optional): Image to be used (needs great_expectations installed). Defaults to "dmateusp/great_expectations:python-3.7-buster-ge-0.11.3".
            git_sync (Optional[GEGitSync], optional): Git Sync information, if it is not used then it is assumed the great_expectations project is inside the image. Defaults to None.
        """
        self.task_id = task_id
        self.name = name
        self.config_variables = config_variables_secret_name
        self.ge_project_subpath = ge_project_subpath
        self.batches = batches
        self.validation_operator_name = validation_operator_name
        self.image = image
        self.git_sync = git_sync

        init_containers = []
        git_sync_dest = Path("great_expectations")
        root_dir = Path("/usr/app/")

        if git_sync:
            init_containers.extend(
                [
                    k8s.V1Container(
                        name="git-sync",
                        image=git_sync.image,
                        volume_mounts=[
                            k8s.V1VolumeMount(
                                name="ssh-key",
                                mount_path="/etc/git-secret/ssh",
                                sub_path="ssh",
                                read_only=True,
                            ),
                            k8s.V1VolumeMount(
                                name="ssh-key",
                                mount_path="/etc/git-secret/known_hosts",
                                sub_path="known-hosts",
                                read_only=True,
                            ),
                            k8s.V1VolumeMount(
                                name="ge-project",
                                mount_path=str(root_dir),
                                read_only=False,
                            ),
                        ],
                        env=[
                            k8s.V1EnvVar(name="GIT_SYNC_REPO", value=git_sync.ge_repo),
                            k8s.V1EnvVar(name="GIT_SYNC_ROOT", value=str(root_dir),),
                            k8s.V1EnvVar(name="GIT_SYNC_SSH", value="true"),
                            k8s.V1EnvVar(name="GIT_SYNC_BRANCH", value=git_sync.branch),
                            k8s.V1EnvVar(name="GIT_SYNC_ONE_TIME", value="true"),
                            k8s.V1EnvVar(
                                name="GIT_SYNC_DEST", value=str(git_sync_dest)
                            ),
                        ],
                    ),
                ]
            )

        volume_mounts = []

        if git_sync:
            volume_mounts.extend(
                [
                    VolumeMount(
                        name="ge-project",
                        mount_path=str(root_dir / git_sync_dest),
                        sub_path=str(git_sync_dest / ge_project_subpath),
                        read_only=False,
                    ),
                ]
            )

        volumes = []

        if git_sync:
            volumes.extend(
                [
                    Volume(
                        name="ssh-key",
                        configs={
                            "secret": {"secretName": git_sync.ssh_key_secret_name}
                        },
                    ),
                    Volume(name="ge-project", configs={"emptyDir": {}}),
                ]
            )

        checkpoint_file_path = (
            root_dir / git_sync_dest / Path(f"checkpoints/{self.task_id}.yml")
        )

        config_variables_mount_path = (
            root_dir / git_sync_dest / Path(".secrets/config_variables.yml")
        )  # temp path we copy the config_variables file before copying to the target path, to avoid potential permissioning issues

        config_variables_target_path = (
            root_dir / git_sync_dest / config_variables_file_path
        )

        super(GreatExpectationsCheckpointKubernetesPodOperator, self).__init__(
            task_id=task_id,
            name=name,
            image=image,
            do_xcom_push=False,
            cmds=["bash", "-cx"],
            arguments=[
                (
                    f"mkdir -p {str(config_variables_target_path.parent)}"
                    f" && mkdir -p {str(checkpoint_file_path.parent)}"
                    f" && cp {str(config_variables_mount_path)} {str(config_variables_target_path)} "  # Copying the config variables to avoid getting permission issues from the "uncommitted" directory being created by the VolumeMount process
                    f' && printf "{self._checkpoint_yaml(batches, validation_operator_name)}" > {str(checkpoint_file_path)}'  # Template the checkpoint YAML file and give it the task_id name (it's clear the YAML checkpoint is not suitable to our use cases, need to give feedback to the GE team to allow checkpoing arguments to come from the CLI)
                    f" && great_expectations checkpoint run {task_id}"
                ),
            ],
            init_containers=init_containers,
            volume_mounts=[
                VolumeMount(
                    name="ge-config-variables",
                    mount_path=str(config_variables_mount_path),
                    sub_path="config_variables.yml",
                    read_only=False,
                ),
            ]
            + volume_mounts
            + (extra_volume_mounts or []),
            volumes=[
                Volume(
                    name="ge-config-variables",
                    configs={"secret": {"secretName": config_variables_secret_name}},
                )
            ]
            + volumes
            + (extra_volumes or []),
            security_context={"fsGroup": 1000,},  # great-expectations group
            retries=0,
            **pod_kwargs,
        )
