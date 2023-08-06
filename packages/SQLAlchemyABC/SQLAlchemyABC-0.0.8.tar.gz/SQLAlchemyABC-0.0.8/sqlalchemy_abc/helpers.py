from typing import Optional
from datetime import datetime
from datetime import date

from sqlalchemy.orm.collections import InstrumentedList

from .database import db


def save(session):
    session.save()


def primarykey(model):
    return model.__mapper__.primary_key[0].name


def hidden_fields(element):
    return set([getattr(col, 'name', col) for col in getattr(element, '__hidden__', set())])


def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
        if attr != 'id' and attr in self.fields():
            setattr(self, attr, value)

    for mtm in set(self.relationattrs()).intersection(set(kwargs.keys())):
        model = getattr(self, mtm)
        current = set(map(lambda rel: getattr(rel, rel.identify_primary_key()), model))
        candidates = set(map(lambda item: list(item.values()).pop(), kwargs[mtm]))
        for addition in candidates.difference(current):
            association = db.session.query(self.__mapper__.relationships.classgroups.entity).get(addition)
            getattr(self, mtm).append(association)

        for removal in current.difference(candidates):
            association = db.session.query(self.__mapper__.relationships.classgroups.entity).get(removal)
            getattr(self, mtm).remove(association)
    self.save()
    return self


def related(model, lookup=None):
    if lookup:
        return getattr(model, lookup).entity.entity
    related_models = [i.entity.entity for i in model.__mapper__.relationships]
    return related_models


def relationships(model, fmt=False):
    rels = model.__mapper__.relationships
    if fmt:
        return set(map(lambda x: x.key, rels))
    return rels


def columns(model, strformat=False, relations=None):
    if not model:
        return None
    bound_columns = set(model.__mapper__.columns)
    if relations:
        return bound_columns.union(set([i.class_attribute for i in model.__mapper__.relationships]))
    if strformat:
        return [i.name for i in bound_columns]
    return bound_columns


def getschema(model):
    cols = set([i.name for i in columns(model)])
    cols = cols.difference([i.name for i in getattr(model, 'hidden', [])])
    schemamap = {
        'model': model.__tablename__,
        'fields': []
    }

    for item in cols:
        column = getattr(model, item)
        schemamap['fields'].append(dict(name=column.name, type=str(column.type)))

    return schemamap


def extract(element, fields=None, exclude: Optional[set] = None, **kwargs) -> Optional[dict]:
    resp = dict()
    if element is None:
        return None
    if exclude is None:
        exclude = set()

    if fields is None:
        fields = columns(element, strformat=True)

    for column in set(fields or []).difference(set(exclude)).difference(hidden_fields(element)):
        if isinstance(getattr(element, column), datetime) or isinstance(getattr(element, column), date):
            resp[column] = str(getattr(element, column))
        else:
            resp[column] = getattr(element, column)

    for prop in getattr(element, '__properties__', set()):
        resp[prop.fget.__name__] = getattr(element, prop.fget.__name__)

    if getattr(element, '__counts__', None):
        resp['__counts__'] = getattr(element, '__counts__')

    if getattr(element, '__expose__', None):
        for entity in getattr(element, '__expose__'):
            if entity.key in exclude:
                continue
            if entity.uselist:
                resp[entity.key] = []
                for child in getattr(element, entity.key):
                    resp[entity.key].append(extract(child))
            else:
                resp[entity.key] = extract(getattr(element, entity.key, None))

    return resp


def process_relationship(data, exclude):
    resp = None
    if isinstance(data, list):
        resp = []
        for item in data:
            resp.append(extract(item, columns(item, strformat=True), exclude))
        return resp
    else:
        resp = extract(data, columns(data, strformat=True), exclude)
    return resp


def transform(data, fields=None, relations=None, **kwargs):
    if isinstance(data, list):
        resp = []
        for item in data:
            resp.append(extract(item))
        return resp
    return extract(data)


