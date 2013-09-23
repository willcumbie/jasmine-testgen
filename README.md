To install:

Clone the repository into your sublime-text-2/Packages directory. The package will add the command `Jasmine: Open Jasmine Spec`.

To use:
Run the `Jasmine: Open Jasmine Spec` command from a JavaScript file. This command will search for a corresponding "spec" file; if that file does not exist, it will open a new file at that location and fill that file with a basic spec template. Once that spec template has been created, it will prompt you for a test title, which will be used to create an `it("")` statement within the test. It will continue prompting for and creating these tests until it is given a blank statement.
