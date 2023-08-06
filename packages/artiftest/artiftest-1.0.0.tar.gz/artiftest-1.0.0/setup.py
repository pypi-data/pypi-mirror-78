from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='artiftest',
    version='1.0.0',
    description='Plugin to create and access MLflow-managed artifacts on Databricks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Databricks',
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        'mlflow>=1.0.0',
    ],
    entry_points={
        "mlflow.artifact_repository": [
            "dbfs=mlflow_databricks_artifacts.store.entrypoint:dbfs_artifact_repo_factory",
        ]
    },
)
