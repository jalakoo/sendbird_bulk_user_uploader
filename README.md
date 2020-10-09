# Sendbird Bulk User Uploader
Super simple python script for uploading .csv files of users to a target Sendbird application using Sendbird's [Platform API](https://docs.sendbird.com/platform)

## Requirements
- A valid [Sendbird account](https://dashboard.sendbird.com/auth/signup)
- A Sendbird application with an Application ID**
- A Sendbird application primary or secondary token**

** Both of these can be found in your Sendbird dashboard/application/Settings/General

## Features
- Saves Sendbird Application id and token to an .env file for faster re-runs

## Usage
From terminal run: `python3 sendbird_users.py -f <csv_filepath>`