def iserialize(data, fields=None, rels=None, root=None, exclude=None, functions=None,
               **kwargs):
    """
    This utility function dynamically converts Alchemy model classes into a
    dict using introspective lookups. This saves on manually mapping each
    model and all the fields. However, exclusions should be noted. Such as
    passwords and protected properties.

    :param model: SQLAlchemy model
    :param data: query data
    :param functions:
    :param fields: More of a whitelist of fields to include (preferred way)
    :param rels: Whether or not to introspect to relationships
    :param exc: Fields to exclude from query result set
    :param root: Root model for processing relationships. This acts as a
    recursive sentinel to prevent infinite recursion due to selecting oneself
    as a related model, and then infinitely trying to traverse the roots
    own relationships, from itself over and over.
    :param exclude: Exclusion in set form. Currently in favour of exc param.

    Only remedy to this is also to use one way relationships. Avoiding any
    back referencing of models.

    :return: json data structure of model
    :rtype: dict
    """

    if functions is None:
        functions = {}
    if exclude is None:
        exclude = set()
    else:
        exclude = set(exclude)

    model = data
    if isinstance(data, list) and len(data):
        model = data[0]

    exclude = exclude.union(set(kwargs.get('exclusions', set())))
    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, 'hidden', set())))
    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, '__hidden__', set())))

    if not data:
        return []

    if rels is True:
        rels = relationships(model, True)

    if not fields:
        fields = set(columns(model, strformat=True))

    fields = fields.difference(exclude)

    def process(element):
        if getattr(element, '_fields', None):
            transformed = {}
            for idx, field in enumerate(element._fields):
                transformed[field] = element[idx]
            return transformed

        transformed = extract(element, fields, exclude, **kwargs)
        if functions:
            for key, value in functions.items():
                transformed[f'_{key}'] = value(getattr(element, key))
        # rels = set([i.key for i in element.__mapper__.relationships]).intersection(fields)

        for item in rels or []:
            if '.' in item:
                left, right = item.split('.')
                _ = process_relationship(getattr(element, left), exclude)

                for idx, i in enumerate(getattr(element, left)):
                    _[idx][right] = extract(getattr(i, right))
                transformed[left] = _
                continue

            rel = None
            if getattr(element, item, None):
                rel = process_relationship(getattr(element, item), exclude)
                transformed[item] = rel
        return transformed

    if root is None:
        root = model.__tablename__

    # Define our model properties here. Columns and Schema relationships
    if not isinstance(data, list):
        return process(data)
    resp = []
    for element in data:
        resp.append(process(element))
    return resp


def serialize(model, data, fields=None, exc: Optional[set] = None, rels=None, root=None, exclude=None, functions=None,
              **kwargs):
    """
    This utility function dynamically converts Alchemy model classes into a
    dict using introspective lookups. This saves on manually mapping each
    model and all the fields. However, exclusions should be noted. Such as
    passwords and protected properties.

    :param model: SQLAlchemy model
    :param data: query data
    :param functions:
    :param fields: More of a whitelist of fields to include (preferred way)
    :param rels: Whether or not to introspect to relationships
    :param exc: Fields to exclude from query result set
    :param root: Root model for processing relationships. This acts as a
    recursive sentinel to prevent infinite recursion due to selecting oneself
    as a related model, and then infinitely trying to traverse the roots
    own relationships, from itself over and over.
    :param exclude: Exclusion in set form. Currently in favour of exc param.

    Only remedy to this is also to use one way relationships. Avoiding any
    back referencing of models.

    :return: json data structure of model
    :rtype: dict
    """

    if functions is None:
        functions = {}
    if exclude is None:
        exclude = set()
    else:
        exclude = set(exclude)

    exclude = exclude.union(set(kwargs.get('exclusions', set())))

    if rels is True:
        rels = relationships(model, True)

    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, 'hidden', set())))
    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, '__hidden__', set())))

    if not fields:
        fields = set(columns(model, strformat=True))

    fields = fields.difference(exclude)

    def process(element):
        if getattr(element, '_fields', None):
            transformed = {}
            for idx, field in enumerate(element._fields):
                transformed[field] = element[idx]
            return transformed

        transformed = extract(element, fields, set(), **kwargs)
        if functions:
            for key, value in functions.items():
                transformed[f'_{key}'] = value(getattr(element, key))
        # rels = set([i.key for i in element.__mapper__.relationships]).intersection(fields)

        for item in rels or []:
            if '.' in item:
                left, right = item.split('.')
                _ = process_relationship(getattr(element, left), exclude)

                for idx, i in enumerate(getattr(element, left)):
                    _[idx][right] = extract(getattr(i, right))
                transformed[left] = _
                continue

            rel = None
            if getattr(element, item):
                rel = process_relationship(getattr(element, item), exclude)
            transformed[item] = rel
        return transformed

    if root is None:
        root = model.__tablename__

    # Define our model properties here. Columns and Schema relationships
    if not isinstance(data, list):
        return process(data)
    resp = []
    for element in data:
        resp.append(process(element))
    return resp
