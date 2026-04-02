#!/bin/bash
cd /Users/alina/PycharmProjects/niffler-py-st3
git add niffler-e2e-tests-python/tests/test_spending_page.py
git commit -m "fix: trigger GitHub Actions workflow for spending page tests"
git push origin main
echo "Push completed"

