[![Build Status](https://travis.ibm.com/Michal-Grzejszczak/ipaconnector.svg?token=wppJ1yqfzQ9QDdCSiLpd&branch=master)](https://travis.ibm.com/Michal-Grzejszczak/ipaconnector)

# IPA Connector

IPA Connector is script that allows to perform standard user/group add/delete/update operations on Red Hat IDM/FreeIPA. \

It requires to have .json file provided with changes specified to be made in IPA. \
See examples at *tests/sample_X.json* 


## Requirements
IPA Connector requires python3.6 to be installed. \
If you want to use Kerberos authentication, install also python package: requests_kerberos 

## Installation
*optional* virtualenv venv -ppython3; source venv/bin/activate;\
*optional* pip install requests_kerberos \
pip install ipaconnector 

## Usage
### Default usage
This will try to connect to ipa.server.net using your current username and will ask you for password.\
ipa-connector ipa.server.net path/to/file.json 

### Adjust log level and change user
ipa-connector ipa.server.net path/to/file.json --log-level 2 -u ipauser

### Use Kerberos to log in 
run kinit first\
ipa-connector ipa.server.net path/to/file.json -k 

### Log level
| Value | Log level |
| ------|:---------:|
5 | ERROR
4 | WARN
3 | INFO
2 | DEBUG
1 | ALL





