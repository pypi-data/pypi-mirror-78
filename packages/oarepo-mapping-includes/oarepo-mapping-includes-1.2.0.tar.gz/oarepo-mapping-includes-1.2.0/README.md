# OAREPO mapping includes

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

This package adds support for inclusions in elasticsearch mappings.

## Example

A title, abstract and description are multilingual strings that look like 

```json5
{
  en: 'English version',
  cs: 'Czech version'
}
```

As elasticsearch does not have support for includes, the mapping for the three properties
would be quite large. With this library, you can create a mapping, for example called
``multilingual-v1.0.0.json`` and reference it:

```json5
// multilingual-v1.0.0.json
{
    "text": {
        "type": "object",
        "properties": {
            "en": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 100
                    }
                } 
            },
            cs: {
                "type": "text",
                "analyzer": "czech",
                "fields": {
                    "keyword": {
                        "ignore_above": 100,
                        "type": "icu_collation_keyword",
                        "language": "cs",
                    }                    
                }
            }
        }
    },
    "analysis": {
        // definition of czech analyzer
    }
}
```

```json5
// main mapping
{
    "settings": {
        "analysis": {
            "oarepo:extends": "multilingual-v1.0.0.json#/analysis"
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "multilingual-v1.0.0.json#/text",
                // extra properties for title might go here and are merged in
            },
            "description": {
                "type": "multilingual-v1.0.0.json#/text"
            },
            "abstract": {
                "type": "multilingual-v1.0.0.json#/text"
            }
        }
    }
}
```

The included mapping might be located inside invenio with no external url, hosted on a web server
and referenced by http:// or https:// or even generated dynamically on demand.

## Installation

```bash

pip install oarepo-mapping-includes

```

## Configuration

This library has to know where included mappings (if not hosted on external server) are located.
Specify this in entrypoints (``my_repo`` is the top-level package of your repository):

```python
setup(
    # ...
    entry_points={
        "oarepo_mapping_includes": [
            "my_repo = my_repo.mapping_includes"
        ],
        "oarepo_mapping_handlers": [
            "something_discussed_later = my_repo.mapping_handlers:dynamic"
        ]
    }
)
```

## Included files location

The ``oarepo_mapping_includes`` is supposed to have the following structure, same as in invenio:

```
my_repo
    +- mapping_includes                     <-- as defined in entrypoint 
        +- v7                               <-- ES version
            +- multilingual-v1.0.0.json     <-- this is referenced in type, oarepo:extends
```

## Supported constructs

### ``type``

Looks if the type is either an external resource (http://, https://) or a registered internal
resource. If not, it is left intact, otherwise the definition is obtained in the following way:

  1. If there are any mapping handlers mapped to the value of the type, they are used
  2. resource (without ``#`` part if present) is fetched from internal cache external uri
  3. if ``#`` is not a part of the type, the whole resource is returned
  4. if the first character after hash is ``/``, it is assumed that it is an json pointer
     and is applied. The result of the json pointer is returned. Error is raised if the path
     does not exist
  5. Otherwise an element containing ``$id`` property with this value is obtained. Error 
     is raised if element with this id does not exist

The definition is then merged with any other elements present at the same level, conflicting
values are overwritten (think of inheritance in python).

#### Array of types

Multiple types are supported.

```json5
{
  // ...
  "title": {
    "type": [
      "multilingual-v1.0.0.json#/text",
      "copy-v1.0.0.json",
    ]
  }
}
```

Where ``copy-v1.0.0.json`` might contain:

```json5
{
  "copy_to": "all_fields"
}
```

On conflict, similar algorithm to python inheritance is used

### oarepo:extends

``oarepo:extends`` behaves exactly the same way as ``type`` but can be used anywhere in the mapping

## Dynamic handlers

Sometimes it would be better if the mapping was dynamically created. For example,
the number of supported languages varies from installation to installation and the 
supported languages are specified in ``invenio.cfg``

In entry points, define ``oarepo_mapping_handlers``. The left hand side before '='
is what should match the ``type``, ``extend``. It might be the full value or the
value before ``#``.

The handler's signature is:

```python
def handler(type=None, resource=None, id=None, json_pointer=None, app=None, 
            content=None, root=None, content_pointer=None, **kwargs):
    """
    :param type         the type as literally written in "type" or "extends" properties
    :param resource     part of the type before '#'
    :param id           part of the type after '#' if it does not start with '/'  
    :param json_pointer part of the type after '#' if it starts with '/'
    :param app          current flask application. Use app.config to get the current config
    :param content      json element containing the ``type`` 
    :param root         the whole mapping
    :param content_pointer 
                        json pointer of the content element
    :param **kwargs     think of extensibility
    """
    return {...}
```

### Merging and replacing content

The handler can return either a dictionary or an instance of ``oarepo_mapping_includes.Mapping``.

If it returns a dictionary it is merged with the original mapping content 
(such as extra properties etc.)

If it returns a ``Mapping(mapping=<dict>, merge=True)``, the parameter ``merge`` defines if 
the original mapping content will be merged in (``True``) or completely replaced (``False``).

This is usable if the handler wants to transform the original content, not simply to merge it.


  [image]: https://img.shields.io/github/license/oarepo/oarepo-mapping-includes.svg
  [1]: https://github.com/oarepo/oarepo-mapping-includes/blob/master/LICENSE
  [2]: https://img.shields.io/travis/oarepo/oarepo-mapping-includes.svg
  [3]: https://travis-ci.org/oarepo/oarepo-mapping-includes
  [4]: https://img.shields.io/coveralls/oarepo/oarepo-mapping-includes.svg
  [5]: https://coveralls.io/r/oarepo/oarepo-mapping-includes
  [6]: https://img.shields.io/pypi/v/oarepo-mapping-includes.svg
  [7]: https://pypi.org/pypi/oarepo-mapping-includes