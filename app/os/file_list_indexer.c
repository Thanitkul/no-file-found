/*
fileList_indexer.c

This program contains 2 functions:
    1. FileListFinder: 
        This function return all file and subdirectory in the given path, with type and name, in format [{"type": "type", "name": "name"}] .
        It works on both given any absolute path or relative path.
        It will return error message if the given path is not a directory.
    2. FileSearcher: 
        This function search for files and their path in the root directory and its subdirectories given the starting path and search string. It can handle regular search and wilecard search(*, ?, [], !, -, #).
        * Matches any number of characters. You can use the asterisk (*) anywhere in a character string.
        ? Matches a single alphabet in a specific position. 
        [] Matches characters within the brackets.
        ! Excludes characters inside the brackets.
        - Matches a range of characters. Remember to specify the characters in ascending order (A to Z, not Z to A).
        # Matches any single numeric character.

        The output format is in format [{"path": "path", "name": "name"}] .

Created by Phasit Thanitkul (Kane), 9 October 2023

*/

#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <ctype.h>

// This function return all file and subdirectory in the given path, with type and name, in format [{"type": "type", "name": "name"}] .
char* FileListFinder(const char *path)
{

    DIR *dir;
    struct dirent *de;

    // testing out on getting current working directory
    char cwd [128];
    getcwd(cwd, 128);
    printf("\n\nThe actual directory is: %s\n", cwd);

    printf("File List in %s\n", path);

    // opendir() returns a pointer of DIR type.
    dir = opendir(path);
    if (!dir)
    {
        printf("Error: Cannot open directory\n");
        return "Error: Cannot open directory\n";
    }
    
    // fileList is a string that will be returned. The memory is allocated dynamically; therefore, it will not overflow even if the files in the directory are too many.
    char *fileList = malloc(2 * sizeof(char));

    //print to fileList file name and file type that is in the given path in format [{type: type, name: name}]
    strcpy(fileList, "[");
    while ((de = readdir(dir)) != NULL)
    {
        fileList = realloc(fileList, (strlen(fileList) + 20) * sizeof(char));
        strcat(fileList, "{\"type\": ");

        fileList = realloc(fileList, (strlen(fileList) + 25) * sizeof(char));
        if (de->d_type == DT_REG)
        {
            strcat(fileList, "\"file\", \"name\": ");
        }
        else if (de->d_type == DT_DIR)
        {
            strcat(fileList, "\"directory\", \"name\": ");
        }
        else
        {
            strcat(fileList, "\"unknown\", \"name\": ");
        }
        // add '' to file name
        char *temp = malloc((strlen(de->d_name) + 3) * sizeof(char));
        strcpy(temp, "\"");
        strcat(temp, de->d_name);
        strcat(temp, "\"");
        fileList = realloc(fileList, (strlen(fileList) + strlen(temp) + 5) * sizeof(char));
        strcat(fileList, temp);
        free(temp);
        strcat(fileList, "}, ");
    }

    //delte the last comma and end the string with ]
    fileList[strlen(fileList) - 2] = '\0';
    fileList = realloc(fileList, (strlen(fileList) + 2) * sizeof(char));
    strcat(fileList, "]");

    // Close directory
    closedir(dir);

    return fileList;
    free(fileList);
}

