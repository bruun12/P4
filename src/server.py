from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import tempfile
import os

app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("webapp/index.html")

@app.get("/index.html")
async def index():
    return FileResponse("webapp/index.html")

@app.get("/style")
async def style():
    return FileResponse("webapp/style.css")

@app.get("/script")
async def script():
    return FileResponse("webapp/src/app.js")


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
        cwd_path = os.path.join(os.path.dirname(__file__), "")

        # Kør: python main.py <input.mit> (ingen output-fil = printer til stdout)
        cimpleToC = subprocess.run(
            ["python", "main.py", input_path, "output.c"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd_path  # Kør fra /src mappen
        )

        if cimpleToC.returncode != 0:
            return cimpleToC

        cToExecutable = subprocess.run(
            ["gcc", "output.c", "-o", "output"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd_path  # Kør fra /src mappen
        )

        if cToExecutable.returncode != 0:
            return cToExecutable
        
        executeC = subprocess.run(
            ["./output"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd_path  # Kør fra /src mappen
        )

        if executeC.returncode != 0:
            return executeC


        """
        if result.returncode != 0:
            return {"error": result.stderr or "compile error"}
        """
        # main.py printer "Program starter..." + C-koden til stdout
        # Vi fjerner den første linje så kun C-koden returneres


        return executeC

    except subprocess.TimeoutExpired:
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.unlink(input_path)