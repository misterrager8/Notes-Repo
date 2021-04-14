# Git

## Basic Usage

- History (local repo) - all files in the git directory. Committing moves tracked changes from the stage to the directory
    - HEAD points to latest commit of the chosen branch
- Stage (index) - where changes are tracked
- Working directory - area where work is done. Changes are not tracked until you explicitly specify with the `git add` command. This command adds files to the staging area where all changes are tracked.
    - `git add .` stages all files
- Basic commands:
    - `git add files` - adds files to the stage
    - `git commit` - basically a “snapshot”, saves changes to git local repo
        - `git commit —amend` replaces one commit with a new commit
    - `git reset — files` - reverse commits of certain file, moves back to stage
        - `git reset` reverses commits of all files
    - `git checkout — files` - undo all local changes. Can be used to switch branches, or create new branches

![](http://marklodato.github.io/visual-git-guide/basic-usage.svg)

- Cherry pick - copies a commit from one branch to another
- Merge - commit that incorporates changes from another commit without changing the history of either branch.
- Rebase - does what a merge does, but instead cherry picks the commits of the selected branch and “pastes” them to the end of the other branch. Instead of two converging branches, it is just one long line of commits

![](https://i.stack.imgur.com/fb6L4.png)

- Stash - basically a temporary commit that “stashes” local changes to prevent merge conflicts and allow pulls
- ***IMPORTANT***: The contents of files are not actually stored in the index (.git/index) or in commit objects. Instead, each file is stored in the object database (.git/objects) as a blob, identified by its SHA-1 hash.

## Sources

- [A Visual Git Reference](http://marklodato.github.io/visual-git-guide/index-en.html)
