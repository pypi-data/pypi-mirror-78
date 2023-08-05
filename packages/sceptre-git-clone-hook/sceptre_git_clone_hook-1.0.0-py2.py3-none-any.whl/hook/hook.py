import os, git, shutil
from git.repo.base import Repo
from sceptre.hooks import Hook

class GitClone(Hook):
    NAME = 'git_clone'
    DELIMITER = ' '

    def __init__(self, *args, **kwargs):
        super(GitClone, self).__init__(*args, **kwargs)

    def run(self):
        """
        Removes, if exists, the current folder and clones the repository in that folder that you have passed by
        - argument with space like delimiter (ie: !git_clone https://github.com/bilardi/sceptre-git-clone-hook my-folder)
        - sceptre_user_data with properties GitRepository and RepositoryFolder
            Raise (Exception): when the system does not find the arguments repository and folder in argument or sceptre_user_data
        """
        if self.argument and self.DELIMITER in self.argument:
            repository, folder = self.argument.split(self.DELIMITER, 1)
            self.logger.debug("[{}] Parameters parsed from the argument".format(self.NAME))
        elif self.stack.sceptre_user_data and 'GitRepository' in self.stack.sceptre_user_data and 'RepositoryFolder' in self.stack.sceptre_user_data:
            repository = self.stack.sceptre_user_data.get('GitRepository', {})
            folder = self.stack.sceptre_user_data.get('RepositoryFolder', {})
            self.logger.debug("[{}] Parameters parsed from sceptre_user_data".format(self.NAME))
        else:
            raise Exception("Parameters GitRepository and RepositoryFolder could not be parsed from sceptre_user_data or argument")

        if os.path.exists(folder):
            shutil.rmtree(folder)
            self.logger.info("[{}] Removed the local repository folder {}".format(self.NAME, folder))

        Repo.clone_from(repository, folder)
        self.logger.info("[{}] Downloaded the remote repository in the folder {}".format(self.NAME, folder))
