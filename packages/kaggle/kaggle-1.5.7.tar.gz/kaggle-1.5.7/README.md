# Kaggle API

Official API for https://www.kaggle.com, accessible using a command line tool implemented in Python 3.

Beta release - Kaggle reserves the right to modify the API functionality currently offered.

IMPORTANT: Competitions submissions using an API version prior to 1.5.0 may not work.  If you are encountering difficulties with submitting to competitions, please check your version with `kaggle --version`.  If it is below 1.5.0, please update with `pip install kaggle --upgrade`.

## Installation

Ensure you have Python 3 and the package manager `pip` installed.

Run the following command to access the Kaggle API using the command line:

`pip install kaggle` (You may need to do `pip install --user kaggle` on Mac/Linux.  This is recommended if problems come up during the installation process.) Installations done through the root user (i.e. `sudo pip install kaggle`) will not work correctly unless you understand what you're doing.  Even then, they still might not work.  User installs are strongly recommended in the case of permissions errors.

You can now use the `kaggle` command as shown in the examples below.

If you run into a `kaggle: command not found` error, ensure that your python binaries are on your path.  You can see where `kaggle` is installed by doing `pip uninstall kaggle` and seeing where the binary is.  For a local user install on Linux, the default location is `~/.local/bin`.  On Windows, the default location is `$PYTHON_HOME/Scripts`.

IMPORTANT: We do not offer Python 2 support.  Please ensure that you are using Python 3 before reporting any issues.

## API credentials

To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. Then go to the 'Account' tab of your user profile (`https://www.kaggle.com/<username>/account`) and select 'Create API Token'. This will trigger the download of `kaggle.json`, a file containing your API credentials. Place this file in the location `~/.kaggle/kaggle.json` (on Windows in the location `C:\Users\<Windows-username>\.kaggle\kaggle.json` - you can check the exact location, sans drive, with `echo %HOMEPATH%`). You can define a shell environment variable `KAGGLE_CONFIG_DIR` to change this location to `$KAGGLE_CONFIG_DIR/kaggle.json` (on Windows it will be `%KAGGLE_CONFIG_DIR%\kaggle.json`).

For your security, ensure that other users of your computer do not have read access to your credentials. On Unix-based systems you can do this with the following command:

`chmod 600 ~/.kaggle/kaggle.json`

You can also choose to export your Kaggle username and token to the environment:

```bash
export KAGGLE_USERNAME=datadinosaur
export KAGGLE_KEY=xxxxxxxxxxxxxx
```
In addition, you can export any other configuration value that normally would be in
the `$HOME/.kaggle/kaggle.json` in the format 'KAGGLE_<VARIABLE>' (note uppercase).
For example, if the file had the variable "proxy" you would export `KAGGLE_PROXY`
and it would be discovered by the client.

## Commands
<div class="document">

<div class="documentwrapper">

<div class="bodywrapper">

<div class="body" data-role="main">

<div class="highlight-default notranslate">

<div class="highlight">

    usage: kaggle [-h] [-v] {competitions,c,datasets,d,kernels,k,config} ...

</div>

</div>

<div id="Named Arguments" class="section">

# Named Arguments[¶](#Named%20Arguments "Permalink to this headline")

  - \-v, --version  
    show program’s version number and exit

</div>

<div id="commands" class="section">

# commands[¶](#commands "Permalink to this headline")

  - command  
    Possible choices: competitions, c, datasets, d, kernels, k, config
    
    Use one of: competitions {list, get, files, download, submit,
    submissions, leaderboard} datasets {list, files, download, create,
    version, init, metadata, status} config {view, set,
unset}

</div>

<div id="Sub-commands:" class="section">

# Sub-commands:[¶](#Sub-commands: "Permalink to this headline")

<div id="competitions (c)" class="section">

## competitions (c)[¶](#competitions%20\(c\) "Permalink to this headline")

Commands related to Kaggle competitions

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle competitions [-h]
                        {list,get,files,download,submit,submissions,leaderboard}
                        ...

</div>

</div>

<div id="commands_repeat1" class="section">

