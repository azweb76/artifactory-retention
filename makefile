all: clean

prepare:
	docker rmi --force azweb76/artifactory-retention || echo 'Image not built yet.'

build_docker: prepare
	docker build -t azweb76/artifactory-retention .

clean: build_docker

test:
	poetry run pytest

publish:
	docker push azweb76/artifactory-retention
