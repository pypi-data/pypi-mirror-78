from cli.shell import run_cmd
from cli.config import DEFAULT_COMMIT


class Command:

    def __init__(self, gitsy):
        self.gitsy = gitsy

    def init(self):
        """
        Creates .gitsy directory, initiates context for current branch.
        """
        return self.gitsy.init()

    def branch(self, branch_name=None):
        """
        Switch to another branch.
        :param branch_name: (optional) Branch name to switch to.
        """
        return self.gitsy.branch(branch_name)

    def up(self, message=DEFAULT_COMMIT):
        """
        Adds, Commits and Pushed changes to remote.
        :param message: (optional) Commit message.
        """
        return self.gitsy.up(message)

    def save(self, message=DEFAULT_COMMIT):
        """
        Adds and Commits changes.
        :param message: (optional) Commit message.
        """
        return self.gitsy.save(message)

    def diff(self):
        """
        Prints diff of selected file.
        """
        return self.gitsy.diff()

    def undo(self, *scope):
        """
        Undo unstaged changes.
        :param scope:
        """
        return self.gitsy.undo(scope)

    def regret(self, *scope):
        return self.gitsy.regret(scope)

    def test(self):
        return self.gitsy.test()

    # ======================== CONTEXT METHODS ======================

    def rm(self, *files):
        return self.gitsy.rm(files)

    def clear(self):
        return self.gitsy.clear()

    def show(self):
        return self.gitsy.show()

    def status(self):
        return self.gitsy.status()

    def add(self, *files):
        return self.gitsy.add(files)

    # ======================== STATIC METHODS =======================

    @staticmethod
    def rename(name):
        run_cmd(f'git branch -m {name}')

    @staticmethod
    def ignore(opt):
        if opt == 'reset':
            run_cmd('git rm -r --cached .')
            run_cmd('git add .')
            run_cmd('git commit -m ".gitignore fixed"')
