VERSION=1.4.1

all: clean

prepare:
	docker rmi --force azweb76/artifactory-retention || echo 'Image not built yet.'

build: prepare
	docker build --platform linux/amd64 -t azweb76/artifactory-retention:$(VERSION) .

clean: build_docker

test:
	poetry run pytest

publish:
	docker push azweb76/artifactory-retention:$(VERSION)
