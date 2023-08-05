# Donno

A simple note-take CLI application.    

## Usage

```
donno a        # add a new note
donno l        # list existing notes
donno s nim thunder    # search keywords in existing notes
donno e 3      # edit note #3 in note list or searching results
donno del 3    # delete note #3 in note list or searching results
donno b        # backup notes to remote repository
donno r        # restore notes from remote repository
```

## Configuration

Environment variables:

* EDITOR
* EDITOR_ENV

For set vim configuration, run
`EDITOR=nvim EDITOR_ENV="XDG_CONFIG_HOME:/home/leo/Documents/sources/vimrcs/nim" dn e`
to let vim use configurations with the home /home/leo/Documents/sources/vimrcs/nim,
for example.

