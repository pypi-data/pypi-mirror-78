import tempfile
import re
import warnings


class GitAdapter(object):
    LIST_OPTION = '--list'
    SORT_OPTION = '--sort'
    HEAD_COMMIT = 'HEAD'
    OPTION_WITH_ARG_FMT = '{option}={value}'
    EMPTY_REPOSITORY_HASH = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

    def __init__(self, repository_dir='.'):
        import git
        self._git_client = git.cmd.Git(repository_dir)
        self._first_commit = None

    def tags(self, sort='-committerdate'):
        sort_option = self.OPTION_WITH_ARG_FMT.format(
            option=self.SORT_OPTION,
            value=sort,
        )

        args = (self.LIST_OPTION, sort_option)
        client_output = self._git_client.tag(args)
        tags = client_output.splitlines()
        return tags

    def diff(self, version, another_version):
        version = version or self.EMPTY_REPOSITORY_HASH

        if version == self.EMPTY_REPOSITORY_HASH:
            msg_fmt = """Creating diff comparing revision[{0}]
            and the repository beginning"""

            warnings.warn(
                msg_fmt.format(another_version)
            )

        diff_file = tempfile.TemporaryFile()
        self._git_client.diff(
            version,
            another_version,
            output_stream=diff_file
        )

        return diff_file

    @property
    def first_commit(self):
        if self._first_commit:
            return self._first_commit

        command_output = tempfile.TemporaryFile()

        args = [
            '--reverse',
            "--pretty=%H",
        ]

        self._git_client.log(args, output_stream=command_output)
        command_output.seek(0)
        first_in_bytes = command_output.readline()
        command_output.close()
        first = first_in_bytes.decode()

        return first.strip()

    def commit_is_first(self, commit):
        return commit == self.first_commit

    @property
    def head_commit(self):
        client_output = self._git_client.rev_parse(self.HEAD_COMMIT)
        return client_output.strip()

    @property
    def current_commit(self):
        return self.head_commit

    @property
    def previous_commit(self):
        return self.previous_commit_from(self.current_commit)

    def previous_commit_from(self, commit, offset=1):
        if self.commit_is_first(commit):
            return self.EMPTY_REPOSITORY_HASH

        command_fmt = "{commit}~{offset}"

        command = command_fmt.format(
            commit=commit,
            offset=offset,
        )

        client_output = self._git_client.rev_parse(
            command
        )

        return client_output.strip()

    def show_commit_refs(self, commit):
        with tempfile.TemporaryFile() as client_output:
            self._git_client.show_ref(
                "--head", "--heads", "--tags", output_stream=client_output
            )
            refs = _read_file_lines_generator(client_output)
            refs = list(
                filter(
                    lambda ref: re.search(commit, ref),
                    refs,
                )
            )

            return refs

    def show_commit_from_tag(self, tag):
        client_output = self._git_client.rev_parse(
            tag
        )

        return client_output.strip()

    @property
    def empty_repository_tree_commit(self):
        return self.EMPTY_REPOSITORY_HASH


def _read_file_lines_generator(file):
    file.seek(0)

    while True:
        line = file.readline()
        line = line.decode().strip()

        if line:
            yield line
        else:
            break
