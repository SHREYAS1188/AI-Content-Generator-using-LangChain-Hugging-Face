from pathlib import Path
import sys
# Ensure local src package is importable when running `uvicorn app:app` from repo root
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ai_content_gen.api import app  # exported FastAPI app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
