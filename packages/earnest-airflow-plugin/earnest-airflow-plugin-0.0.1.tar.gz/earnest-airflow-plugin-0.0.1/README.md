# airflow-plugin

Operators and Hooks for Airflow

## Airflow at Earnest

We use heavily the `KubernetesPodOperator` for the following reasons:

- Keep non-scheduling logic out of the scheduler.
- Avoid locking logic inside Airflow (containers can run through other schedulers).
- Avoid accumulating python dependencies in the Airflow image.
- Align with our engineering culture (functional programming and strongly typed languages lead to more maintainable code, Haskell preferred :) ).

As such, you will find most of the Operators we share inherit from the `KubernetesPodOperator`.

## Running the tests locally

0. Install dev requirements

    ```bash
    pip install -r requirements_dev.txt
    ```

1. Run the unit tests

    ```bash
    pytest -v -m "not kubernetes"
    ```

2. Start a local kubernetes cluster through [docker-for-desktop](https://www.docker.com/products/docker-desktop) (Mac/Windows) or [minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/) (Linux)

3. Bootstrap the cluster (it'll use the `airflow` namespace)

    ```bash
    tests/resources/kubernetes/bootstrap.sh
    ```

4. Run the kubernetes tests

    ```bash
    AIRFLOW__KUBERNETES__IN_CLUSTER=False pytest -v -m "kubernetes"
    ```

## Releasing

Currently, publishing a new version of the project is a manual process:

0. Install dev requirements

    ```bash
    pip install -r requirements_dev.txt
    ```

1. Edit the `version` in [setup.cfg](setup.cfg)

2. Create a new git release:

    ```bash
    # e.g.
    git tag -a v0.0.1
    ```

    There's a simple template in [RELEASE_NOTES_TEMPLATE.md](RELEASE_NOTES_TEMPLATE.md) for a release message.

3. Push the release:

    ```bash
    git push origin v0.0.1
    ```

4. Create a source distribution:

    ```bash
    python setup.py sdist bdist_wheel
    ```

5. Upload to PyPi

    ```bash
    twine upload dist/*
    ```
