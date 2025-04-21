import subprocess
import os

# Fast API
from typing import Union
from fastapi import FastAPI
app = FastAPI()

# Benchmark
import time

@app.get("/")
def read_root():
    return {"Hello": "Scraper"}

@app.get("/ls")
def read_root():
    result = subprocess.run("ls -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="cp437")
    output = result.stdout
    return_code = result.returncode
    return {"return_code": return_code, "output": output}

@app.get("/hyundai/daemon/{trackingNumber}")
async def hyundai_daemon_scrape(trackingNumber: str):
    # If server is windows
    WIN_COMMAND = "docker run -it --rm -v C:/Users/Shipsgo_Ugur/Desktop/seleniumbasedocker/SeleniumBase/scrapers:/SeleniumBase/scrapers:rw seleniumbase python3 carriers/hyundai/hyundai-scrape.py " + str(trackingNumber)

    proxy_token_for_linux = os.getenv("PROXY_TOKEN")

    # server is linux
    LIN_COMMAND = "docker run -it --rm -e PROXY_TOKEN -v /root/srv/seleniumbase/SeleniumBase/scrapers:/SeleniumBase/scrapers:rw seleniumbase python3 /SeleniumBase/scrapers/api/carriers/hyundai/hyundai-scrape.py " + str(trackingNumber)

    result = subprocess.run(
        args=LIN_COMMAND,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        encoding="cp437"
    )

    output = result.stdout
    return_code = result.returncode

    return {"return_code": return_code, "result": output}