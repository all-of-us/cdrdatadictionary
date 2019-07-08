# Prototype YAML Generator

This document will guide you through setting up the yaml generator in your environment.

Create your working environment and load the required packages.
  1.  Create a virtual environment.  For python 2.7, try `virtualenv <env_folder_name>`
  2.  Source your virtual environment.  `source <env_folder_name>/bin/activate`
  3.  Ensure pip is up to date.  `pip install --upgrade pip`
  4.  Install the requirements from the requirements file.  `pip install -r requirements.txt`

Set up your google account credentials and API access.  This document will go through the process of setting up the google drive requirements.  You may study google's documentation for more in-depth knowledge.

### Enable the Google Sheets API
  1.  Ensure you are logged into the Google project that will host the spreadsheet.
  2.  Using a web browser, navigate to google libraries at: https://console.developers.google.com/apis/library.
  3.  Search for `Google Sheets API`.
  4.  Select the Google Sheets API and enable it.

### Create Account Credentials
  1.  Using a web browser, navigate to https://console.developers.google.com/apis/credentials
  2.  Select the project owning the Google Sheet.
  2.  Use the `Create credentials` button to create an `OAuth Client ID`.  
  3.  You may have to create a consent screen for your project.  Provide a name and any other requirements you would like to place on the screen.  Then go back to the main credentials screen.
  4.  Select a type of Other and give it a name.
  5.  Download the client secret key.

Alternatively, you may use a service account key if you prefer.

### Execute the program from the command line
To execute the yaml generator:
  1.  Ensure your virtual environment is active.  `source <env_name>/bin/activate`
  2.  In the directory with `generate_yaml.py`, type:  `python generate_yaml.py <path_to_client_secret_key> <URL identifier of the Google Sheet> "<Sheet Name>"
  
This will generate a yaml file for the sheet identified by the URL identifier and the sheet name.  For example, if the URL of the sheet is:  https://docs.google.com/spreadsheets/d/1qDTcz5tUnEGFoZfyPPtp-2mF6U/edit, then the identifier is:  1qDTcz5tUnEGFoZfyPPtp-2mF6U.  If the document contained sheets named:  `Field Gen`, `Row Sup`, you would generate a yaml file for the `Row Sup` sheet with the command line:  `python generate_yaml.py <path_to_client_secret_key> 1qDTcz5tUnEGFoZfyPPtp-2mF6U "Row Sup"`

Other optional command line arguments exist and can be viewed with: `python generate_yaml.py -h`.  These optional arguments allow you to define an output file name, a range of cells in the sheet, and the column to use when grouping.

```
(yaml_env) $ python generate_yaml.py -h
usage: generate_yaml.py [-h] [-r RANGE] [-o OUTPUT_FILE]
                        [-g {A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z}]
                        key_file spreadsheet_id sheet_name

Google drive yaml prototype. Automatically generates a yaml file from the read
only version of the identified file. Defaults exist for choosing the value to
group around. See https://developers.google.com/sheets/api/quickstart/python
and https://developers.google.com/sheets/api/guides/concepts for information
on configuring required credentials for reading Google Drive files.

positional arguments:
  key_file              Filepath to your service account key
  spreadsheet_id        Google spreadsheet ID (as seen in URL)
  sheet_name            Name of the sheet in the spreadsheet to parse. Enclose
                        in quotes if the name contains spaces.

optional arguments:
  -h, --help            show this help message and exit
  -r RANGE, --range RANGE
                        Range of cells to select in the sheet. If not
                        specified, returns all cell values.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Name to give the produced yaml file. If not provided,
                        defaults to out.yaml
  -g {A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z}, --group_by {A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z}
                        Used to create groupings around a different field in a
                        sheet. Sheets with 'Field' in the title default to
                        Column B. Sheets with 'Row' in the title default to
                        Column D. Sheets with neither in the title default to
                        Column A.
```
