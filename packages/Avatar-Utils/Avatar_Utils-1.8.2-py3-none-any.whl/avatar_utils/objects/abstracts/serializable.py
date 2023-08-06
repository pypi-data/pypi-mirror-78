import json
import re
from copy import deepcopy
from dataclasses import dataclass as python_dataclass
from logging import getLogger
from typing import Any

# import avatar_utils.objects - required
import avatar_utils.objects

logger = getLogger(__name__)


@python_dataclass
class Serializable:

    def __post_init__(self):
        self.repr_type = self.__fullname()

    # reliable but not the most productive way to serialize as a dict
    def to_dict(self) -> dict:
        json_data = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        return json.loads(json_data)

    @staticmethod
    def class_attributes(cls):
        attributes = []

        for key in cls.__dict__.keys():
            if key == '__dataclass_fields__':
                dataclass_fields = getattr(cls, key)
                for field in dataclass_fields.keys():
                    attributes.append(field)

        return attributes

    @staticmethod
    def any_to_dict(data: Any):
        data_copy = deepcopy(data)

        if isinstance(data_copy, Serializable):
            res = data_copy.to_dict()
            return res
        elif isinstance(data_copy, list):
            for i in range(len(data_copy)):
                data_copy[i] = Serializable.any_to_dict(data=data_copy[i])
            return data_copy
        elif isinstance(data_copy, dict):
            for key, value in data_copy.items():
                data_copy[key] = Serializable.any_to_dict(value)
            return data_copy
        else:
            raise NotImplementedError

    # все вложенные объекты десериализуются как Serializable, то есть у них должно быть поле repr_type
    @classmethod
    def from_dict(cls, data: Any, objects_existing_check: bool = False) -> Any:

        def from_dict_with_check(cls, data: Any) -> (Any, bool):
            if isinstance(data, dict):
                # serializable class
                if cls.__name__ == 'Serializable':
                    logger.debug('Deserialize object in general. Using Serializable')
                    repr_type = data.pop('repr_type', None)

                    if repr_type:
                        # check precisely
                        if not injection_detected(cls=cls, repr_type=repr_type):
                            # evaluate actual class
                            actual_cls = eval(repr_type)
                            return extract_class(actual_cls, data)
                        else:
                            logger.error('Injection detected. Skip evaluation')
                            return {}, False

                    else:
                        logger.debug('Dict is received')

                        result = {}
                        object_has_met = False
                        for k, v in data.items():
                            result[k], inner_object_has_met = from_dict_with_check(cls=Serializable, data=v)
                            object_has_met = object_has_met | inner_object_has_met

                        return result, object_has_met
                else:
                    # concrete class received
                    return extract_class(cls, data)

            elif isinstance(data, list):
                object_has_met = False
                i: int
                for i in range(data.__len__()):
                    data[i], inner_object_has_met = from_dict_with_check(cls, data[i])
                    object_has_met = object_has_met | inner_object_has_met
                return data, object_has_met
            else:
                return data, False

        def injection_detected(cls, repr_type: str):
            module_name = 'avatar_utils.objects'
            import sys, inspect
            for name, obj in inspect.getmembers(sys.modules[module_name]):
                if inspect.isclass(obj):
                    qualify_path = str(obj)[8:-2]
                    # concrete classes in avatar_utils.objects module
                    if qualify_path.startswith(module_name) and not qualify_path.lower().__contains__('abstract'):
                        # class exists
                        if qualify_path.endswith(repr_type):
                            # acceptable only
                            if re.match('^[A-Za-z_\\.]*$', qualify_path):
                                return False

            return True

        def extract_class(cls, data: Any):

            attributes = Serializable.class_attributes(cls)

            result = {}
            for k, v in data.items():
                if k in attributes:
                    result[k], skip = from_dict_with_check(cls=Serializable, data=v)
                else:
                    logger.warning('Skip unexpected keyword argument "%s"', k)
            extracted_cls = cls(**result)
            return extracted_cls, True

        result, object_has_met = from_dict_with_check(cls, deepcopy(data))

        if objects_existing_check:
            if not object_has_met:
                raise TypeError('No object has met')

        return result

    def __fullname(self):
        # o.__module__ + "." + o.__class__.__qualname__ is an example in
        # this context of H.L. Mencken's "neat, plausible, and wrong."
        # Python makes no guarantees as to whether the __module__ special
        # attribute is defined, so we take a more circumspect approach.
        # Alas, the module name is explicitly excluded from __qualname__
        # in Python 3.

        module = self.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return self.__class__.__name__  # Avoid reporting __builtin__
        else:
            return module + '.' + self.__class__.__name__
