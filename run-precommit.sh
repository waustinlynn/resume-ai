#!/bin/bash
# Run pre-commit hooks on changed files
pre-commit run --from-ref HEAD~1 --to-ref HEAD
