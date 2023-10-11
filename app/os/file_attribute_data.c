/*
file_attribute_data.c

This function return file properties(name, path, size, last modified time) in format {"name": "name", "path": "path", "size": "size", "last_modified_time": "last_modified_time"}.

size of file is in bytes.

Created by Phasit Thanitkul (Kane), 11 October 2023

*/



#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>

// this function return file properties(name, path, size, last modified time) in format {"name": "name", "path": "path", "size": "size", "last_modified_time": "last_modified_time"}.
char *GetFileAttribute(const char *path)
{
    
    struct stat fileStat;

    // check if file exist
    if (stat(path, &fileStat) < 0)
    {
        printf("Error: Cannot open file\n");
        return "Error: Cannot open file";
    }

    //check if path is a directory, if it is, return error
    if (S_ISDIR(fileStat.st_mode))
    {
        printf("Error: Cannot open directory\n");
        return "Error: Cannot open directory, please enter a file path";
    }

    // extract file name from path
    char fileName[512];
    for (int i = strlen(path) - 1; i >= 0; i--)
    {
        if (path[i] == '/')
        {
            strcpy(fileName, path + i + 1);
            break;
        }
    }

    // extract file size from fileStat
    double size = fileStat.st_size;
    
    // extract last modified time from fileStat
    struct tm dt = *(gmtime(&fileStat.st_mtime));



    
     // fileAttribute is a string that will be returned. The memory is allocated dynamically; therefore, it will not overflow even if the files in the directory are too many.
    char *fileAttribute = malloc(10 * sizeof(char));

    //print to fileAttribute file name and file type that is in the given path in format {"name": "name", "path": "path", "size": "size", "last_modified_time": "last_modified_time"}  
    strcpy(fileAttribute, "{\"name\": ");

    fileAttribute = realloc(fileAttribute, (strlen(fileAttribute) + strlen(fileName) + 20) * sizeof(char));
    strcat(fileAttribute, "\"");
    strcat(fileAttribute, fileName);
    strcat(fileAttribute, "\", \"path\": ");

    fileAttribute = realloc(fileAttribute, (strlen(fileAttribute) + strlen(path) + 20) * sizeof(char));
    strcat(fileAttribute, "\"");
    strcat(fileAttribute, path);
    strcat(fileAttribute, "\", \"size\": ");

    char *temp = malloc(20 * sizeof(char));
    sprintf(temp, "%f", size);
    fileAttribute = realloc(fileAttribute, (strlen(fileAttribute) + strlen(temp) + 30) * sizeof(char));
    strcat(fileAttribute, temp);
    free(temp);
    strcat(fileAttribute, ", \"last_modified_time\": ");

    temp = malloc(20 * sizeof(char));
    //store last modified time in format dd-mm-yyyy hh:mm:ss
    sprintf(temp, "%d-%d-%d %d:%d:%d", dt.tm_mday, dt.tm_mon, dt.tm_year + 1900, dt.tm_hour, dt.tm_min, dt.tm_sec);
    fileAttribute = realloc(fileAttribute, (strlen(fileAttribute) + strlen(temp) + 5) * sizeof(char));
    strcat(fileAttribute, "\"");
    strcat(fileAttribute, temp);
    free(temp);
    strcat(fileAttribute, "\"}");

    return fileAttribute;
    free(fileAttribute);
}