### commands[¶](#commands_repeat1 "Permalink to this headline")

  - command  
    Possible choices: list, get, files, download, submit, submissions,
    leaderboard

</div>

<div id="Sub-commands:_repeat1" class="section">

### Sub-commands:[¶](#Sub-commands:_repeat1 "Permalink to this headline")

<div id="list" class="section">

#### list[¶](#list "Permalink to this headline")

List available competitions

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle competitions list [-h] [--group GROUP] [--category CATEGORY]
                             [--sort-by SORT_BY] [-p PAGE] [-s SEARCH] [-v]

</div>

</div>

<div id="Named Arguments_repeat1" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat1 "Permalink to this headline")

  - \--group  
    Search for competitions in a specific group. Default is ‘general’.
    Valid options are ‘general’, ‘entered’, and ‘inClass’

  - \--category  
    Search for competitions of a specific category. Default is ‘all’.
    Valid options are ‘all’, ‘featured’, ‘research’, ‘recruitment’,
    ‘gettingStarted’, ‘masters’, and ‘playground’

  - \--sort-by  
    Sort list results. Default is ‘latestDeadline’. Valid options are
    ‘grouped’, ‘prize’, ‘earliestDeadline’, ‘latestDeadline’,
    ‘numberOfTeams’, and ‘recentlyCreated’

  - \-p, --page  
    Page number for results paging. Page size is 20 by default
    
    Default: 1

  - \-s, --search  
    Term(s) to search for

  - \-v, --csv  
    Print results in CSV format (if not set print in table format)
    
    Default: False

</div>

</div>

<div id="files" class="section">

#### files[¶](#files "Permalink to this headline")

List competition
files

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle competitions files [-h] [-v] [-q] [competition]

</div>

</div>

<div id="Named Arguments_repeat2" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat2 "Permalink to this headline")

  - competition  
    Competition URL suffix (use “kaggle competitions list” to show
    options) If empty, the default competition will be used (use “kaggle
    config set competition”)”

  - \-v, --csv  
    Print results in CSV format (if not set print in table format)
    
    Default: False

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

</div>

</div>

<div id="download" class="section">

#### download[¶](#download "Permalink to this headline")

Download competition
    files

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle competitions download [-h] [-f FILE_NAME] [-p PATH] [-w] [-o] [-q]
                                 [competition]

</div>

</div>

<div id="Named Arguments_repeat3" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat3 "Permalink to this headline")

  - competition  
    Competition URL suffix (use “kaggle competitions list” to show
    options) If empty, the default competition will be used (use “kaggle
    config set competition”)”

  - \-f, --file  
    File name, all files downloaded if not provided (use “kaggle
    competitions files -c \<competition\>” to show options)

  - \-p, --path  
    Folder where file(s) will be downloaded, defaults to current working
    directory

  - \-w, --wp  
    Download files to current working path

  - \-o, --force  
    Skip check whether local version of file is up to date, force file
    download
    
    Default: False

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

</div>

</div>

<div id="submit" class="section">

#### submit[¶](#submit "Permalink to this headline")

Make a new competition
    submission

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle competitions submit [-h] -f FILE_NAME -m MESSAGE [-q] [competition]

</div>

</div>

<div id="required arguments" class="section">

##### required arguments[¶](#required%20arguments "Permalink to this headline")

  - \-f, --file  
    File for upload (full path)

  - \-m, --message  
    Message describing this
submission

</div>

<div id="Named Arguments_repeat4" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat4 "Permalink to this headline")

  - competition  
    Competition URL suffix (use “kaggle competitions list” to show
    options) If empty, the default competition will be used (use “kaggle
    config set competition”)”

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

</div>

</div>

<div id="submissions" class="section">

#### submissions[¶](#submissions "Permalink to this headline")

Show your competition
submissions

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle competitions submissions [-h] [-v] [-q] [competition]

</div>

</div>

<div id="Named Arguments_repeat5" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat5 "Permalink to this headline")

  - competition  
    Competition URL suffix (use “kaggle competitions list” to show
    options) If empty, the default competition will be used (use “kaggle
    config set competition”)”

  - \-v, --csv  
    Print results in CSV format (if not set print in table format)
    
    Default: False

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

