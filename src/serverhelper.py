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
    kode = body.get("code", "")

    if not kode.strip():
        return {"error": "Ingen kode modtaget"}

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".cimple", delete=False, encoding="utf-8"
    ) as f:
        f.write(kode)
        input_sti = f.name

    try:
        # Kør: python main.py <input.mit> (ingen output-fil = printer til stdout)
        resultat = subprocess.run(
            ["python", "main.py", input_sti],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=os.path.join(os.path.dirname(__file__), "src")  # Kør fra /src mappen
        )

        if resultat.returncode != 0:
            return {"error": resultat.stderr or "Kompileringsfejl"}

        # main.py printer "Program starter..." + C-koden til stdout
        # Vi fjerner den første linje så kun C-koden returneres
        linjer = resultat.stdout.splitlines()
        c_kode = "\n".join(
            l for l in linjer if not l.startswith("Program starter")
        )

        return {"output": c_kode}

    except subprocess.TimeoutExpired:
        return {"error": "Timeout - koden tog for lang tid"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.unlink(input_sti)