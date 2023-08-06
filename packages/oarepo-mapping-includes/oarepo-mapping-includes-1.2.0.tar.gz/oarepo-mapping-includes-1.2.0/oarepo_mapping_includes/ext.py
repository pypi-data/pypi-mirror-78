import json
import os

import pkg_resources
import requests
from elasticsearch import VERSION as ES_VERSION
from invenio_base.signals import app_loaded
from jsonpointer import JsonPointer, JsonPointerException
from pkg_resources import iter_entry_points

from oarepo_mapping_includes.mapping_transformer import mapping_transformer


class IncludedMapping:
    def __init__(self, name, json):
        self.name = name
        self.json = json
        self.build_ids()

    def get_id(self, idd):
        if not idd:
            return self.json
        try:
            return self.ids[idd]
        except KeyError:
            raise KeyError('Id %s not found in %s' % (idd, self.name))

    def get_pointer(self, pointer):
        if not pointer:
            return self.json

        try:
            return JsonPointer(pointer).resolve(self.json)
        except JsonPointerException as e:
            raise KeyError('Json pointer %s not found in %s: %s' % (pointer, self.name, str(e)))

    def build_ids(self):
        def build(el):
            el_id = el.pop('$id', None)
            if el_id:
                self.ids[el_id] = el
            for k, v in el.items():
                if isinstance(v, dict):
                    build(v)

        self.ids = {}
        build(self.json)


class OARepoMappingIncludesState:
    def __init__(self, app, _includes=None, _handlers=None):
        self.app = app
        self._includes = _includes
        self._handlers = _handlers

    @property
    def included_mappings(self):
        if self._includes is None:
            self._includes = self._load_included_mappings()
        return self._includes

    @property
    def mapping_handlers(self):
        if self._handlers is None:
            self._handlers = self._load_mapping_handlers()
        return self._handlers

    def _load_included_mappings(self):
        included_mappings = {}
        for ep in iter_entry_points('oarepo_mapping_includes'):
            package_name = '{}.v{}'.format(ep.module_name, ES_VERSION[0])
            package_name = package_name.split('.', maxsplit=1)
            package_path = package_name[1].replace('.', '/')
            for filename in pkg_resources.resource_listdir(package_name[0], package_path):
                if filename.endswith('.json'):
                    file_data = pkg_resources.resource_string(
                        package_name[0],
                        os.path.join(package_path, filename))
                    included_mappings[filename] = IncludedMapping(filename, json.loads(file_data.decode("utf-8")))
        return included_mappings

    def _load_mapping_handlers(self):
        handlers = {}
        for ep in iter_entry_points('oarepo_mapping_handlers'):
            handlers[ep.name] = ep.load()
        return handlers

    def load_type(self, type, content, root, content_pointer):
        mapping_handlers = self.mapping_handlers

        if '#' not in type:
            resource, json_pointer = type, None
        else:
            resource, json_pointer = type.split('#', maxsplit=1)

        if json_pointer and json_pointer[0] != '/':
            idd = json_pointer
            json_pointer = None
        else:
            idd = None

        if type in mapping_handlers:
            return mapping_handlers[type](
                type=type, resource=resource, id=idd, json_pointer=json_pointer,
                app=self.app, content=content, root=root, content_pointer=content_pointer)

        if resource in mapping_handlers:
            return mapping_handlers[resource](
                type=type, resource=resource, id=idd, json_pointer=json_pointer,
                app=self.app, content=content, root=root, content_pointer=content_pointer)

        mappings = self.included_mappings
        if resource not in mappings:
            if resource.startswith('http://') or resource.startswith('https://'):
                mappings[resource] = IncludedMapping(resource, requests.get(resource).json())
        try:
            mapping = mappings[resource]
        except KeyError:
            if not json_pointer and not idd:
                return None
            raise KeyError('%s not in %s' % (resource, list(sorted(mappings.keys()))))

        if idd:
            return mapping.get_id(idd)
        else:
            return mapping.get_pointer(json_pointer)


class OARepoMappingIncludesExt:

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.init_config(app)
        app.extensions['oarepo-mapping-includes'] = OARepoMappingIncludesState(app)
        app_loaded.connect(mapping_transformer)

    def init_config(self, app):
        pass
