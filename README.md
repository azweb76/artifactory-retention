# Artifactory Retention Tools
Tools for maintaining Artifactory retention.

## Install
```bash
pip install https://github.com/azweb76/artifactory-retention [--upgrade]
```

## Usage (clean)
To delete artifacts in Artifactory.

Strategy:
* retrieve all artifacts not downloaded in the past N days
* skip N most recent artifacts. this is useful for artifacts that are in production that are being used but have not been downloaded for a while.

```bash
ART_USER=myuser artret clean --whatif --days 15 --folder 'myfolder' \
  --repo 'docker-group-local' -vvv
```

|option|type|description|
|---|---|---|
|days|int|optional. default 45. number of days to check for unused artifacts|
|folder|string (multiple)|required. folders to group by for cleaning. use '*' for all|
|skip|int|optional. default 50. number of most recent artifacts in unused list to keep|
|repo|string|required. Artifactory repository to scan|
|whatif|flag|default false. don't actually delete, show log as if deleting|
|verbose|flag (multiple)|default 0. show detailed logs|
