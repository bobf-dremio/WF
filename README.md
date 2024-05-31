Utilize an excel upsert into Dremio  by calling UpsertExcel.pu -c <configfile> -f <pathtoyourexcelfile> -t <name_of_table> -p <'path,of,your,table'> .
For Path, please comma separate and do not use spaces.

The config File should look like the below:
{
    "dremio_url":  "https://yourdremiourl",
    "api_key": "yourapi_key"
}
