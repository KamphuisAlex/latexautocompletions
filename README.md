# latexautocompletions
LaTeX Autocompletions for sublime text generated from CWL files

This repository provides:

1. A .sublime-completions file that has many completions premade for you to use
2. A collection of CWL files that you can use as input for autocompletions
3. Python code to convert CWL files to a sublime text .sublime-completions file

## To use the premade completions
download the file *latexCompletes.sublime-completions* and put it in the packages folder for your sublime distribution. You can find this folder via Preferences > browse packages. It is a good idea to place the completion file in the *User* folder.

For a more intuitive behaviour you need unset the character '\' as word separator. The best place to do this is in your syntax specific settings:

- open a .tex file
- preferences > settings - more > syntax specific
- add the following line: "word_separators": "./()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?",

You should be done without restarting sublime, enjoy.

## To use the CWL files that I collected
Clone or download the CWL files. You can for instance put them in your TexStudio autocomplete folder for more autocompletions!

## To use the python code to make your own completions
Download the src folder. Put the CWL files that you want to use as input in the same folder as the python source. Run *convert_cwl_to_snippet.py*. It will generate a .sublime-completions file with all commands in your CWL files.

Note that not all CWL properties can be directly translated to sublime completions. All info is parsed, but not everything is used.