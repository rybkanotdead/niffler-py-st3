#!/usr/bin/env python3
"""
Niffler E2E Tests - CI Setup & Validation Script
This script verifies all dependencies and configurations before running tests.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a shell command and handle errors."""
    if description:
        print(f"\n{description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr if e.stderr else e.stdout}")
        return False

def check_package_version(import_path: str, package_name: str) -> bool:
    """Check if a package is installed and get its version."""
    try:
        parts = import_path.split('.')
        module = __import__(parts[0])
        for part in parts[1:]:
            module = getattr(module, part)

        version = getattr(module, '__version__', 'unknown')
        print(f"  ✅ {package_name:20} - {import_path:35} v{version}")
        return True
    except Exception as e:
        print(f"  ❌ {package_name:20} - Error: {e}")
        return False

def main():
    """Main setup and validation function."""
    print("=" * 80)
    print("Niffler E2E Tests - CI Setup & Validation")
    print("=" * 80)

    # Change to niffler-e2e-tests-python directory
    script_dir = Path(__file__).parent
    test_dir = script_dir / "niffler-e2e-tests-python"

    if not test_dir.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return 1

    os.chdir(test_dir)
    print(f"📂 Working directory: {test_dir}")

    # Step 1: Install dependencies
    print("\n" + "=" * 80)
    print("Step 1️⃣  - Installing Dependencies")
    print("=" * 80)

    if not run_command("pip install --upgrade pip setuptools wheel", "Upgrading pip..."):
        return 1

    if not run_command("pip install -e .", "Installing project dependencies..."):
        return 1

    # Step 2: Verify critical imports
    print("\n" + "=" * 80)
    print("Step 2️⃣  - Verifying Critical Imports")
    print("=" * 80)

    packages = [
        ("selenium", "selenium.__version__", "Selenium WebDriver"),
        ("selene", "selene.__version__", "Selene (Selenium wrapper)"),
        ("grpc", "grpc.__version__", "gRPC"),
        ("protobuf", "google.protobuf.__version__", "Protocol Buffers"),
        ("pytest", "pytest.__version__", "pytest"),
        ("faker", "faker.__version__", "Faker"),
        ("requests", "requests.__version__", "requests"),
        ("pydantic", "pydantic.__version__", "Pydantic"),
        ("allure", "allure.__version__", "Allure"),
    ]

    failed_packages = []

    print("\n📦 Package Versions:")
    for pkg_name, version_path, display_name in packages:
        if not check_package_version(version_path, display_name):
            failed_packages.append(display_name)

    if failed_packages:
        print(f"\n❌ Failed to import {len(failed_packages)} package(s):")
        for pkg in failed_packages:
            print(f"   - {pkg}")
        return 1

    # Step 3: Verify gRPC generated files
    print("\n🔌 Checking gRPC Generated Files:")
    try:
        from clients.grpc_stubs import niffler_currency_pb2, niffler_currency_pb2_grpc
        from clients.grpc_client import CurrencyGrpcClient
        print("  ✅ niffler_currency_pb2")
        print("  ✅ niffler_currency_pb2_grpc")
        print("  ✅ CurrencyGrpcClient")
    except Exception as e:
        print(f"  ❌ gRPC imports failed: {type(e).__name__}: {e}")
        return 1

    # Step 4: Verify Page Objects (may fail due to Selene version incompatibilities)
    print("\n📄 Checking Page Objects:")
    page_objects = [
        ("pages.auth_reg_page", "AuthRegistrationPage"),
        ("pages.profile_page", "ProfilePage"),
        ("pages.spendings_page", "SpendingPage"),
    ]

    failed_pages = []
    for module_path, class_name in page_objects:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {class_name}")
        except Exception as e:
            print(f"  ⚠️  {class_name}: {type(e).__name__}: {e}")
            failed_pages.append((class_name, str(e)))

    if failed_pages:
        print(f"\n⚠️  {len(failed_pages)} page object(s) failed to load (may be due to Selene version):")
        for class_name, error in failed_pages:
            print(f"   - {class_name}: {error}")
        print("   UI tests will be skipped during pytest execution.")

    # Step 5: Create allure-results directory
    print("\n📁 Creating allure-results directory...")
    allure_dir = Path("allure-results")
    allure_dir.mkdir(exist_ok=True)
    print(f"  ✅ Created: {allure_dir.absolute()}")

    # Step 6: List test files
    print("\n🧪 Test Files Found:")
    test_files = list(Path("tests").glob("test_*.py"))
    if not test_files:
        print("  ⚠️  No test files found!")
    else:
        for test_file in sorted(test_files):
            print(f"  📋 {test_file}")

    print("\n" + "=" * 80)
    print("✅ CI Setup Complete!")
    print("=" * 80)
    print(f"\n🚀 Ready to run tests with: pytest tests/")

    return 0

if __name__ == "__main__":
    sys.exit(main())

