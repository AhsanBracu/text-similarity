
PYTHON = python3

.PHONY: help run benchmark test clean

# Display available commands
help:
	@echo "Available commands:"
	@echo "  make run        - Run document similarity detection"
	@echo "  make benchmark  - Run scalability benchmarks"
	@echo "  make test       - Run unit tests"
	@echo "  make clean      - Remove Python cache files"

# Run similarity detection
run:
	$(PYTHON) main.py

# Run performance benchmarks
benchmark:
	$(PYTHON) benchmark.py

# Run unit tests
test:
	$(PYTHON) -m unittest discover -s tests -v

# Remove generated Python cache files
clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
