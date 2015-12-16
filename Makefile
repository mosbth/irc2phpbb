#!/usr/bin/make -f
#
#
LOGFILES = aggregate.error aggregate.log aggregate.ignore



#
#
#
.PHONY: clean

clean: 
	rm -f $(LOGFILES)
	rm -rf build



#
#
#
test: prepare jsonlint pylint



#
#
#
.PHONY: prepare

prepare:
	install -d build



#
#
#
.PHONY: jsonlint

jsonlint:
	jsonlint --quiet *.json | tee build/jsonlint 



#
#
#
.PHONY: pylint

pylint:
	pylint --rcfile=.pylintrc *.py | tee build/pylint
