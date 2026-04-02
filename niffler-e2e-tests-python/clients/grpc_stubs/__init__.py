# gRPC generated stubs for Niffler Currency Service

# Import the protobuf generated files with proper module path setup
import sys
from pathlib import Path

# Ensure the grpc_stubs directory is in Python path for relative imports
_stubs_dir = Path(__file__).parent
if str(_stubs_dir) not in sys.path:
    sys.path.insert(0, str(_stubs_dir))

# Now import the generated modules
from . import niffler_currency_pb2, niffler_currency_pb2_grpc

__all__ = ["niffler_currency_pb2", "niffler_currency_pb2_grpc"]


