/*
fileList_indexer.c


FileSearcher: 
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


// This function is used to check if the given string matches the given pattern. It can handle regular search and wildcard search(*, ?, [], !, -, #).
// * Matches any number of characters. You can use the asterisk (*) anywhere in a character string.
// ? Matches a single alphabet in a specific position.
// [] Matches characters within the brackets.
// ! Excludes characters inside the brackets.
// - Matches a range of characters. Remember to specify the characters in ascending order (A to Z, not Z to A).
// # Matches any single numeric character.
// parameters:
//      pattern: the pattern to be matched; string
//      str: the string to be checked; string
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
// parameters:
//      path: the path of the file; string
//      name: the name of the file; string
char* formatResult(const char *path, const char *name) {
    // Calculate the size of the result string; using snprintf to calculate the size by passing NULL as the first argument and 0 as the second argument
    int size = snprintf(NULL, 0, "{\"path\": \"%s\", \"name\": \"%s\"}", path, name);
    char *result = (char *)malloc(size + 1);
    if (result) {
        snprintf(result, size + 1, "{\"path\": \"%s\", \"name\": \"%s\"}", path, name);
    }
    return result;
}

// This function recursively search for files and their path in the root directory and its subdirectories given the starting path and search string.
// It can handle regular search and wilecard search(*, ?, [], !, -, #).
// parameters:
//      path: the starting path; string
//      searchString: the search string; string
//      result: the address of the result string; string
void searchFiles(const char *path, const char *searchString, char **result) {
    // dir is a pointer to the directory
    // entry is a pointer to the directory entry for each file and subdirectory
    DIR *dir;
    struct dirent *entry;

    // Open directory
    // return if cannot open directory
    if ((dir = opendir(path)) == NULL) {
        perror("opendir");
        return;
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
            if (matchesWildcard(searchString, entry->d_name) || strcasestr(entry->d_name, searchString) != NULL) {
                char *formatted = formatResult(path, entry->d_name);
                // check if the result string is empty
                if (formatted) {
                    //*result = realloc(*result, (strlen(*result) + strlen(formatted) + 2) * sizeof(char));
                    char * new_result = realloc(*result, (strlen(*result) + strlen(formatted) + 2) * sizeof(char));
                    if (new_result == NULL) {
                        // Handle memory allocation failure
                        free(result); // Free the old memory
                        return;
                    }
                    *result = new_result;
                    strcat(*result, formatted);
                    strcat(*result, ", ");
                }
                free(formatted);
            }
        }
    }
    closedir(dir);
}

// This function is called to search for files and their path in the root directory and its subdirectories given the starting path and search string. 
// parameters:
//      path: the starting path; string
//      searchString: the search string; string
char *FileSearcher(const char *path, const char *searchString)
{
    // declare result string for storing the output
    char *result = malloc(2 * sizeof(char));
    //char *result = calloc(2, sizeof(char));
    strcpy(result, "[");

    // recursive call to searchFiles function
    searchFiles(path, searchString, &result);

    // delete the last comma and end the string with ]
    result[strlen(result) - 2] = '\0';


    char * new_result = realloc(result, (strlen(result) + 4) * sizeof(char));
    if (new_result == NULL) {
        // Handle memory allocation failure
        free(result); // Free the old memory
        return NULL;
    }
    result = new_result;
    strcat(result, "]");
    return result;
}

void FreeMemory(void *ptr) {
    printf("Freeing memory\n");
    printf("ptr: %p\n", ptr);
    free(ptr);
    printf("Memory freed\n");
    return; 
}

