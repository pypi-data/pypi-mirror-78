import os
from os.path import join

import yaml
from termcolor import colored

from cli.shell import run_cmd
from cli.config import (
    BRANCH_CONTEXT_INIT,
    GLOBAL_CONTEXT_INIT
)

from cli.display import display_message
from cli.interactive import verify_prompt


class Context:

    def __init__(self, repo) -> None:
        self.repo = repo
        self.repo_path = os.path.dirname(repo.git_dir)
        self.branch = repo.active_branch.name
        self.branch_context = join(self.repo_path, '.gitsy', f'context_{self.branch}.yaml')

    def init_context(self):
        if not os.path.isdir(join(self.repo_path, '.gitsy')):
            self._init_global_context()
        if not os.path.exists(self.branch_context):
            self._init_branch_context()
        else:
            print(colored(f'local context for {self.branch} exists:', 'red '))
            with open(self.branch_context, 'r') as f:
                print(f.read())

    # def switch(self, from_ctx, to_ctx):
    #     self.repo = repo
    #     self.repo_path = os.path.dirname(repo.git_dir)
    #     self.branch = repo.active_branch.name
    #     self.branch_context = f'{self.repo_path}/.gitsy/context_{self.branch}.yaml'

    def get_context(self, opt, silent=False):
        if opt == 'required':
            if not os.path.exists(self.branch_context):
                try:
                    verified = verify_prompt("No context found for this branch, create one?")
                except Exception:
                    return
                if not verified:
                    return False
                else:
                    self.repo.init()

            with open(self.branch_context, 'r') as f:
                context = yaml.load(f, Loader=yaml.FullLoader)

            if context['status'] == 'disabled':
                print('context is disabled for this branch')
                return False

            display_message(f'Running in branch context: {self.branch}', 'magenta', 'house')
            return context

        elif opt == 'optional':
            if not os.path.exists(self.branch_context):
                display_message('Running in global context', 'magenta', 'earth_africa')
                return False
            else:
                with open(self.branch_context, 'r') as f:
                    context = yaml.load(f, Loader=yaml.FullLoader)

                if context['status'] == 'disabled':
                    display_message('Running in global context', 'magenta', 'earth_africa')
                    return False
                else:
                    display_message(f'Running in branch context: {self.branch}', 'magenta', 'house')
                    return context

    def set_context(self, context):
        with open(self.branch_context, 'w') as f:
            yaml.dump(context, f)

    def _init_global_context(self):
        run_cmd('mkdir -p .gitsy')
        with open('.gitignore', 'a') as ignore_file:
            ignore_file.write('/.gitsy/')
        self.repo.git.add('.gitignore')
        file_name = join('.gitsy', 'global_context.yaml')
        with open(file_name, 'w') as f:
            yaml.dump(GLOBAL_CONTEXT_INIT, f)

    def _init_branch_context(self):
        display_message(f'initiating local context for branch: {self.branch}', 'cyan', 'house')
        with open(self.branch_context, 'w') as f:
            yaml.dump(BRANCH_CONTEXT_INIT, f)


def contextual(opt):
    def context_decorator(func):
        def context_wrapper(self, *args, **kwargs):
            ctx = Context(self.repo)
            context = ctx.get_context(opt)
            res = func(self, context, *args, **kwargs)
            if context:
                ctx.set_context(context)
            return res
        return context_wrapper
    return context_decorator
