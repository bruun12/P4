from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/compile")
def compile_code(body: dict):
    code = body.get("code", "")

    if not code.strip():
        return {"error": "No code passed"}

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".cimple", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        input_path = f.name

    try:
        # Kør: python main.py <input.mit> (ingen output-fil = printer til stdout)
        result = subprocess.run(
            ["python", "main.py", input_path, "output.c", "&&", "gcc", "output.c", "-o", "output", "&&", "./output"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=os.path.join(os.path.dirname(__file__), "")  # Kør fra /src mappen
        )

        """
        if result.returncode != 0:
            return {"error": result.stderr or "compile error"}
        """
        # main.py printer "Program starter..." + C-koden til stdout
        # Vi fjerner den første linje så kun C-koden returneres


        return {"output": result}

    except subprocess.TimeoutExpired:
        return {"error": "Timeout - koden tog for lang tid"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.unlink(input_path)