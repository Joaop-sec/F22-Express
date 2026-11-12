import os
import subprocess
import sys

def main():
    print("1. Criando ambiente virtual (venv)...")
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    if os.name == "nt":
        pip_venv = os.path.join("venv", "Scripts", "pip.exe")
        python_venv = os.path.join("venv", "Scripts", "python.exe")
    else:
        pip_venv = os.path.join("venv", "bin", "pip")
        python_venv = os.path.join("venv", "bin", "python")

    print("2. Instalando bibliotecas do requirements.txt...")
    subprocess.run([pip_venv, "install", "-r", "requirements.txt"], check=True)

    print("3. Baixando pistas e gerando banco de dados...")
    os.makedirs("data", exist_ok=True)
    subprocess.run([python_venv, "aspistaslá.py"], check=True)

    print("\nTudo pronto! Para iniciar o sistema, execute:")
    print(f"{python_venv} main.py")

if __name__ == "__main__":
    main()