</div>

</div>

<div id="leaderboard" class="section">

#### leaderboard[¶](#leaderboard "Permalink to this headline")

Get competition leaderboard information

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle competitions leaderboard [-h] [-s] [-d] [-p PATH] [-v] [-q]
                                    [competition]

</div>

</div>

<div id="Named Arguments_repeat6" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat6 "Permalink to this headline")

  - competition  
    Competition URL suffix (use “kaggle competitions list” to show
    options) If empty, the default competition will be used (use “kaggle
    config set competition”)”

  - \-s, --show  
    Show the top of the leaderboard
    
    Default: False

  - \-d, --download  
    Download entire leaderboard
    
    Default: False

  - \-p, --path  
    Folder where file(s) will be downloaded, defaults to current working
    directory

  - \-v, --csv  
    Print results in CSV format (if not set print in table format)
    
    Default: False

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

</div>

</div>

</div>

</div>

<div id="datasets (d)" class="section">

## datasets (d)[¶](#datasets%20\(d\) "Permalink to this headline")

Commands related to Kaggle datasets

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets [-h]
                    {list,files,download,create,version,init,metadata,status} ...

</div>

</div>

<div id="commands_repeat2" class="section">

### commands[¶](#commands_repeat2 "Permalink to this headline")

  - command  
    Possible choices: list, files, download, create, version, init,
    metadata,
status

</div>

<div id="Sub-commands:_repeat2" class="section">

### Sub-commands:[¶](#Sub-commands:_repeat2 "Permalink to this headline")

<div id="list_repeat1" class="section">

#### list[¶](#list_repeat1 "Permalink to this headline")

List available datasets

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets list [-h] [--sort-by SORT_BY] [--size SIZE]
                         [--file-type FILE_TYPE] [--license LICENSE_NAME]
                         [--tags TAG_IDS] [-s SEARCH] [-m] [--user USER] [-p PAGE]
                         [-v] [--max-size MAX_SIZE] [--min-size MIN_SIZE]

</div>

</div>

<div id="Named Arguments_repeat7" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat7 "Permalink to this headline")

  - \--sort-by  
    Sort list results. Default is ‘hottest’. Valid options are
    ‘hottest’, ‘votes’, ‘updated’, and ‘active’

  - \--size  
    DEPRECATED. Please use –max-size and –min-size to filter dataset
    sizes.

  - \--file-type  
    Search for datasets with a specific file type. Default is ‘all’.
    Valid options are ‘all’, ‘csv’, ‘sqlite’, ‘json’, and ‘bigQuery’.
    Please note that bigQuery datasets cannot be downloaded

  - \--license  
    Search for datasets with a specific license. Default is ‘all’. Valid
    options are ‘all’, ‘cc’, ‘gpl’, ‘odb’, and ‘other’

  - \--tags  
    Search for datasets that have specific tags. Tag list should be
    comma separated

  - \-s, --search  
    Term(s) to search for

  - \-m, --mine  
    Display only my items
    
    Default: False

  - \--user  
    Find public datasets owned by a specific user or organization

  - \-p, --page  
    Page number for results paging. Page size is 20 by default
    
    Default: 1

  - \-v, --csv  
    Print results in CSV format (if not set print in table format)
    
    Default: False

  - \--max-size  
    Specify the maximum size of the dataset to return (bytes)

  - \--min-size  
    Specify the minimum size of the dataset to return (bytes)

</div>

</div>

<div id="files_repeat1" class="section">

#### files[¶](#files_repeat1 "Permalink to this headline")

List dataset
files

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets files [-h] [-v] [dataset]

</div>

</div>

<div id="Named Arguments_repeat8" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat8 "Permalink to this headline")

  - dataset  
    Dataset URL suffix in format \<owner\>/\<dataset-name\> (use “kaggle
    datasets list” to show options)

  - \-v, --csv  
    Print results in CSV format (if not set print in table format)
    
    Default: False

</div>

</div>

<div id="download_repeat1" class="section">

#### download[¶](#download_repeat1 "Permalink to this headline")

