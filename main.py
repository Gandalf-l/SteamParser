from steam_parser import SteamParser
from datetime import datetime


def main():
  try:
    start = datetime.now()

    parser = SteamParser()
    parser.parse()

    end = datetime.now()
    total = end - start
    print(str(total))

  except Exception as ex:
    print(ex)


if __name__ == '__main__':
  main()
