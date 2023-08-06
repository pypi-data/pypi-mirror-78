"""
| A container friendly startup routine for Packmaker servers.
|
| Maintained by Routh.IO
"""
from .core import MineInit


def main():
    """
    | Script entrypoint
    """
    return MineInit()


if __name__ == "__main__":
    main()
