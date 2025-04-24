import subprocess

results = subprocess.run("echo 22", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)

print(str({"hello": "world"}))