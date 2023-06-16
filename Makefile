# utility
# ======================================================================

.PHONY: init init-* run lint autolint lint-strict

init:
	pip3 install -r requirements.txt

# run
# ======================================================================
scrape:
	@echo
	@echo --- Scrape  ---
	python3 scrape/scrape.py

run:
	@echo
	@echo --- Run ---
	python3 main.py

run-example:
	@echo
	@echo --- Run Example ---
	python3 example.py
