#####################################################
# Property by Your Engineering Solutions (Y.E.S.)   #
# Engineers: Lorans Hirmez, Brandon Fong            #
#####################################################

# How to test if a file/directory exists https://www.guru99.com/python-check-if-file-exists.html & https://stackabuse.com/creating-and-deleting-directories-with-python/
# How to create a file https://www.guru99.com/reading-and-writing-files-in-python.html

# Current Workflow:
# 1. Creates file
# 2. Calls a function to write into a file
# 3. Calles a function to close the file
# I.E. Init_File() -> Inject_Data() -> Close_File() 

### LIBRARIES ###
from System import Client
from zipfile import ZipFile
from XML import xmlreader
import datetime
import os
import System
import shutil

FTPDir = xmlreader.string('DirectoryForOutboundFTPFiles'); # defines where the file will be imported
LogForMaxPowerDir = xmlreader.string('DirectoryForMaxPowerLogFiles'); # defines where the file will be imported
FTPArchiveDir = xmlreader.string('ArchiveForOutboundFTPFiles'); # defines where the file will be imported
LOGArchiveDir = xmlreader.string('ArchiveForMaxPowerLogFiles');
FTPFileType = xmlreader.string('FileTypeForFTP');
LOGFileType = xmlreader.string('FileTypeForLogs');
ZipExtension = xmlreader.string('FileTypeForZippedFolder');


def MakeDir(makepath):
    if(not (os.path.isdir(makepath))): # if that directory doesn't exist, create it
            try:
                os.mkdir(makepath) # mkdir cmd 
            except OSError:
                print("\nCreation of the directory %s failed" % makepath); # Unsuccessful
            else:
                print("\nSuccessfully created the directory %s " % makepath); # Successful
    else:
        print("\nDirectory %s already exits.\n" % makepath);

# Meant to write into files that are ready for FTP
class File_Handler:
    def Init_File(): # function to create a file

        Date_and_Time = datetime.datetime.now(); # gets current date and time
        MakeDir(FTPDir);

        # Creates the file to be injected by our power tracker
        # This will be sent through FTP via script to our remote server
        filename = FTPDir + "/maxpower_" + Date_and_Time.strftime("%m%d%Y_%H%M%S") + FTPFileType; 
        try:
            System.File = open(filename,"w+"); # this file is global
        except OSError:
            print("Creation of file %s failed." % filename);
            return 1;
        else:
            print("Successfully created file: %s" % filename);
            return 0;

    def Inject_Data(wind_data, solar_data):
        Date_and_Time = datetime.datetime.now(); # gets current date and time
        try:
            System.File.write("{}, {}, {}, {}\n" .format(Client.ID,
                Date_and_Time.strftime("%Y-%m-%d %H:%M:%S"), wind_data, solar_data));
        except OSError:
            print("\nWriting of file failed\n");
            return 1;
        except AttributeError as ex:
            print("in file");
            print(ex);
        else:
            print("\nWriting successful\n");
            return 0;

    def Close_File():
        System.File.close();
        System.File = 0; # clear variable

# This is meant for debugging purposes
# When you don't have the terminal up, you can view the logs to check the outputs
class Log_Handler:
    def Init_File(): # function to create a file

        Date_and_Time = datetime.datetime.now(); # gets current date and time
        MakeDir(LogForMaxPowerDir);

        # Creates the file to be injected by our power tracker
        # This will be sent through FTP via script to our remote server
        filename = LogForMaxPowerDir +  "/MaxPowerLog_" + Date_and_Time.strftime("%m%d%Y_%H%M%S") + LOGFileType;
        try:
            System.Log = open(filename,"w+"); # this file is global
        except OSError:
            print("\nCreation of file %s failed." % filename);
            return 1;
        else:
            print("\nSuccessfully created file: %s" % filename);
            return 0;

    def Write_Log(string):
        try:
            System.Log.write(string);
        except OSError:
            print("\nWriting log failed\n");
            return 1;
        except AttributeError as ex:
            print("in log");
            print(ex);
        else:
            return 0;

    def Close_File():
        System.Log.close();
        System.Log = 0; # clear variable
        print("\nMaintenance check in \\logs\\MaxPower.  Delete files if space is needed");
        

# Moves files into an archive folder and zips it up when it is past a certain number of files
class Archive_Handler:
    def ArchiveFiles():

        MakeDir(FTPArchiveDir);
        MakeDir(LOGArchiveDir);

        # In FTP Folder
        FTPFiles = os.listdir(FTPDir);
        for f in FTPFiles:
            if f.endswith(FTPFileType):
                FilePath = FTPDir + "/" + f;
                shutil.move(FilePath, FTPArchiveDir);
                print("\nMoved %s to archive folder\n" % f);

        # In logs\MaxPower Folder
        LOGFiles = os.listdir(LogForMaxPowerDir);
        for f in LOGFiles:
            if f.endswith(LOGFileType):
                FilePath = LogForMaxPowerDir + "/" + f;
                shutil.move(FilePath, LOGArchiveDir);
                print("\nMoved %s to archive folder\n" % f);

        # Checks archive folder to zip
        # Note you need 7z to unzip the zip file on windows
        # TODO test linux environment

        # In FTP archive Folder
        FTPArchivedFiles = os.listdir(FTPArchiveDir);
        if (FTPArchivedFiles.__len__()) > 10:
            print("\nBeginning to zip files in %s\n" % FTPArchiveDir)
            filename = FTPArchiveDir +  "/Archive_" + datetime.datetime.now().strftime("%m%d%Y_%H%M%S") + ZipExtension; 
            zipper = ZipFile(filename, 'w');
            for f in FTPArchivedFiles:
                if f.endswith(FTPFileType):
                    FilePath = FTPArchiveDir + "/" + f;
                    zipper.write(FilePath);
                    os.remove(FilePath);
            zipper.close();
            print("\nZipped files in %s\n" % FTPArchiveDir);
            
        # In logs\MaxPower archive Folder
        LOGArchivedFiles = os.listdir(LOGArchiveDir);
        if (LOGArchivedFiles.__len__()) > 10:
            print("\nBeginning to zip files in %s\n" % LOGArchiveDir)
            filename = LOGArchiveDir +  "/Archive_" + datetime.datetime.now().strftime("%m%d%Y_%H%M%S") + ZipExtension; 
            zipper = ZipFile(filename, 'w');
            for f in LOGArchivedFiles:
                if f.endswith(LOGFileType):
                    FilePath = LOGArchiveDir + "/" + f;
                    zipper.write(FilePath);
                    os.remove(FilePath);
            zipper.close();
            print("\nZipped files in %s\n" % LOGArchiveDir);
        