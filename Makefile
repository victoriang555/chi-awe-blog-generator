# utility
# ======================================================================

.PHONY: init init-* run lint autolint lint-strict

init:
	pip3 install -r requirements.txt

# run
# ======================================================================
run:
	@echo
	@echo --- Run ---
	python3 main.py
