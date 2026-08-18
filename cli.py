import argparse
from pathlib import Path
from .runtime import run

def main():
    ap=argparse.ArgumentParser(prog="thanvi", description="Thanvi Programming Language")
    ap.add_argument("file")
    a=ap.parse_args()
    run(Path(a.file).read_text(encoding="utf-8"))

if __name__=="__main__": main()
