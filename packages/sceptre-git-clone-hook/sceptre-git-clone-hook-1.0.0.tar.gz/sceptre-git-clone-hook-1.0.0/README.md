# Git Clone

This package is a Sceptre Hook to clone a git repository. It executes two actions:

* removes, if exists, the current folder that you have passed
* clones the git repository that you have passed, in that folder

## Installation

```bash
git clone https://github.com/bilardi/sceptre-git-clone-hook
cd sceptre-git-clone-hook
make plugin TARGET=<relative_path_of_existing_sceptre_project_root>
```

## Syntax

You have to pass two parameters:

* the **git repository url** can have the follow protocols: http, https or git
* the local **repository folder** is a relative path from your Sceptre project root where you want to clone the repository

You can clone more git repositories using the syntax below for each git repository you need

```yaml
<hook_point>:
  - !git_clone <git repository url> <repository folder>
```

or you can clone one git repository and save the details in the property named **sceptre_user_data**, for using them in other steps

```yaml
<hook_point>:
  - !git_clone
sceptre_user_data:
    GitRepository: <git repository url>
    RepositoryFolder: <repository folder>
```

## Example

For cloning one repository before create the stack

```yaml
before_create:
  - !git_clone https://github.com/bilardi/sceptre-git-clone-hook my-folder
```

for cloning two different repositories before create the stack

```yaml
before_create:
  - !git_clone https://github.com/bilardi/sceptre-git-clone-hook my-folder-one
  - !git_clone https://github.com/bilardi/sceptre-zip-code-s3 my-folder-two
```

or for cloning one repository before create the stack and sharing the details with other steps

```yaml
before_create:
  - !git_clone
sceptre_user_data:
    GitRepository: https://github.com/bilardi/sceptre-git-clone-hook
    RepositoryFolder: my-folder
```

## Development

```bash
# after your change
python3 -m pytest tests/test_git_clone.py
git add .
git commit
bumpversion --dry-run --verbose patch|minor|major
bumpversion patch|minor|major
git push origin master
git push origin vX.Y.Z
```