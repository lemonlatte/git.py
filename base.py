from os import path
import subprocess


class GitCommandError(Exception):
    pass


class GitRepo(object):

    def __init__(self, repo_path=None, git_exec=None):
        self.repo_path = repo_path
        self.git_exec = git_exec
        self.status()

    def _run(self, *args):
        cmd = [self.git_exec]
        if self.repo_path:
            cmd.extend(["--git-dir=%s" % path.join(self.repo_path, ".git"),
                        "--work-tree=%s" % self.repo_path])

        cmd.extend(args)
        print " ".join(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.wait()
        if proc.returncode:
            raise GitCommandError(proc.stderr.read())
        print proc.stdout.read()
        print proc.stderr.read()

    def status(self):
        self._run('status')

    def stage(self, *args):
        if args:
            self._run('add', *args)

    def unstage(self, *args):
        if args:
            self._run("reset", "HEAD", *args)

    def commit(self, message, *args):
        self._run('commit', "-m", message, *args)

    # @repo_func
    def fetch(self, remote="origin", branch="master", *args):
        self._run('fetch', remote, branch)

    def pull(self, remote="origin", branch="master", **kwargs):
        _cmd = [remote, branch]
        if kwargs.get("rebase", False):
            _cmd.insert(0, "--rebase")
        self._run("pull", *_cmd)

    def push(self, remote="origin", branch="master", *args):
        self._run('push', remote, branch)
