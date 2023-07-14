ifneq (,$(wildcard .env))
	$(info Found .env file.)
	include .env
	export
endif

style:
	flake8 .

types:
	mypy .

tests:
	pytest .

check:
	make style types tests