Download dataset
    files

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets download [-h] [-f FILE_NAME] [-p PATH] [-w] [--unzip] [-o]
                             [-q]
                             [dataset]

</div>

</div>

<div id="Named Arguments_repeat9" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat9 "Permalink to this headline")

  - dataset  
    Dataset URL suffix in format \<owner\>/\<dataset-name\> (use “kaggle
    datasets list” to show options)

  - \-f, --file  
    File name, all files downloaded if not provided (use “kaggle
    datasets files -d \<dataset\>” to show options)

  - \-p, --path  
    Folder where file(s) will be downloaded, defaults to current working
    directory

  - \-w, --wp  
    Download files to current working path

  - \--unzip  
    Unzip the downloaded file. Will delete the zip file when completed.
    
    Default: False

  - \-o, --force  
    Skip check whether local version of file is up to date, force file
    download
    
    Default: False

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

</div>

</div>

<div id="create" class="section">

#### create[¶](#create "Permalink to this headline")

Create a new
    dataset

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets create [-h] [-p FOLDER] [-u] [-q] [-t] [-r {skip,zip,tar}]

</div>

</div>

<div id="Named Arguments_repeat10" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat10 "Permalink to this headline")

  - \-p, --path  
    Folder for upload, containing data files and a special
    datasets-metadata.json file
    (<https://github.com/Kaggle/kaggle-api/wiki/Dataset-Metadata>).
    Defaults to current working directory

  - \-u, --public  
    Create publicly (default is private)
    
    Default: False

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

  - \-t, --keep-tabular  
    Do not convert tabular files to CSV (default is to convert)
    
    Default: True

  - \-r, --dir-mode  
    Possible choices: skip, zip, tar
    
    What to do with directories: “skip” - ignore; “zip” - compressed
    upload; “tar” - uncompressed upload
    
    Default: “skip”

</div>

</div>

<div id="version" class="section">

#### version[¶](#version "Permalink to this headline")

Create a new dataset version

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets version [-h] -m VERSION_NOTES [-p FOLDER] [-q] [-t]
                            [-r {skip,zip,tar}] [-d]

</div>

</div>

<div id="required arguments_repeat1" class="section">

##### required arguments[¶](#required%20arguments_repeat1 "Permalink to this headline")

  - \-m, --message  
    Message describing the new
version

</div>

<div id="Named Arguments_repeat11" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat11 "Permalink to this headline")

  - \-p, --path  
    Folder for upload, containing data files and a special
    datasets-metadata.json file
    (<https://github.com/Kaggle/kaggle-api/wiki/Dataset-Metadata>).
    Defaults to current working directory

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

  - \-t, --keep-tabular  
    Do not convert tabular files to CSV (default is to convert)
    
    Default: True

  - \-r, --dir-mode  
    Possible choices: skip, zip, tar
    
    What to do with directories: “skip” - ignore; “zip” - compressed
    upload; “tar” - uncompressed upload
    
    Default: “skip”

  - \-d, --delete-old-versions  
    Delete old versions of this dataset
    
    Default: False

</div>

</div>

<div id="init" class="section">

#### init[¶](#init "Permalink to this headline")

Initialize metadata file for dataset
creation

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets init [-h] [-p FOLDER]

</div>

</div>

<div id="Named Arguments_repeat12" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat12 "Permalink to this headline")

  - \-p, --path  
    Folder for upload, containing data files and a special
    datasets-metadata.json file
    (<https://github.com/Kaggle/kaggle-api/wiki/Dataset-Metadata>).
    Defaults to current working directory

</div>

</div>

<div id="metadata" class="section">

#### metadata[¶](#metadata "Permalink to this headline")

Download metadata about a
dataset

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets metadata [-h] [--update] [-p PATH] [dataset]

</div>

</div>

<div id="Named Arguments_repeat13" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat13 "Permalink to this headline")

  - dataset  
    Dataset URL suffix in format \<owner\>/\<dataset-name\> (use “kaggle
    datasets list” to show options)

  - \--update  
    A flag to indicate whether the datasetmetadata should be updated.
    
    Default: False

  - \-p, --path  
    Location to download dataset metadata to. Defaults to current
    working directory

