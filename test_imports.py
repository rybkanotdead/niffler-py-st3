#!/usr/bin/env python3
"""
Test script to verify all critical imports work correctly.
This helps diagnose import errors early in the CI/CD process.
"""

import sys
import importlib
from pathlib import Path

# Add the test directory to Python path
test_dir = Path(__file__).parent / "niffler-e2e-tests-python"
sys.path.insert(0, str(test_dir))

print("=" * 70)
print("Testing Critical Imports for Niffler E2E Tests")
print("=" * 70)

tests = [
    ("Selenium", "selenium", "selenium.__version__"),
    ("Selene", "selene", "selene.__version__"),
    ("gRPC Core", "grpc", "grpc.__version__"),
    ("Protobuf", "google.protobuf", "google.protobuf.__version__"),
    ("pytest", "pytest", "pytest.__version__"),
    ("Faker", "faker", "faker.__version__"),
    ("Requests", "requests", "requests.__version__"),
    ("Pydantic", "pydantic", "pydantic.__version__"),
]

failed = []
passed = []

for name, module_name, version_attr in tests:
    try:
        mod = importlib.import_module(module_name)
        version = getattr(mod, "__version__", "unknown")
        print(f"✅ {name:20} - {module_name:30} v{version}")
        passed.append(name)
    except Exception as e:
        print(f"❌ {name:20} - {module_name:30}")
        print(f"   Error: {type(e).__name__}: {e}")
        failed.append((name, str(e)))

print("\n" + "=" * 70)
print("Testing gRPC Generated Files and Page Objects")
print("=" * 70)

grpc_tests = [
    ("gRPC Stubs", "niffler_e2e_tests_python.clients.grpc_stubs"),
    ("gRPC Stubs - pb2", "niffler_e2e_tests_python.clients.grpc_stubs.niffler_currency_pb2"),
    ("gRPC Stubs - pb2_grpc", "niffler_e2e_tests_python.clients.grpc_stubs.niffler_currency_pb2_grpc"),
    ("gRPC Client", "niffler_e2e_tests_python.clients.grpc_client"),
]

# Try direct path imports for niffler tests
sys.path.insert(0, str(test_dir / "clients"))
sys.path.insert(0, str(test_dir / "clients" / "grpc_stubs"))

for name, module_name in grpc_tests:
    try:
        mod = importlib.import_module(module_name)
        print(f"✅ {name:40}")
        passed.append(name)
    except Exception as e:
        print(f"❌ {name:40}")
        print(f"   Error: {type(e).__name__}: {e}")
        failed.append((name, str(e)))

print("\n" + "=" * 70)
print("Summary")
print("=" * 70)
print(f"Passed: {len(passed)}")
print(f"Failed: {len(failed)}")

if failed:
    print("\nFailed imports:")
    for name, error in failed:
        print(f"  - {name}: {error}")
    sys.exit(1)
else:
    print("\n✅ All critical imports successful!")
    sys.exit(0)

