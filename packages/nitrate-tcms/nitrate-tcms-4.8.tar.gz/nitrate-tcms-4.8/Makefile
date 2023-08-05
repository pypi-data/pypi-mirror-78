SPECFILE=python-nitrate-tcms.spec

default: help

DIST_DIR=$(shell pwd)/dist/
DEFINE_OPTS=--define "_sourcedir $(PWD)/dist" --define "_srcrpmdir $(PWD)/dist" --define "_rpmdir $(PWD)/dist"


.PHONY: tarball
tarball:
	@python3 setup.py sdist


.PHONY: srpm
srpm:
	@rpmbuild $(DEFINE_OPTS) -bs $(SPECFILE)


.PHONY: rpm
rpm: srpm
	@rpmbuild $(DEFINE_OPTS) -ba $(SPECFILE)


.PHONY: build
build:
	python setup.py build


.PHONY: install
install:
	python setup.py install


.PHONY: flake8
flake8:
	@tox -e flake8


.PHONY: check
check:
	@tox


.PHONY: tags
tags:
	@rm -f .tags
	@ctags -R --languages=Python,Javascript --python-kinds=-im \
		--exclude=build --exclude=tcms/static/js/lib --exclude=dist --exclude=.tox -f .tags


.PHONY: etags
etags:
	@rm -f TAGS
	@ctags -R -e --languages=Python,Javascript --python-kinds=-im \
		--exclude=build --exclude=tcms/static/js/lib --exclude=dist --exclude=.tox -f TAGS

CONTAINER ?= podman
RELEASE_VERSION ?= latest
DOCKER_ORG ?= quay.io/nitrate
IMAGE_TAG = $(DOCKER_ORG)/nitrate:$(RELEASE_VERSION)

release-image:
	@$(CONTAINER) build -t $(IMAGE_TAG) -f ./docker/released/Dockerfile --build-arg version=$(RELEASE_VERSION) .

.PHONY: publish-release-image
publish-release-image:
	@if [[ -n "$(QUAY_ROBOT_USER)" ]] && [[ -n "$(QUAY_ROBOT_PASSWORD)" ]]; then \
		echo "$(QUAY_ROBOT_PASSWORD)" | $(CONTAINER) login -u "$(QUAY_ROBOT_USER)" --password-stdin quay.io; \
	else \
		$(CONTAINER) login quay.io; \
  	fi
	$(CONTAINER) push $(IMAGE_TAG)

dev-image:
	@$(CONTAINER) build -t $(IMAGE_TAG:$(RELEASE_VERSION)=dev) -f ./docker/dev/Dockerfile .

# By default, released image is pulled from remote registry.
# For the purpose of testing released image locally, execute target
# `release-image' manually before this up.
up-release-container: export IMAGE_VERSION = $(RELEASE_VERSION)
up-release-container:
	@docker-compose -f docker-compose.yml up

clear-release-container:
	@docker-compose -f docker-compose.yml rm

# Depends on dev-image
up-dev-container:
	@docker-compose -f docker-compose-dev.yml up

clear-dev-container:
	@docker-compose -f docker-compose-dev.yml rm

web-container-initconfig:
	# Make sure web is up from docker-compose.yml already
	# Database migrations
	@$(CONTAINER) exec -i -t --env DJANGO_SETTINGS_MODULE=tcms.settings.product nitrate_web_1 \
		/prodenv/bin/django-admin migrate
	# Create superuser admin
	@$(CONTAINER) exec -i -t --env DJANGO_SETTINGS_MODULE=tcms.settings.product nitrate_web_1 \
		/prodenv/bin/django-admin createsuperuser --username admin --email admin@example.com
	# Set permissions to default groups
	@$(CONTAINER) exec -i -t --env DJANGO_SETTINGS_MODULE=tcms.settings.product nitrate_web_1 \
		/prodenv/bin/django-admin setdefaultperms

# ./manage.py runserver with default SQLite database
runserver:
	@./src/manage.py runserver

runserver-mysql:
	@mysql -uroot -e "CREATE DATABASE IF NOT EXISTS nitrate CHARACTER SET utf8mb4;"
	@NITRATE_DB_ENGINE=mysql NITRATE_DB_NAME=nitrate ./src/manage.py runserver

runserver-pgsql:
	@echo "CREATE DATABASE nitrate" | psql -U postgres || true
	@NITRATE_DB_ENGINE=pgsql NITRATE_DB_NAME=nitrate NITRATE_DB_USER=postgres ./src/manage.py runserver


testbox_image_tag = $(DOCKER_ORG)/testbox

.PHONY: remove-testbox-image
remove-testbox-image:
	@if [ -n "$($(CONTAINER) images -q $(testbox_image_tag))" ]; then $(CONTAINER) rmi $(testbox_image_tag); fi

.PHONY: testbox-image
testbox-image: remove-testbox-image
	@$(CONTAINER) build -t $(testbox_image_tag) \
		$(if $(index_url),--build-arg pypi_index=$(index_url),) \
		-f contrib/travis-ci/Dockerfile .

.PHONY: push-testbox-image
push-testbox-image: $(if $(skip_build),,testbox-image)
	@$(CONTAINER) login quay.io
	@$(CONTAINER) push $(testbox_image_tag)


.PHONY: publish-to-pypi
publish-to-pypi:
	@twine upload dist/nitrate-tcms-$(RELEASE_VERSION).tar.gz


.PHONY: help
help:
	@echo 'Usage: make [command]'
	@echo ''
	@echo 'Available commands:'
	@echo ''
	@echo '  rpm              - Create RPM'
	@echo '  srpm             - Create SRPM'
	@echo '  tarball          - Create tarball. Run command: python setup.py sdist'
	@echo '  flake8           - Check Python code style throughout whole source code tree'
	@echo '  test             - Run all tests default'
	@echo '  build            - Run command: python setup.py build'
	@echo '  install          - Run command: python setup.py install'
	@echo '  tags             - Refresh tags for VIM. Default filename is .tags'
	@echo '  etags            - Refresh tags for Emacs. Default filename is TAGS'
	@echo '  help             - Show this help message and exit. Default if no command is given'
