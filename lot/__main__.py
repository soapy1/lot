import os

from lot.cli import root

def main():
    if os.environ.get("PARK_URL") is None:
        os.environ["PARK_URL"] = "http://localhost:8000"
    
    root.app()


if __name__ == "__main__":
   main()
