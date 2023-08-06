import coverage
import os

print("COVERAGE_PROCESS_START", os.environ.get("COVERAGE_PROCESS_START"))
coverage.process_startup()
