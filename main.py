import argparse
from application import Application

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load")
    args = parser.parse_args()
    print(args)

    Application(args.load).start()
