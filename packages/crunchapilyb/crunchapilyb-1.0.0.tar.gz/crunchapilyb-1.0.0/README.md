# CrunchAPI
A CrunchBase API by Christopher, 08/29/2020

## Quick Start
We can use this package to download people/organization data from CrunchBase based on RapidAPI and store them in .csv files if needed.
Two functions are available: ```crunch_api_ppl``` and ``` crunch_api_org```, respectively for people/organization queries.

### Features
* Number limitation supported
  * Users can appoint the maximum number of the records they want to obtain, and functions would return either all records (if the appointed number is non-positive or is greater the total number of records searched) or this number of records.
* CSV files supported
  * Query result is returned as a Pandas DataFrame, and users can choose to save them directly in a .csv file.
  * If no records is available, the return would be None and no .csv files would be created.
* RapidAPI Key
  * For each run, users would have to enter the valid Key only once.
  * If the key is invalid, users would be asked to re-enter the Key until it's valid.
  
### ```crunch_api_ppl```
Optional parameters:
* ```num_records```: int, maximum number of the records to query;
* ```since_time```: string, restricts the result set to People where updated_at >= the passed value when provided;
* ```sort_order```: string, the sort order of the collection, including "createdat ASC", "createdat DESC", "updatedat ASC", and "updatedat DESC";
* ```name```: string, a full-text query of name only;
* ```query```: string, a full-text query of name, title, and company;
* ```locations```: string, filter by location names (comma separated, AND'd together), e.g. locations=California,San Francisco;
* ```types```: string, filter by type (currently, either this is empty, or is simply "investor");
* ```socials```: string, Filter by social media identity (comma separated, AND'd together), e.g. socials=ronconway;
* ```csv_name```: string, .csv file to save results to.

### ```crunch_api_org```
Optional parameters:
* ```num_records```: int, maximum number of the records to query;
* ```since_time```: string, restricts the result set to People where updated_at >= the passed value when provided;
* ```sort_order```: string, the sort order of the collection, including "createdat ASC", "createdat DESC", "updatedat ASC", and "updatedat DESC";
* ```name```: string, a full-text search of of an Organization's name, aliases (i.e. previous names or "also known as"), and short description;
* ```query```: string, a full-text search limited to name and aliases;
* ```domain_name```: string, text search of an Organization's domain_name, e.g. www.google.com;
* ```locations```: string, filter by location names (comma separated, AND'd together), e.g. locations=California,San Francisco;
* ```types```: string, filter by one or more types. Multiple types are separated by commas. Available types are "company", "investor", "school", and "group". Multiple organization_types are logically AND'd;
* ```csv_name```: string, .csv file to save results to.


## Requirements
Packages needed:
* requests
* pandas