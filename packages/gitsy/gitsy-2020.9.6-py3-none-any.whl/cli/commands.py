from cli.config import DEFAULT_COMMIT
from core.context import Context


class Command:

    def __init__(self, gitsy):
        self.gitsy = gitsy

    #  ===== Git operations commands =====

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
        Undo un-staged (non added) changes.
        :param optional file list as scope:
        """
        return self.gitsy.undo(scope)

    def regret(self, *scope):
        """
        Undo staged (added) changes.
        :param optional file list as scope:
        """
        return self.gitsy.regret(scope)

    def rename(self, name):
        """
        Rename current branch.
        :param required new branch name:
        """
        return self.gitsy.rename(name)

    def ignore(self, opt):
        """
        Enable gitignore modifications: add, remove.
        Syncs gitignore to remote.
        """
        return self.gitsy.ignore(opt)

    def test(self):
        """
        Route for dev purposes
        """
        return self.gitsy.test()

    # ===== Context operations commands =====

    # TODO - all context methods should be invoked from context object within gitsy object

    @staticmethod
    def init():
        """
        Creates .gitsy directory if not yet created
        Adds .gitsy path to gitignore if not yet added
        Creates context file for current branch.
        """
        context = Context.from_command()
        return context.init_context()

    @staticmethod
    def context():
        """
        Prints current context information.
        """
        context = Context.from_command()
        return context.status()

    @staticmethod
    def add(*files):
        context = Context.from_command()
        return context.add(files)

    @staticmethod
    def rm(*files):
        context = Context.from_command()
        return context.rm(files)

    @staticmethod
    def clear():
        context = Context.from_command()
        return context.clear()

    @staticmethod
    def remove():
        context = Context.from_command()
        return context.remove()
