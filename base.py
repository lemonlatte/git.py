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
        stdout, stderr = proc.communicate()
        if proc.returncode:
            raise GitCommandError(stderr)
        # print stdout
        return stdout

    def status(self):
        print self._run('status')

    def stage(self, *args):
        if args:
            self._run('add', *args)
        else:
            self._run('add', ".")

    def unstage(self, *args):
        if args:
            self._run("reset", "HEAD", *args)

    def commit(self, message, body, *args):
        """Test"""
        self._run('commit', "-m", "%s\n\n%s" % (message, body), *args)

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

    def log(self, commit=None):
        _cmd = ['log', '--pretty=format:"%H,%an,%ad,%s,%b"']
        if commit:
            _cmd[1:1] = ['-1', commit]
            raw_log = self._run(*_cmd)
            commit_log = GitLog(*raw_log.split(","))
            return commit_log
        else:
            return self._run(*_cmd)


class GitLog(object):
    def __init__(self, commit, author, date, subject, body):
        self.commit = commit
        self.author = author
        self.date = date
        self.subject = subject
        self.body = body

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "commit %s\nAuthor: %s\nSubject: %s" % (self.commit, self.author, self.subject)
