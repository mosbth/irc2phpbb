#!/usr/bin/make -f

# ----------------------------------------------------------------------------
#
# Generic stuff
#

# Detect OS
OS = $(shell uname -s)

# Defaults
ECHO = echo

# Make adjustments based on OS
# http://stackoverflow.com/questions/3466166/how-to-check-if-running-in-cygwin-mac-or-linux/27776822#27776822
ifneq (, $(findstring CYGWIN, $(OS)))
	ECHO = /bin/echo -e
endif

# Colors and helptext
NO_COLOR	= \033[0m
ACTION		= \033[32;01m
OK_COLOR	= \033[32;01m
ERROR_COLOR	= \033[31;01m
WARN_COLOR	= \033[33;01m

# Which makefile am I in?
WHERE-AM-I = $(CURDIR)/$(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
THIS_MAKEFILE := $(call WHERE-AM-I)

# Echo some nice helptext based on the target comment
HELPTEXT = $(ECHO) "$(ACTION)--->" `egrep "^\# target: $(1) " $(THIS_MAKEFILE) | sed "s/\# target: $(1)[ ]*-[ ]* / /g"` "$(NO_COLOR)"

# Add local bin path for test tools
#PATH := "./.bin:./vendor/bin:./node_modules/.bin:$(PATH)"
#SHELL := env PATH=$(PATH) $(SHELL)
PHPUNIT := .bin/phpunit
PHPLOC 	:= .bin/phploc
PHPCS   := .bin/phpcs
PHPCBF  := .bin/phpcbf
PHPMD   := .bin/phpmd
PHPDOC  := .bin/phpdoc
BEHAT   := .bin/behat



# target: help               - Displays help.
.PHONY:  help
help:
	@$(call HELPTEXT,$@)
	@$(ECHO) "Usage:"
	@$(ECHO) " make [target] ..."
	@$(ECHO) "target:"
	@egrep "^# target:" $(THIS_MAKEFILE) | sed 's/# target: / /g'



# ----------------------------------------------------------------------------
#
# Specifics
#
LOGFILES = aggregate.error aggregate.log aggregate.ignore
PYFILES = *.py
JSONFILES = *.json



# target: clean              - Removes generated files and directories.
.PHONY: clean
clean:
	@$(call HELPTEXT,$@)
	rm -f $(LOGFILES)
	rm -rf build
	find -type d -name __pycache__ -exec rm -rf {} \;
	find -type f -name '*.pyc' -exec rm -f {} \;



# target: prepare            - Prepare for tests and build
.PHONY: prepare
prepare:
	@$(call HELPTEXT,$@)
	install -d build



# target: test                - Run all tests.
.PHONY: test
#test: prepare jsonlint pylint pycodestyle flake8 unittest doctest coverage
test: prepare jsonlint pylint # pycodestyle flake8 unittest doctest coverage
	@$(call HELPTEXT,$@)



# target: pylint              - Run pylint validation.
.PHONY: pylint
pylint:
	@$(call HELPTEXT,$@)
	@install -d build/pylint
	-pylint --reports=no *.py
	-@pylint *.py > build/pylint/output.txt



# target: pycodestyle         - Run pycodestyle validation.
.PHONY: pycodestyle
pycodestyle:
	@$(call HELPTEXT,$@)
	@install -d build/pycodestyle
	-pycodestyle --exclude=orig --count --statistics . | tee build/pycodestyle/log.txt



# target: flake8              - Run flake8 validation.
.PHONY: flake8
flake8:
	@$(call HELPTEXT,$@)
	@install -d build/flake8
	-flake8 --exclude=orig --count --statistics . | tee build/flake8/log.txt



# target: unittest            - Run all unittests.
.PHONY: unittest
unittest:
	@$(call HELPTEXT,$@)
	python3 -m unittest discover -b -s tests



# target: doctest             - Run all doctests.
.PHONY: doctest
doctest:
	@$(call HELPTEXT,$@)
	python3 -m doctest *.py



# target: coverage            - Run code coverage of all unittests.
.PHONY: coverage
coverage:
	@$(call HELPTEXT,$@)
	@install -d build/coverage-html
	$(ENV) && coverage run --source=. -m unittest discover -b -s tests
	$(ENV) && coverage html --directory=build/coverage-html
	$(ENV) && coverage report -m



# target: install-tools       - Install needed devtools.
.PHONY: install-tools
install-tools:
	@$(call HELPTEXT,$@)
	python3 -m pip install --requirement .requirements.txt 



# target: upgrade-tools       - Upgrade needed devtools.
.PHONY: upgrade-tools
upgrade-tools:
	@$(call HELPTEXT,$@)
	python3 -m pip install --upgrade --requirement .requirements.txt 


# target: check               - Check versions of installed devtools.
.PHONY: check
check:
	@$(call HELPTEXT,$@)
	@$(ECHO) "$(INFO_COLOR)python:$(NO_COLOR)" && which python3 && python3 --version
	@$(ECHO) "\n$(INFO_COLOR)pip:$(NO_COLOR)" && python3 -m pip --version
	@$(ECHO) "\n$(INFO_COLOR)pylint:$(NO_COLOR)" && which pylint && pylint --version
	@$(ECHO) "\n$(INFO_COLOR)coverage:$(NO_COLOR)" && which coverage && coverage --version
	@$(ECHO) "\n$(INFO_COLOR)flake8:$(NO_COLOR)" && which flake8 && flake8 --version
	@$(ECHO) "\n$(INFO_COLOR)pycodestyle:$(NO_COLOR)" && which pycodestyle && pycodestyle --version


#
#
# target: jsonlint           - Validate all JSON files.
.PHONY: jsonlint
jsonlint: $(JSONFILES)
	@$(call HELPTEXT,$@)

$(JSONFILES):
	jsonlint --quiet $@ 2>&1 | tee build/jsonlint-$@



#
#
#
.PHONY: pylint

pylint:
	pylint --rcfile=.pylintrc $(PYFILES) | tee build/pylint
