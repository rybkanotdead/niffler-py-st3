#!/bin/bash
# Comprehensive test setup script for Niffler E2E Tests CI/CD

set -e

echo "=========================================="
echo "Niffler E2E Tests - CI Setup & Validation"
echo "=========================================="

# Change to the niffler-e2e-tests-python directory
cd "$(dirname "$0")/niffler-e2e-tests-python" || exit 1

echo ""
echo "1️⃣  Installing dependencies..."
pip install --upgrade pip setuptools wheel

# Install from the project pyproject.toml
pip install -e .

echo ""
echo "2️⃣  Verifying critical imports..."
python3 << 'EOF'
import sys

print("\n📦 Checking Package Versions:")
packages = {
    'selenium': 'selenium.__version__',
    'selene': 'selene.__version__',
    'grpc': 'grpc.__version__',
    'protobuf': 'google.protobuf.__version__',
    'pytest': 'pytest.__version__',
}

for pkg_name, version_path in packages.items():
    try:
        parts = version_path.split('.')
        mod = __import__(parts[0])
        for part in parts[1:-1]:
            mod = getattr(mod, part)
        version = getattr(mod, parts[-1])
        print(f"  ✅ {pkg_name:15} {version}")
    except Exception as e:
        print(f"  ❌ {pkg_name:15} Error: {e}")
        sys.exit(1)

print("\n🔌 Checking gRPC Generated Files:")
try:
    from clients.grpc_stubs import niffler_currency_pb2, niffler_currency_pb2_grpc
    print("  ✅ niffler_currency_pb2")
    print("  ✅ niffler_currency_pb2_grpc")
except Exception as e:
    print(f"  ❌ gRPC imports failed: {e}")
    sys.exit(1)

print("\n📄 Checking Page Objects:")
try:
    from pages.auth_reg_page import AuthRegistrationPage
    from pages.profile_page import ProfilePage
    from pages.spendings_page import SpendingPage
    print("  ✅ AuthRegistrationPage")
    print("  ✅ ProfilePage")
    print("  ✅ SpendingPage")
except Exception as e:
    print(f"  ❌ Page objects import failed: {e}")
    sys.exit(1)

print("\n✅ All imports verified successfully!")
EOF

echo ""
echo "3️⃣  Creating allure-results directory..."
mkdir -p allure-results

echo ""
echo "4️⃣  Finding and listing test files..."
test_count=$(find tests -name "test_*.py" | wc -l)
echo "  📋 Found $test_count test files:"
find tests -name "test_*.py" | sed 's/^/     /'

echo ""
echo "✅ CI Setup Complete!"
echo ""

