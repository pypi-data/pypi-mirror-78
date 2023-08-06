# `rcl` - A simple command line wrapper for `rclone`.

`rcl` is a simple command line wrapper for [rclone](https://rclone.org/) focused on easy folder syncing. It is loosely based on [git's interface](https://git-scm.com/docs) and therefore uses the concepts of *"local"* and *"remote"* along with having commands such as `pull`, `push` and `diff`.  

Feel free to raise any [issues](https://github.com/Ben-Ryder/rcl/issues/new?assignees=Ben-Ryder&labels=bug&template=bug-report.md&title=), suggest [improvements](https://github.com/Ben-Ryder/rcl/issues/new?assignees=Ben-Ryder&labels=improvement&template=improvement.md&title=) and [features](https://github.com/Ben-Ryder/rcl/issues/new?assignees=Ben-Ryder&labels=feature&template=feature-request.md&title=) or fork and contribute.

## Requirements
`rcl` only acts as a wrapper around `rclone`, you therefore must first [install](https://rclone.org/install/) and [configure](https://rclone.org/docs/) rclone and ensure that it is properly accessible on your `PATH`.


## Installation
`rcl` is available on [PyPI](https://pypi.org/project/rcl/) and can be installed by running `pip install rcl`.

**Note**: *It is possible that pip will warn you that the install location is not on your`$PATH`. If so, `rcl` may not be found until you add the directory shown in the warning to your `$PATH`.*


## Usage
To use `rcl` you add entries which consist of local/remote folder pairs. You can then interact with these entries like they're a connected system.  

The folder values you add to entries will directly match what rclone uses and should conform to [rclone's interface](https://rclone.org/docs/#usage) of:  
- Local Folder: `/local/path/to/folder`   
- Remote Folder: `remote:path/to/folder`  


### Commands
| Command | Explanation |
| --- | --- |
| `rcl` / `rcl --help` | Outputs the help and a list of commands. |
| `rcl add <entry_id> <local_folder> <remote_folder>` | Add a new entry, identified by `<entry_id>`. |
| `rcl diff <entry_id>` | Show the difference between the local and remote folder. |  
| `rcl list` | List all entries. |
| `rcl pull <entry_id> [--dry]` | Pull remote changes to your local. (Sync local to match remote). |
| `rcl push <entry_id> [--dry]` | Push local changes to the remote. (Sync remote to match local). |
| `rcl rm <entry_id>` | Remove an entry.  |


### Examples
| Example | Explanation |
| --- | --- |
| `rcl add music /home/user/Music gdrive:Music` | Add a new "music" entry linking the default Linux Music folder with a top-level "Music" folder in a remote called "gdrive". |
| `rcl push music` | Push local changes to the remote. (Sync remote with local). |
| `rcl pull music` | Pull remote changes to your local. (Sync local with remote). |
| `rcl rm music` | Remove the "music" entry. |


### Notes  
- `push` and `pull` can both be run with the `--dry` flag which will add `--dry-run` to the rclone command.
- `push` and `pull` automatically add the `--progress` flag to the rclone command.
- `rcl` can be run from any directory as it will always run rclone using the local/remote folders from the entry specified.


## Current Limitations
- Opinionated - This wrapper offers a simple interface for specific aspects of syncing I use.
- Manual External Setup - rclone still has to be setup externally prior to use.
- No Input vAl1dation - None of the values supplied to the `add` command are validated in any way.
- Error Handling - There is some python error handling on `rcl rm` but nothing protecting against invalid inputs to `rcl add` or rclone errors.  

## License
`rcl` is release under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license so you can use and adapt as you wish.
