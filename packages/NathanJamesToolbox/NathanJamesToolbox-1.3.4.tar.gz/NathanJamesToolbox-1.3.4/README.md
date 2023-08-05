# Table of contents
- [NathanJames Toolbox](#nathanjames-toolbox)
	* [Getting Started](#getting-started)
		+ [Installing](#installing)
	* [AirtableToolbox Class](#airtabletoolbox-class)
		+ [Overview](#overview)
		+ [Importing the module](#importing-the-module)
		+ [Create a URL using the table name](#create-a-url-using-the-table-name)
		+ [Create a dictionary of columns](#create-a-dictionary-of-columns)
		+ [Create a list of JSON containing all data](#create-a-list-of-json-containing-all-data)
		+ [Create a list of Airtable record IDs](#create-a-list-of-airtable-record-ids)
		+ [Delete a list of Airtable record IDs](#delete-a-list-of-airtable-record-ids)
		+ [Push data to Airtable](#push-data-to-airtable)
		+ [Create a list of data in an Airtable column](#create-a-list-of-data-in-an-airtable-column)
		+ [Check Airtable table for duplicates based on column data](#check-airtable-table-for-duplicates-based-on-column-data)
		+ [Cleans up a string that is formatted as a list](#cleans-up-a-string-that-is-formatted-as-a-list)
	* [SlackToolbox Class](#)
		+ [Overview](#)
		+ [Send a warning message in a slack channel](#)
		+ [Send a booking confirmation message in a slack channel](#)
	* [MySQLToolbox Class](#)
		+ [Overview](#)
		+ [Read a query](#)
		+ [Run a query](#)
	* [Cin7Toolbox Class](#)
		+ [Overview](#)
		+ [get_json](#)
	* [MiscToolbox Class](#)
		+ [Overview](#)
		+ [getWeek](#)
		+ [get_key](#)
		+ [divide_list](#)
		+ [convert_to_json](#)
	* [Author](#authors)
	* [License](#license)

<!-- toc -->

# NathanJames Toolbox 

Collection of tools used by NathanJames

[back](#table-of-contents)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

[back](#table-of-contents)

### Installing

You can use pip to install the package.

```
pip install NathanJamesToolbox
```
[back](#table-of-contents)

### AirtableToolbox Class
#### Overview
The class contains functions that help integrating with Airtable easier.

[back](#table-of-contents)

---

#### Importing the module

	>>> from NathanJamesToolbox import NathanJamesToolbox as nj
[back](#table-of-contents)

#### AirtableToolbox Class Instance

	_airtable = nj.airtableToolbox(<airtable base>, <airtable API Key>)
[back](#table-of-contents)

---
#### Create a URL using the table name
 - Create a formatted URL by supplying the table name

Example:

	>>> # _airtable.create_url(<Table Name>)
	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> url = _airtable.create_url('Master')
	>>> url
	'https://api.airtable.com/v0/Master'
[back](#table-of-contents)

#### Create a dictionary of columns
- Loop through all the pages and create a dictionary based on the table columns.

Example:

	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> url = _airtable.create_url('Master?filterbyformula={SKU}=12345')
	
	>>> _dict_master = _airtable.create_dictionary(url, 'SKU', reverse=False)
	>>> _dict_master
	{'12345': ['recxyzId']}
	
	>>> _dict_master = _airtable.create_dictionary(url, 'SKU', reverse=False, 'Product Class', 'Item Status')
	>>> _dict_master
	{'12345': ['recxyzId', 'Regular', 'Live']}
[back](#table-of-contents)
	
#### Create a list of JSON containing all data
- Loop through all the pages and create a list containing all data on all columns.

Example:

	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> url = _airtable.create_url('Master?filterbyformula={SKU}=12345')

	>>> _json_master = _airtable.get_json(url)
	>>> _json_master
	[{"id": "recxyzId","fields": {"SKU": "12345","Product Title": "Sample Title","PDS": ["recapABC"],"Product Class": "New","UPC": ["recABC"]}]
[back](#table-of-contents)
	
#### Create a list of Airtable record IDs
- Loop through all the pages and create a dictionary containing the {record ID: column data}.
- This is similar to create_dictionary but this limits the output to just 1 data point with the key being the record ID.
- The function also does not allow you to pass in query parameters.

Example:

	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> _json_master = _airtable.get_ids('Master', 'SKU')
	{'recxyzId': '12345', 'recabcId': '54321', 'recasdId': '74125'}
[back](#table-of-contents)

#### Delete a list of Airtable record IDs
- Delete records in Airtable based on record IDs.
- Please note that the function can only accept a maximum of 10 record IDs per request. This is an inherit limitation from Airtable.

Example:

	>>> # delete_ids(<table name>, <list_id>)
	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> _airtable.delete_ids('Master', ['recxyzId', 'recabcId', 'recasdId'])
[back](#table-of-contents)

#### Push data to Airtable (Patch / Post)
- Sends either a patch or post request to the Airtable API.

|Status|Code|Reason|Description
|--|--|--|--|
|Success|200|OK|Request completed successfully.
|User Error|400|Bad Request|The request encoding is invalid; the request can't be parsed as a valid JSON.
|User Error|401|Unauthorized|Accessing a protected resource without authorization or with invalid credentials.
|User Error|402|Payment Required|The account associated with the API key making requests hits a quota that can be increased by upgrading the Airtable account plan.
|User Error|403|Forbidden|Accessing a protected resource with API credentials that don't have access to that resource.
|User Error|404|Not Found|Route or resource is not found. This error is returned when the request hits an undefined route, or if the resource doesn't exist (e.g. has been deleted).
|User Error|413|Request Entity Too Large|The request exceeded the maximum allowed payload size. You shouldn't encounter this under normal use.
|User Error|422|Invalid Request|The request data is invalid. This includes most of the base-specific validations. You will receive a detailed error message and code pointing to the exact issue.
|Server error|500|Internal Server Error|The server encountered an unexpected condition.
|Server error|502|Bad Gateway|Airtable's servers are restarting or an unexpected outage is in progress. You should generally not receive this error, and requests are safe to retry.
|Server error|503|Service Unavailable|The server could not process your request in time. The server could be temporarily unavailable, or it could have timed out processing your request. You should retry the request with backoffs.
	
- The function returns the status code

Example:
	
	>>> # push_data(url, payload, patch=True) *** if patch=True, send a patch request else if patch=False then send a post request
	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> url = _airtable.create_url('Master')
	>>> payload = {"records": [{"id": "recxyzId", "fields": {"Product Title": "New Sample Title"}}]}
	>>> req = _airtable.push_data(url, payload, patch=True)
	>>> req
	200
[back](#table-of-contents)

#### Create a list of data in an Airtable column
- Returns a list of row data based on the Airtable column.

Example:

	>>># create_list(url, column)
	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> url = _airtable.create_url('Master')
	>>> _list = _airtable.create_list(url, 'SKU')
	>>> _list
	['12345', '54321', '74125']
[back](#table-of-contents)

#### Check Airtable table for duplicates based on column data
- Returns a list of duplicate row data based on the Airtable column.

Example:

	>>># table_duplicate_check(url, baseName)
	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> url = _airtable.create_url('Master')
	>>> _list_duplicates = _airtable.table_duplicate_check(url, 'SKU')
	>>> _list
	The following duplicates found on
	----table: Master
	----Data: ['74125']
	>>> # This means that the Master table contains 2 records with SKU 74125
[back](#table-of-contents)

#### Cleans up a string that is formatted as a list
- Returns a string that contains the following characters: ["'", "[", "]"]

Example:

	>>># clean_list_string(str)
	>>> _airtable = nj.airtableToolbox('abcdefg', 'xyzApiKey')
	>>> my_string = "['rec123456']"
	>>> my_string = _airtable.clean_list_string(my_string )
	>>> print(type(my_sting), my_sting)
	string	rec123456
[back](#table-of-contents)
	
---
### SlackToolbox Class
#### Overview
The class contains functions that help integrating with Slack easier.
[back](#table-of-contents)

---

#### SlackToolbox Class Instance

	_slack = nj.SlackToolbox(<api_key>, <channel_name>)
[back](#table-of-contents)

---
#### Send a warning message in a slack channel
- The function sends a message to a specific channel

Example:

	>>> # send_warning(pyfile=__file__, funcName=None, description=None)

	>>> import sys
	>>> _slack = nj.SlackToolbox('xyzAPIkey', 'General')
	>>> _slack.send_warning(__file__, 'check_stock_availability', 'Stock Availability for 74403 returned -33.0')

![Sample message](https://github.com/pfajardo-nj/NathanJamesToolbox/blob/master/assets/slack_error_sample.JPG)
[back](#table-of-contents)
	
#### Send a booking confirmation message in a slack channel
- The function sends a booking confirmation message to a specific channel

Example:

	>>> # send_booking_confirmation(funcName, description)

	>>> _slack = nj.SlackToolbox('xyzAPIkey', 'operations')
	>>> _slack.send_warning(__file__, 'create_shipment', 'Flexport booking created for PO-00xxx (#Containers: 4) | Cargo Ready Date: 2020-08-31) | Delivery Date: 2020-09-30)')
[back](#table-of-contents)

---
### MySQLToolbox Class
#### Overview
The class contains functions that help integrating with mySQL easier.
[back](#table-of-contents)

---
#### MySQLToolbox Class Instance

	>>> # _mySQL= nj.mySQLToolbox(default_file_path, host, user, password, database_name)
	>>> _mySQL= nj.mySQLToolbox('c:\\', '123.456.7.8', 'root', 'Pass8426Word', 'NathanJames')
[back](#table-of-contents)

---
#### Read a query
- Run a query and return the result
- Accepts both file 'f' or a query string 'q'

Example:

	>>> # readQuery(qry, type)
	>>> _mySQL= nj.mySQLToolbox('c:\\', '123.456.7.8', 'root', 'Pass8426Word', 'NathanJames')
	>>> qry = 'SELECT sku, product_class FROM NathanJames.Master'
	>>> req = _mySQL.read_query(qry, 'q')
	>>> req
	((12345, Regular), (54321, Regular), (74125, Regular))
	
	>>> with open('c:\\test.sql', 'w') as f:
	>>>		f.write('SELECT sku, product_class FROM NathanJames.Master')
	>>> qry = 'c:\\test.sql'
	>>> req = _mySQL.read_query(qry, 'f')
	>>> req
	((12345, Regular), (54321, Regular), (74125, Regular))
[back](#table-of-contents)

#### Run a query
- Run a query and return if it passed or failed

Example:

	>>> # runQuery(qry)
	>>> qry = 'CREATE TABLE NathanJames.Test (SKU VARCHAR(10))'
	>>> req = _mySQL.runWuery(qry)
	>>> req
	Passed

	>>> qry = 'CREATE TABLE NathanJames.Test'
	>>> req = _mySQL.runQuery(qry)
	>>> req
	Failed
[back](#table-of-contents)

---
### Cin7Toolbox Class
#### Overview
The class contains functions that help integrating with Cin7.
[back](#table-of-contents)

---
#### Cin7Toolbox Class Instance

	>>> # _cin7= nj.Cin7Toolbox(username, password)
	>>> _cin7= nj.Cin7Toolbox('test_user', 'Pass8426Word')
[back](#table-of-contents)

---
#### get_json
- Return a list containing the json response from the end-point

Example:

	>>> # get_json(self, endpoint)
	>>> _cin7= nj.Cin7Toolbox('test_user', 'Pass8426Word')
	>>> url = 'https://api.cin7.com/api/v1/SalesOrders?where=id=1234'
	>>> req = _cin7.get_json(url)
	>>> req
	[{"id": 1234,"createdDate": "2018-07-18T06:00:00Z","modifiedDate": "2018-08-09T19:01:12Z","createdBy": 30437,"processedBy": 0,"isApproved": true,"reference": "CS122213218","memberId": 17,"firstName": "","lastName": "","company": "Wayfair","email": "","phone": "88888888888","mobile": ""}]
[back](#table-of-contents)

---
### MiscToolbox Class
#### Overview
The class contains functions that help integrating with Cin7.
[back](#table-of-contents)

---
#### MiscToolbox Class Instance

	>>> _misc= nj._misc()
[back](#table-of-contents)

---
#### getWeek
- Return the current day's NathanJames week number

Example:

	>>> # get_week()
	>>> _misc= nj._misc()
	>>> # Suppose today is August 18, 2020
	>>> _week = get_week()
	>>> _week
	154
[back](#table-of-contents)

## Authors

* **Paulo Fajardo** - *Initial work* - [github](https://github.com/pfajardo-nj/NathanJames-Automation-Script)

[back](#table-of-contents)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

[back](#table-of-contents)