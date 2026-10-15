import sys
import os

# Ensure backend root and parent root are on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(backend_dir)
for p in (root_dir, backend_dir):
    if p and p not in sys.path:
        sys.path.insert(0, p)

# Support running directly within backend directory
if "backend" not in sys.modules:
    try:
        import backend
    except ImportError:
        import types
        pkg = types.ModuleType("backend")
        pkg.__path__ = [backend_dir]
        sys.modules["backend"] = pkg

from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=False)