</div>

</div>

<div id="status" class="section">

#### status[¶](#status "Permalink to this headline")

Get the creation status for a
dataset

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle datasets status [-h] [dataset]

</div>

</div>

<div id="Named Arguments_repeat14" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat14 "Permalink to this headline")

  - dataset  
    Dataset URL suffix in format \<owner\>/\<dataset-name\> (use “kaggle
    datasets list” to show options)

</div>

</div>

</div>

</div>

<div id="kernels (k)" class="section">

## kernels (k)[¶](#kernels%20\(k\) "Permalink to this headline")

Commands related to Kaggle kernels

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle kernels [-h] {list,init,push,pull,output,status} ...

</div>

</div>

<div id="commands_repeat3" class="section">

### commands[¶](#commands_repeat3 "Permalink to this headline")

  - command  
    Possible choices: list, init, push, pull, output,
status

</div>

<div id="Sub-commands:_repeat3" class="section">

### Sub-commands:[¶](#Sub-commands:_repeat3 "Permalink to this headline")

<div id="list_repeat2" class="section">

#### list[¶](#list_repeat2 "Permalink to this headline")

List available kernels. By default, shows 20 results sorted by
    hotness

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle kernels list [-h] [-m] [-p PAGE] [--page-size PAGE_SIZE] [-s SEARCH]
                        [-v] [--parent PARENT] [--competition COMPETITION]
                        [--dataset DATASET] [--user USER] [--language LANGUAGE]
                        [--kernel-type KERNEL_TYPE] [--output-type OUTPUT_TYPE]
                        [--sort-by SORT_BY]

</div>

</div>

<div id="Named Arguments_repeat15" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat15 "Permalink to this headline")

  - \-m, --mine  
    Display only my items
    
    Default: False

  - \-p, --page  
    Page number for results paging. Page size is 20 by default
    
    Default: 1

  - \--page-size  
    Number of items to show on a page. Default size is 20, max is 100
    
    Default: 20

  - \-s, --search  
    Term(s) to search for

  - \-v, --csv  
    Print results in CSV format (if not set print in table format)
    
    Default: False

  - \--parent  
    Find children of the specified parent kernel

  - \--competition  
    Find kernels for a given competition slug

  - \--dataset  
    Find kernels for a given dataset slug. Format is
    {username/dataset-slug}

  - \--user  
    Find kernels created by a given username

  - \--language  
    Specify the language the kernel is written in. Default is ‘all’.
    Valid options are ‘all’, ‘python’, ‘r’, ‘sqlite’, and ‘julia’

  - \--kernel-type  
    Specify the type of kernel. Default is ‘all’. Valid options are
    ‘all’, ‘script’, and ‘notebook’

  - \--output-type  
    Search for specific kernel output types. Default is ‘all’. Valid
    options are ‘all’, ‘visualizations’, and ‘data’

  - \--sort-by  
    Sort list results. Default is ‘hotness’. Valid options are
    ‘hotness’, ‘commentCount’, ‘dateCreated’, ‘dateRun’,
    ‘relevance’, ‘scoreAscending’, ‘scoreDescending’, ‘viewCount’,
    and ‘voteCount’. ‘relevance’ is only applicable if a search term is
    specified.

</div>

</div>

<div id="init_repeat1" class="section">

#### init[¶](#init_repeat1 "Permalink to this headline")

Initialize metadata file for a
kernel

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle kernels init [-h] [-p FOLDER]

</div>

</div>

