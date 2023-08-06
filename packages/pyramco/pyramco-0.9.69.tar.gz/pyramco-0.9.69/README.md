# pyramco
A complete Python wrapper class for the RAMCO API


version 0.9.69
9-1-2020


Notes for 0.9.69 release: changed innacurate references to tuples in attributes, should be strings - changed arg types in same locations. Should resolve non-recognized string delimiter in some cases. Changes should be backward-compatible; revert to version 0.9.62 or lower if you experience issues and inspect code related to your attribute strings.

A new major release is coming soon and will include breaking changes: 

- Attributes and Attribute/Value string args will be normalized to accept proper lists/dict refs as args
- API key will be detected as an environment variable OR in a config file, and throw an exception otherwise


RAMCO API Documentation permalink:
<https://api.ramcoams.com/api/v2/ramco_api_v2_doc.pdf>


Requires the **requests** module:
<https://pypi.org/project/requests/>


your RAMCO API key should be set as an environment variable `RAMCO_API_KEY`



The contributors to Pyramco are not affiliated, associated, authorized, endorsed by, or in any way officially connected with RAMCO, The NATIONAL ASSOCIATION OF REALTORS®, or any of their subsidiaries or affiliates. The official RAMCO website can be found at https://ramcoams.com 

The name RAMCO, as well as related names, marks, emblems and images are registered trademarks of their respective owners.