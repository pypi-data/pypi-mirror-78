# -*- coding: utf-8 -*-
import sys


__all__ = ('main',)


def main():
    from ark.bin.ark import main as _main
    sys.exit(_main())


if __name__ == '__main__':
    main()
