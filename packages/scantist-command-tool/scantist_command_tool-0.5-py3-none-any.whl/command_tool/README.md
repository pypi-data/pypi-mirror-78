# Manual

## Install
pip install scantist-command-tool
scantist_cmd
scantist_auth

## Authentication
- Login and save credentials
    
        scantist_auth -b $baseurl -e $email -p $password
- Set up base url and apikey:

        scantist_auth -b $base_url -a apikey

- Register a new user and set up everything

        scantist_auth -b $base_url -e $email -p $password -c


## Binary Scan
- scantist_cmd -t binary -f $local_file_path 

- optional parameter: 
        
        -r [csv|pdf]: download scan report
        
        -v          : set the version of the project
        
        -p          : set the project name. if this parameter is null, will use file name as project name
        
        -j          : project id.
        
        -h          : report output path. Default path is current working directory.
        
file + version -> create new project, name by file.【if duplicate name project exist, will update the project】

file + version + project_name -> create new project, name by the project_name.

local_binary_file + version + project_id -> create new version of existing project.

project_id -> scan existing project.

## Source code scan
- scantist_cmd -t source_code -f $local_file_path 

- optional parameter :

        -r [csv|pdf]: download scan report
        
        -h          : report output path. Default path is current working directory.
        
        -b          : trigger source code scan with bom-detect. Otherwise, upload file and remotely trigger build and scan.
         
## List user projects
- scantist_cmd -l


## Download scan result
Generate and download the most recent scan report if no $project_id given
- scantist_cmd -r ["csv"|"pdf"]

- optional parameter:

        -j  : project id.



