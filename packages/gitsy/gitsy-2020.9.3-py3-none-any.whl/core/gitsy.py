import os
from os.path import join
from pathlib import Path
from subprocess import DEVNULL

from git import Repo
from git import InvalidGitRepositoryError
from git import GitCommandError
from termcolor import colored

from cli.shell import run_cmd
from cli.display import *
from cli.interactive import *
from cli.config import *

from core.context import Context, contextual


class Gitsy:

    def __init__(self, repo_path=os.getcwd()):
        try:
            # initialize repo object
            self.repo = Repo(repo_path, search_parent_directories=True)
            self.repo_path = os.path.dirname(self.repo.git_dir)

            # initialize attributes for methods usage
            self._cwd = os.getcwd()
            self._branch = self.repo.active_branch.name

        except InvalidGitRepositoryError:
            raise Exception('Not a git repo, I have no power here...')

    def get_branch(self):
        return self._branch

    # ====================== NON CONTEXTUAL METHODS =====================

    def init(self):
        """
        initialize an empty context on current branch
        """
        context = Context(self.repo)
        if not context.get_context('optional'):
            context.init_context()

    def branch(self, target_branch):
        """
        Swith to target_branch if specified, else prompt branch menu.
        Implements auto-stashing to allow flex branch hopping.
        :param target_branch:
        :return:
        """
        if not target_branch:
            branches = [branch.name for branch in list(self.repo.branches)]
            if len(branches) == 1:
                return 'No local branches detected'
            else:
                target_branch = branch_selector(branches)
                if not target_branch:
                    return
        change_list = [item.a_path for item in self.repo.index.diff(None)]
        if len(change_list) > 0:
            run_cmd(f'git stash save "{GLOBAL_STASH_PREFIX}_{self.get_branch()}"')
            print(f'stashing diff at {GLOBAL_STASH_PREFIX}_{self.get_branch()}')
        self._switch_branch(target_branch)

        stash_list = run_cmd(f'git stash list', stderr=DEVNULL)[0]
        stash_stub = f'{GLOBAL_STASH_PREFIX}_{self.get_branch()}'
        if stash_list:
            stash_list = stash_list.split("\n")

        for stash in stash_list:
            stash_name = stash.split(' ')[-1]
            if stash_stub == stash_name:
                stash_index = stash.split(' ')[0].replace(':', '')
                run_cmd(f'git stash pop {stash_index}', stderr=DEVNULL)
                break

    # ====================== OPTIONALLY CONTEXTUAL METHODS =====================

    @contextual('optional')
    def up(self, context, message):
        change_list = list(self._calculate_change_list(context))
        if change_list:
            self._up(change_list, message)
        else:
            return f'Nothing to send up within context: {self._branch}'

    @contextual('optional')
    def save(self, context, message):
        change_list = list(self._calculate_change_list(context))
        if change_list:
            self._save(change_list, message)
        else:
            return f'No changes to save within context: {self._branch}'

    @contextual('optional')
    def diff(self, context):
        change_list = self._calculate_change_list(context)
        if not change_list:
            return 'No diff for you!'
        file = file_selector(change_list)
        if not file:
            return
        diff = self.repo.git.diff(file).split('\n')
        sep = '~' * 60
        print(colored(sep, 'white'))
        for line in diff:
            if line.startswith('+++') or line.startswith('---'):
                print(colored(line, 'white'))
            elif line.startswith('+'):
                print(colored(line, 'green'))
            elif line.startswith('-'):
                print(colored(line, 'red'))
            else:
                print(colored(line, 'white'))
        print(colored(sep, 'white'))

    @contextual('optional')
    def undo(self, context, scope):
        try:
            scope = self._get_scope(context, scope, None, 'undo')
        except Exception as e:
            return e
        self.repo.git.checkout('--', list(scope))
        display_list('undo', scope)

    @contextual('optional')
    def regret(self, context, scope):
        try:
            scope = self._get_scope(context, scope, 'HEAD', 'regret')
        except Exception as e:
            return e
        self.repo.git.reset('--', scope)
        display_list('unstaged', scope)

    # ====================== ONLY CONTEXTUAL METHODS =====================

    @contextual('required')
    def clear(self, context):
        context['working-on'].clear()
        display_message(f'context cleared', 'magenta', 'ledger')

    @contextual('required')
    def rm(self, context, files):
        if len(files) == 0:
            if len(context["working-on"]) > 0:
                files = files_checkboxes(context['working-on'], 'remove from context')
            else:
                display_message(f'No files in context', 'magenta', 'construction_worker')
                return
        for file in list(files):
            context['working-on'].remove(file)
        display_list('removed', list(files))

    @contextual('required')
    def show(self, context):
        display_message(f'status: {context["status"]}', 'magenta', 'ledger')
        if len(context["working-on"]) > 0:
            display_list('working-on', context['working-on'])
        else:
            display_message(f'No files in context', 'magenta', 'construction_worker')

    @contextual('required')
    def status(self, context):
        working_on = context['working-on']
        print('Pending changes:')
        for item in self.repo.index.diff(None):
            if item.a_path in working_on:
                print('\t' + colored(item.a_path, 'red'))

    @contextual('required')
    def add(self, context, files):

        if len(files) == 0:
            path = Path(self.repo_path)

            # collect all files in repo
            opt_files = [str(file.relative_to(self.repo_path))
                         for file in list(path.rglob('*'))
                         if self._file_conditions(self.repo_path, file)]

            # subtract files that are already added
            opt_files = set(opt_files) - set(context['working-on'])

            if not opt_files:
                return 'No files found to add.'
            else:
                files = files_checkboxes(list(opt_files), 'add')

        added_files = []
        for file in files:
            added_files.append(self._normalize_path(file))

        added_files = set(added_files) - set(context['working-on'])
        context['working-on'] += list(added_files)
        display_list('added', added_files)

    @staticmethod
    def rename(name):
        run_cmd(f'git branch -m {name}')

    @staticmethod
    def ignore(opt):
        if opt == 'reset':
            run_cmd('git rm -r --cached .')
            run_cmd('git add .')
            run_cmd('git commit -m ".gitignore fixed"')

    # ==================== INTERNAL AUX METHODS ====================

    def _normalize_path(self, file):
        if not os.path.exists(f'{self.repo_path}/{file}'):
            rel_path = os.path.relpath(self._cwd, self.repo_path)
            adjusted_file = join(rel_path, file)
            return adjusted_file
        else:
            return file

    def _up(self, files, message):
        try:
            self._save(files, message)
            display_list('up', files)
        except GitCommandError:
            print(colored(f'pushing without changes', 'cyan'))
        run_cmd(f'git stash save "{GLOBAL_STASH_PREFIX}_{self.get_branch()}"', stdout=DEVNULL, stderr=DEVNULL)
        self.repo.git.push('origin', self._branch)
        display_message('pushed', 'green', 'thumbsup')

    def _save(self, files, message):
        display_list('saving', files)
        self.repo.git.add(files)
        commit = self.repo.git.commit('-m', message)
        display_message(commit, 'white', 'cat')
        display_message('saved', 'green', 'thumbsup')

    def _switch_branch(self, branch_name):
        self.repo.git.checkout(branch_name)
        self._branch = self.repo.active_branch.name

    # TODO: the scope should not be all in context but all changed in context (like in the add function)
    def _get_scope(self, context, scope, diff, method):
        change_list = self._calculate_change_list(context, diff)
        if len(scope) == 0:
            if len(change_list) > 0:
                scope = files_checkboxes(change_list, method)
            else:
                raise Exception(f'No actionable items in found context: {self._branch}')

        elif scope[0] == 'all':
            if len(scope) < 2 or not scope[1] == 'allow':
                try:
                    verified = verify_prompt(f'This will {method} all staged changes')
                except Exception:
                    return
                if not verified:
                    return
            scope = change_list
        else:
            scope = [value for value in scope
                     if value in change_list]
        return scope

    def _calculate_change_list(self, context, diff_source=None):
        change_list = [item.a_path for item in self.repo.index.diff(diff_source)] + self.repo.untracked_files
        context_list = context['working-on'] if context else change_list
        return self._intersection(change_list, context_list)

    @staticmethod
    def _intersection(iterable1, iterable2):
        return set(iterable1).intersection(iterable2)

    @staticmethod
    def _file_conditions(root, file):
        file_parents = [p.name for p in list(file.relative_to(root).parents)]
        return file.is_file() \
               and '.git' not in file_parents \
               and '.gitsy' not in file_parents

    # ==================== TEST METHODS ====================

    def test(self):
        print('=== TEST ROUTE ===')

        # stash_list = run_cmd(f'git stash list', stderr=DEVNULL)[0]
        # stash_stub = 'test1_state'
        # if stash_list:
        #     stash_list = stash_list.split("\n")
        # print(stash_list)
        # for stash in stash_list:
        #     stash_name = stash.split(' ')[-1]
        #     if stash_stub == stash_name:
        #         print(f'found {stash_name}')
        #         stash_index = stash.split(' ')[0].replace(':', '')
        #         print(f'stash_index = {stash_index}')

        print('=== END TEST ROUTE ===')