// This function is used to check if the given string matches the given pattern. It can handle regular search and wilecard search(*, ?, [], !, -, #).
// * Matches any number of characters. You can use the asterisk (*) anywhere in a character string.
// ? Matches a single alphabet in a specific position.
// [] Matches characters within the brackets.
// ! Excludes characters inside the brackets.
// - Matches a range of characters. Remember to specify the characters in ascending order (A to Z, not Z to A).
// # Matches any single numeric character.
bool matchesWildcard(const char *pattern, const char *str) {
    while (*pattern != '\0') {
        if (*pattern == '*') {
            // Handle asterisk: match any number of characters
            pattern++;
            while (*str != '\0' && !matchesWildcard(pattern, str)) {
                str++;
            }
        } else if (*pattern == '?') {
            // Handle question mark: match any single alphabet
            if (*str < 'A' || (*str > 'Z' && *str < 'a') || *str > 'z') {
                return false;
            }
            pattern++;
            str++;
        } else if (*pattern == '[') {
            // Handle bracket expression
            bool inclusive = true;
            if (*(pattern + 1) == '!') {
                inclusive = false;
                pattern += 2;
            } else {
                pattern++;
            }

            bool match = false;
            while (*pattern != ']' && *pattern != '\0') {
                if (*pattern == '-' && *(pattern + 1) != '\0' && *(pattern + 2) == ']') {
                    // Handle character range (e.g., [A-Z])
                    char start = *(pattern - 1);
                    char end = *(pattern + 1);
                    if (*str >= start && *str <= end) {
                        match = true;
                        break;
                    }
                    pattern += 3;
                } else if (*str == *pattern) {
                    // Handle single character match
                    match = true;
                    break;
                }
                pattern++;
            }

            if ((inclusive && !match) || (!inclusive && match)) {
                return false;
            }

            while (*pattern != ']' && *pattern != '\0') {
                pattern++;
            }

            if (*pattern == ']') {
                pattern++;
            }

            str++;
        } else if (*pattern == '#') {
            // Handle numeric character
            if (*str < '0' || *str > '9') {
                return false;
            }
            pattern++;
            str++;
        } else {
            // Handle regular character
            if (*pattern != *str) {
                return false;
            }
            pattern++;
            str++;
        }
    }

    return (*str == '\0');
}

// This function is used to format the result in format {"path": "path", "name": "name"}.
char* formatResult(const char *path, const char *name) {
    int size = snprintf(NULL, 0, "{\"path\": \"%s\", \"name\": \"%s\"}", path, name);
    char *result = (char *)malloc(size + 1);
    if (result) {
        snprintf(result, size + 1, "{\"path\": \"%s\", \"name\": \"%s\"}", path, name);
    }
    return result;
}

// This function recursively search for files and their path in the root directory and its subdirectories given the starting path and search string. It can handle regular search and wilecard search(*, ?, [], !, -, #).
void searchFiles(const char *path, const char *searchString, char **result) {
    DIR *dir;
    struct dirent *entry;

    // Open directory
    // return if cannot open directory
    if ((dir = opendir(path)) == NULL) {
        perror("opendir");
        return ;
    }

    // Loop through all files and directories in the directory
    while ((entry = readdir(dir)) != NULL) {
        // if the entry is a directory, recursively call the function with the new path
        if (entry->d_type == DT_DIR) {
            // Skip . and ..
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;
            char *new_path = malloc((strlen(path) + strlen(entry->d_name) + 2) * sizeof(char));
            strcpy(new_path, path);
            strcat(new_path, "/");
            strcat(new_path, entry->d_name);
            searchFiles(new_path, searchString, result);
            free(new_path);
        } else {
            // check if the file name matches the search string
            if (matchesWildcard(searchString, entry->d_name) || strcasecmp(entry->d_name, searchString) == 0) {                
                char *formatted = formatResult(path, entry->d_name);
                if (formatted) {
                    *result = realloc(*result, (strlen(*result) + strlen(formatted) + 2) * sizeof(char));
                    strcat(*result, formatted);
                    strcat(*result, ", ");
                    free(formatted);
                }
            }
        }
    }

    closedir(dir);
}

// This function is called to search for files and their path in the root directory and its subdirectories given the starting path and search string. It can handle regular search and wilecard search(*, ?, [], !, -, #).
char *FileSearcher(const char *path, const char *searchString)
{
    printf("Searching for %s in %s\n", searchString, path);

    // declare result string for storing the output
    char *result = malloc(2 * sizeof(char));
    strcpy(result, "[");

    // recursive call to searchFiles function
    searchFiles(path, searchString, &result);

    // delete the last comma and end the string with ]
    result[strlen(result) - 2] = '\0';
    result = realloc(result, (strlen(result) + 2) * sizeof(char));
    strcat(result, "]");

    return result;
    free(result);
}