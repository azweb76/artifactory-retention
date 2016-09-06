# Artifactory Retention Tools
Tools for maintaining Artifactory retention.

## Install
```bash
pip install git+https://github.com/azweb76/artifactory-retention [--upgrade]
```

## Usage (clean)
To delete artifacts in Artifactory.

Strategy:
* retrieve all artifacts not downloaded in the past N days
* skip N most recent artifacts. this is useful for artifacts that are in production that are being used but have not been downloaded for a while.

```bash
export ART_URL='https://artifactory.mydomain.com/artifactory'
ART_USER=myuser artret --repo 'docker-group-local' clean --whatif --days 15 --folder 'myfolder'
```

|option|type|description|
|---|---|---|
|days|int|optional. default 45. number of days to check for unused artifacts|
|folder|string (multiple)|required. folders to group by for cleaning. use '*' for all|
|skip|int|optional. default 50. number of most recent artifacts in unused list to keep|
|repo|string|required. Artifactory repository to scan|
|whatif|flag|default false. don't actually delete, show log as if deleting|

## Running in Kubernetes
To run in a Kubernetes cluster, follow these steps:

* Create a cicd namespace (To use your own, make sure you update the kube-pod.yaml file with that namespace).
* Create a secret named artifactory-user in the cicd namespace with `artifactory-username` and `artifactory-password` keys containing the username/password to delete artifacts in your repo.
* Copy and modify [kube-pod.yaml](kube-pod.yaml) to include your Artifactory URL (ART_URL) and Artifactory repository (ART_REPO). Additional options can be set in this file.
* Run `kubectl create -f kube-pod.yaml`.

> NOTE: Ensure the secret and pod exist in the same namespace (default for kube-pod is cicd).