<div id="Named Arguments_repeat16" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat16 "Permalink to this headline")

  - \-p, --path  
    Folder for upload, containing data files and a special
    kernel-metadata.json file
    (<https://github.com/Kaggle/kaggle-api/wiki/Kernel-Metadata>).
    Defaults to current working directory

</div>

</div>

<div id="push" class="section">

#### push[¶](#push "Permalink to this headline")

Push new code to a kernel and run the
kernel

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle kernels push [-h] [-p FOLDER]

</div>

</div>

<div id="Named Arguments_repeat17" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat17 "Permalink to this headline")

  - \-p, --path  
    Folder for upload, containing data files and a special
    kernel-metadata.json file
    (<https://github.com/Kaggle/kaggle-api/wiki/Kernel-Metadata>).
    Defaults to current working directory

</div>

</div>

<div id="pull" class="section">

#### pull[¶](#pull "Permalink to this headline")

Pull down code from a
kernel

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle kernels pull [-h] [-p PATH] [-w] [-m] [kernel]

</div>

</div>

<div id="Named Arguments_repeat18" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat18 "Permalink to this headline")

  - kernel  
    Kernel URL suffix in format \<owner\>/\<kernel-name\> (use “kaggle
    kernels list” to show options)

  - \-p, --path  
    Folder where file(s) will be downloaded, defaults to current working
    directory

  - \-w, --wp  
    Download files to current working path

  - \-m, --metadata  
    Generate metadata when pulling kernel
    
    Default: False

</div>

</div>

<div id="output" class="section">

#### output[¶](#output "Permalink to this headline")

Get data output from the latest kernel
run

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle kernels output [-h] [-p PATH] [-w] [-o] [-q] [kernel]

</div>

</div>

<div id="Named Arguments_repeat19" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat19 "Permalink to this headline")

  - kernel  
    Kernel URL suffix in format \<owner\>/\<kernel-name\> (use “kaggle
    kernels list” to show options)

  - \-p, --path  
    Folder where file(s) will be downloaded, defaults to current working
    directory

  - \-w, --wp  
    Download files to current working path

  - \-o, --force  
    Skip check whether local version of file is up to date, force file
    download
    
    Default: False

  - \-q, --quiet  
    Suppress printing information about the upload/download progress
    
    Default: False

</div>

</div>

<div id="status_repeat1" class="section">

#### status[¶](#status_repeat1 "Permalink to this headline")

Display the status of the latest kernel
run

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle kernels status [-h] [kernel]

</div>

</div>

<div id="Named Arguments_repeat20" class="section">

##### Named Arguments[¶](#Named%20Arguments_repeat20 "Permalink to this headline")

  - kernel  
    Kernel URL suffix in format \<owner\>/\<kernel-name\> (use “kaggle
    kernels list” to show options)

</div>

</div>

</div>

</div>

<div id="config" class="section">

## config[¶](#config "Permalink to this headline")

Configuration settings

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle config [-h] {view,set,unset} ...

</div>

</div>

<div id="commands_repeat4" class="section">

### commands[¶](#commands_repeat4 "Permalink to this headline")

  - command  
    Possible choices: view, set,
unset

</div>

<div id="Sub-commands:_repeat4" class="section">

### Sub-commands:[¶](#Sub-commands:_repeat4 "Permalink to this headline")

<div id="view" class="section">

#### view[¶](#view "Permalink to this headline")

View current config values

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle config view [-h]

</div>

</div>

</div>

<div id="set" class="section">

#### set[¶](#set "Permalink to this headline")

Set a configuration
value

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle config set [-h] -n NAME -v VALUE

</div>

</div>

<div id="required arguments_repeat2" class="section">

##### required arguments[¶](#required%20arguments_repeat2 "Permalink to this headline")

  - \-n, --name  
    Name of the configuration parameter (one of competition, path,
    proxy)

  - \-v, --value  
    Value of the configuration parameter, valid values depending on name
    - competition: Competition URL suffix (use “kaggle competitions
    list” to show options) - path: Folder where file(s) will be
    downloaded, defaults to current working directory - proxy: Proxy for
    HTTP requests

</div>

</div>

<div id="unset" class="section">

#### unset[¶](#unset "Permalink to this headline")

Clear a configuration
value

<div class="highlight-default notranslate">

<div class="highlight">

    kaggle config unset [-h] -n NAME

</div>

</div>

<div id="required arguments_repeat3" class="section">

##### required arguments[¶](#required%20arguments_repeat3 "Permalink to this headline")

  - \-n, --name  
    Name of the configuration parameter (one of competition, path,
    proxy)

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="sphinxsidebar" data-role="navigation" data-aria-label="main navigation">

<div class="sphinxsidebarwrapper">

