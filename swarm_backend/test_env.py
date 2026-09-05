import sys
print(f"Python Version: {sys.version}")
try:
    import fastapi
    print("FastAPI: OK")
except ImportError:
    print("FastAPI: MISSING")
