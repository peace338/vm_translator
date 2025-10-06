import argparse
from Parser.parser import Parser

def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path of input file. ex: ./fileName.vm")
    parser.add_argument("--debug", action="store_true", help="run debug mode")
    args = parser.parse_args()
    
    return args

def main(args:argparse.Namespace):
    parser = Parser(args.input)

if __name__ == "__main__":
    args = parser()
    main(args)