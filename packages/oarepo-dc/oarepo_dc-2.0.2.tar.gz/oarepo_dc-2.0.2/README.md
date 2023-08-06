OARepo DC data model
====================

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

DC Terms data model for oarepo.

Instalation
----------
```bash
    pip install oarepo-dc
```
Usage
-----
The library provides Dublin Core object for json schema with marshmallow validation and deserialization and elastic search mapping.

JSON Schema
----------
Add this package to your dependencies and use it via $ref in json
schema as ``"[server]/schemas/dcterms-v2.0.0.json#/definitions/DCObject"``. 
Elastic Search mapping is handled automatically via Eleastic Search templates.

### Usage example
```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "these": {
            "$ref": "https://localhost:5000/schemas/dcterms-v2.0.0.json#/definitions/DCObject"
      }
  }
}
```

```json
{
  "type": "object",
  "properties": {
    "these": {
        "abstract" : {"cs": "neco", "en": "something"}, 
        "contributor" : "Alzbeta Pokorna", 
        "modified":"2012-04-23T18:25:43.511Z"
            }
        }
}
```
Marshmallow
-----------
For data validation and deserialization.

If marshmallow validation is performed within application context, languages in multilingual string data fields are validated against SUPPORTED_LANGUAGES config.
If the validation is performed outside app context, the keys are not checked against a list of languages
but a generic validation is performed - keys must be in ISO 639-1 or language-region format from RFC 5646.

### Usage example
```python
class MD(DCObjectSchemaV2Mixin, marshmallow.Schema):
    pass

data = {"title": {"cs": "neco"},
                 "alternative": {"en-us": "something", "cs": "neco"},
                 "abstract": {},
                 "creator": "Alzbeta Pokorna",
                 "contributor": "Miroslav Simek",
                 "dateSubmitted": "1970-10-12",
                 "available": "1970-03-18",
                 "created": "1970-09-29",
                 "modified": "1970-12-31",
                 "description": {"en-us": "something", "cs": "neco"},
                 "identifier": "id"}


    MD().load(data)
```
Supported languages validation
------------------------------
You can specified supported languages in your application configuration in ``SUPPORTED_LANGUAGES`` . Then only these
languages are allowed as multilingual string. 
You must specified your languages in format ``"en"`` or ``"en-us"``.
### Usage example
```python
app.config.update(SUPPORTED_LANGUAGES = ["cs", "en"])
```

  [image]: https://img.shields.io/github/license/oarepo/oarepo-dc.svg
  [1]: https://github.com/oarepo/oarepo-dc/blob/master/LICENSE
  [2]: https://img.shields.io/travis/oarepo/oarepo-dc.svg
  [3]: https://travis-ci.org/oarepo/oarepo-dc
  [4]: https://img.shields.io/coveralls/oarepo/oarepo-dc.svg
  [5]: https://coveralls.io/r/oarepo/oarepo-dc
  [6]: https://img.shields.io/pypi/v/oarepo-dc.svg
  [7]: https://pypi.org/pypi/oarepo-dc