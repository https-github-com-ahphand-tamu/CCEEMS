import subprocess

def run_models_script():
    try:
        subprocess.run(["python", "models.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running models.py: {e}")
        exit(1)

if __name__ == "__main__":
    run_models_script()
