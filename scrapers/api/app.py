import subprocess
import os
import ast
import time

# Fast API
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
app = FastAPI()

# Benchmark
import time

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

@app.get("/")
def read_root():
    return {"Hello": "Scraper"}

@app.get("/ls")
def read_root():
    result = subprocess.run("ls -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    output = result.stdout
    return_code = result.returncode
    return {"return_code": return_code, "output": output}

@app.get("/scrape/hyundai/{blNumber}")
async def hyundai_scrape(blNumber: str):

    SCRAPE_COMMAND = "python3 /SeleniumBase/scrapers/api/carriers/hyundai/turkon-scraper.py " + str(blNumber)
    
    # General Benchmark START
    start_time = time.time()  # Başlangıç zamanı

    result = subprocess.run(
        args=SCRAPE_COMMAND,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        encoding="utf-8"
    )

    output = result.stdout
    return_code = result.returncode

    parsed_json_output = ast.literal_eval(output)

    # Genel Benchmark END
    end_time = time.time()  # Bitiş zamanı
    elapsed_time = end_time - start_time
    general_benchmark_time = f"Geçen süre: {elapsed_time:.5f} saniye"

    return {"return_code": return_code, "general_benchmark": general_benchmark_time, "result": parsed_json_output}


@app.get("/hyundai/daemon/{trackingNumber}")
async def hyundai_daemon_scrape(trackingNumber: str):

    # If server is windows
    WIN_COMMAND = "docker run -it --rm -v C:/Users/Shipsgo_Ugur/Desktop/seleniumbasedocker/SeleniumBase/scrapers:/SeleniumBase/scrapers:rw seleniumbase python3 carriers/hyundai/turkon-scraper.py " + str(trackingNumber)

    proxy_token_for_linux = os.getenv("PROXY_TOKEN")

    # server is linux
    LIN_COMMAND = "docker run -it --rm -e PROXY_TOKEN -v /root/srv/seleniumbase/SeleniumBase/scrapers:/SeleniumBase/scrapers:rw seleniumbase python3 /SeleniumBase/scrapers/api/carriers/hyundai/turkon-scraper.py " + str(trackingNumber)

    result = subprocess.run(
        args=LIN_COMMAND,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        encoding="utf-8"
    )

    output = result.stdout
    return_code = result.returncode

    return {"return_code": return_code, "result": output}

