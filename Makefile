CURRENT_USER_ID:=$(shell id -u)
export CURRENT_USER_ID

CURRENT_GROUP_ID:=$(shell id -g)
export CURRENT_GROUP_ID

INTERACTIVE:=$(shell [ -t 0 ] && echo 1)
ifdef INTERACTIVE
	DOCKER_RUN_TTY_ARG := -it
endif


ACCEPTARGSGOALS := devcodestylecheck devcodestyleformat


# If the first argument in ACCEPTARGSGOALS
ifneq ($(filter $(firstword $(MAKECMDGOALS)),$(ACCEPTARGSGOALS)),)
  # use the rest as arguments
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # turn them into blank targets
  $(eval $(RUN_ARGS):;@:)
endif


CODESTYLEIMIGENAME ?= codestyle

.PHONY: devcodestylecheck
devcodestylecheck:
	cd codestyle && \
	docker build -t $(CODESTYLEIMIGENAME) . && \
	docker run $(DOCKER_RUN_TTY_ARG) --rm --volume "${PWD}:/code" $(CODESTYLEIMIGENAME) check $(RUN_ARGS)

.PHONY: devcodestyleformat
devcodestyleformat:
	cd codestyle && \
	docker build -t $(CODESTYLEIMIGENAME) . && \
	docker run $(DOCKER_RUN_TTY_ARG) --rm --volume "${PWD}:/code" --user "${CURRENT_USER_ID}:${CURRENT_GROUP_ID}" $(CODESTYLEIMIGENAME) format $(RUN_ARGS)

