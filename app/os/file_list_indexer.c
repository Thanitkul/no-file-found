/*
fileList_indexer.c

This program contains 2 functions:
    1. FileListFinder: 
        This function return all file and subdirectory in the given path, with type and name, in format [{"type": "type", "name": "name"}] .
        It works on both given any absolute path or relative path.
        It will return error message if the given path is not a directory.
    2. FileSeacher: TODO

Created by Phasit Thanitkul (Kane), 9 October 2023

*/

#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

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

