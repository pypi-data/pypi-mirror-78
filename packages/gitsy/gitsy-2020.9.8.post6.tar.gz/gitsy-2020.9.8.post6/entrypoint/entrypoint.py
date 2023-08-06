import os
import fire


from cli.commands import Command
from core.gitsy import Gitsy


def main():
    try:
        # ========== for DEV_MODE only ==========
        if 'PC' in os.environ:
            cmd = input('enter command: ') or 'add'
            fire.Fire(Command(Gitsy('/Users/kobarhan/workspace/gitsy_test')), command=cmd)
        # =======================================
        else:
            fire.Fire(Command(Gitsy()))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
