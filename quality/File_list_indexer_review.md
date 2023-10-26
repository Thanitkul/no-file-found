For all functions: Non of the comments above the functions have a line explaining the detail of each arguments that is passed through the function. This violates our coding standards.

Line 236:
```
// This function is called to search for files and their path in the root directory and its subdirectories given the starting path and search string. It can handle regular search and wilecard search(*, ?, [], !, -, #).
char *FileSearcher(const char *path, const char *searchString)
{
    ...
}
```
The text comment is too long to fit in 1 line and should enter a new line after a few words.

Line 195:
```
// This function recursively search for files and their path in the root directory and its subdirectories given the starting path and search string. It can handle regular search and wilecard search(*, ?, [], !, -, #).
void searchFiles(const char *path, const char *searchString, char **result) {
```
This comment is also too long to fit within 1 line and should have a new line after the first sentence.

Line 196:
```
    DIR *dir;
    struct dirent *entry;
```
The variable names are too vague and the team members do not understand the purpose of the variables, there should be a comment explaining it

Line 203:
```
if ((dir = opendir(path)) == NULL) {
        perror("opendir");
        return ;
    }
```
There is a trailing whitespace after the return.

Line 100:
```

// This function is used to check if the given string matches the given pattern. It can handle regular search and wilecard search(*, ?, [], !, -, #).
```
Wildcard is misspelled 

Line 185:
```
char* formatResult(const char *path, const char *name) {
    int size = snprintf(NULL, 0, "{\"path\": \"%s\", \"name\": \"%s\"}", path, name);
    char *result = (char *)malloc(size + 1);
    if (result) {
        snprintf(result, size + 1, "{\"path\": \"%s\", \"name\": \"%s\"}", path, name);
    }
    return result;
}
```
The function names are unclear ("snprintf") and the team members do not understand the purpose of the code.
The variable name "size" seems to indicate that its storing some sort of a counter but the snprintf seems to be a printing command.
He explains that by passing NULL and 0 into the arguments, it will eject out the string length, which is kinda of a hacky method to do this.

Line 187: malloc is called but the memory does not get free'd which could cause a memory leak. It is unclear when the memory should be freed.

Line 203:
```
        return ;
```
Trailing whitespace

Line 223:
```
                if (formatted) {
```
The if condition is unclear what it's checking for, since the variable is a char * type

Line 224:
```
if (formatted) {
                    *result = realloc(*result, (strlen(*result) + strlen(formatted) + 2) * sizeof(char));
                    strcat(*result, formatted);
                    strcat(*result, ", ");
                    free(formatted);
                }
```
After the realloc, it does not check whether it returns a NULL pointer which may cause an error.