import calendar
import sys

def table(y, m):
    """
    Format rest. Tatiana. Beautiful girl :).
    """
    return calendar.month(y, m)


if __name__ == "__main__":
    print('.. table::', table(int(sys.argv[1]), int(sys.argv[2])))
