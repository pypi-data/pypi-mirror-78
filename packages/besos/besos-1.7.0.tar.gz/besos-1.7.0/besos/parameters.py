"""
Classes used to represent the attributes of the building that can be varied,
such as the thickness of the insulation, or the window to wall ratio.
These parameters are separate from the value that they take on during any evaluation of the model.
"""
import warnings
from abc import ABC, abstractmethod
from typing import Callable, Dict, Iterable, List, Tuple

import platypus
from deprecated.sphinx import deprecated

import eppy_funcs as ef
import pyehub_funcs as pf
from IO_Objects import AnyValue, Descriptor, DummySelector, IOBase, Selector
from config import range_parameter as conf
from errors import ModeError


# Descriptors
from besos.types import PathLike


class RangeParameter(Descriptor):
    """Represents a value that is contained in an interval.

    .. warning:: RangeParameter is actually a kind of
        :class:`Descriptor <IO_Objects.Descriptor>`,
        not a :class:`Parameter`. This naming may be confusing.
    """

    pandas_type = float
    rbf_type = "R"

    def __init__(
        self, min_val: float = conf.get("min"), max_val: float = conf.get("max")
    ):
        """

        :param max_val: the minimum value
        :param min_val: the maximum value
        """
        super().__init__()
        if min_val > max_val:
            raise ValueError("minimum is larger than maximum")
        self.min = min_val
        self.max = max_val
        self._add_reprs(["min", "max"])
        self.platypus_type = platypus.Real(self.min, self.max)

    def validate(self, value: float) -> bool:
        """Checks if `value` is contained within the range described by this Descriptor

        :param value: The value to check.
        :return: True if the value in the range, False otherwise.
        """
        min_ = float("-inf") if self.min is None else self.min
        max_ = float("inf") if self.max is None else self.max
        return min_ <= value <= max_

    def sample(self, value: float) -> float:
        """Transforms a value in [0, 1] into a value in [min, max].
        This transformation is uniform.

        :param value: a value in the interval [0, 1]
        :return: a value from the interval [min, max]
        """
        return (self.max - self.min) * value + self.min

    def __str__(self):
        return f"{self.__class__.__name__} [{self.min}, {self.max}]"


class DependentParameter(Descriptor):
    """ A parameter that the value of it depends on a range parameter"""

    def __init__(self, index: int, factor, mode):
        """

        :param index: the index of the target range parameter in parameter list
        :param mode: mode of dependent parameter.
            If mode = 'sum', value = factor - target_val.
            If mode = 'subtract', value = target_val - factor.
            If mode = 'multiple', value = factor * target_val.
            If mode= 'divide', value = factor / target_val
            If mode = 'power', value = target_val ** factor
        :param factor: the factor for calculation
        """
        super().__init__()
        mode_list = ["sum", "subtract", "multiple", "divide", "power"]
        if mode not in mode_list:
            raise ValueError(f"DependentParameter doesn't support mode {mode}")
        self.mode = mode
        self.factor = factor
        self.index = index
        self._add_reprs(["mode", "factor", "index"])
        self.platypus_type = platypus.Real(0, self.factor)

    def validate(self, value):
        """Checks if value is a valid value for this parameter.

        :param value:
        """
        return isinstance(value, (int, float))

    def sample(self, value):
        """Return a value based on mode and factor

        :param value:
        """
        return self.get_value(value)

    def get_value(self, value):
        if self.mode == "sum":
            return self.factor - value
        elif self.mode == "subtract":
            return value - self.factor
        elif self.mode == "multiple":
            return self.factor * value
        elif self.mode == "divide":
            return self.factor / value
        else:
            return value ** self.factor

    def __str__(self):
        return f"{self.__class__.__name__} index = {self.index}, mode = {self.mode}, factor = {self.factor}"


class _Category(platypus.Subset):
    def __init__(self, elements):
        super().__init__(elements=elements, size=1)

    def encode(self, value):
        return [value]

    def decode(self, value):
        return value[0]


class CategoryParameter(Descriptor):
    """Represents value that is selected from a list of possible values.

    .. warning:: CategoryParameter is actually a kind of
        :class:`Descriptor <IO_Objects.Descriptor>`,
        not a :class:`Parameter`.
        This naming may be confusing.
    """

    pandas_type = "category"

    def __init__(self, options: Iterable, **kwargs):
        """

        :param options: a list of possible value this parameter can be set to
        """
        super().__init__(**kwargs)
        self.options = list(options)
        self._add_repr("options")
        self.platypus_type = _Category(self.options)

    def validate(self, value):
        return value in self.options

    def sample(self, value):
        return self.options[int(len(self.options) * value)]


class AbstractFieldSelector(Selector, ABC):
    """Base class for selectors that modify one field in one or more objects in an EnergyPlus building"""

    def __init__(self, field_name):
        super().__init__()
        self.field_name = field_name
        self._add_repr("field_name")

    def get(self, building) -> List:
        """Gets the current values of this field from a building

        :param building: the building to retrieve values from
        :return: a list containing the current values of this selector's fields
        """
        mode = ef.get_mode(building)
        objects = self.get_objects(building)
        field_name = ef.convert_format(self.field_name, "field", mode)
        if mode == "idf":
            return [getattr(o, field_name) for o in objects]
        if mode == "json":
            return [o[field_name] for o in objects]

    def set(self, building, value) -> None:
        """Sets this field in the building to the provided value

        :param building: the building to modify
        :param value: the value to set this field to
        :return:
        """
        mode = ef.get_mode(building)
        objects = self.get_objects(building)
        field_name = ef.convert_format(self.field_name, "field", mode)
        if mode == "idf":
            for o in objects:
                setattr(o, field_name, value)
        if mode == "json":
            for o in objects:
                assert field_name in o, f"{field_name} not in {repr(o)}"
                o[field_name] = value

    def multiply(self, building, value) -> None:
        """Multiplies this field in the building by the provided value

        :param building: the building to modify
        :param value: the value to multiply this field by
        :return:
        """
        mode = ef.get_mode(building)
        objects = self.get_objects(building)
        field_name = ef.convert_format(self.field_name, "field", mode)
        if mode == "idf":
            for o in objects:
                setattr(o, field_name, value * getattr(o, field_name))
        if mode == "json":
            for o in objects:
                assert field_name in o, f"{field_name} not in {repr(o)}"
                o[field_name] = value * o[field_name]

    def add(self, building, value) -> None:
        """Adds to this field in the building by the provided value

        :param building: the building to modify
        :param value: the value to add to this field
        :return:
        """
        mode = ef.get_mode(building)
        objects = self.get_objects(building)
        field_name = ef.convert_format(self.field_name, "field", mode)
        if mode == "idf":
            for o in objects:
                setattr(o, field_name, value + getattr(o, field_name))
        if mode == "json":
            for o in objects:
                assert field_name in o, f"{field_name} not in {repr(o)}"
                o[field_name] = value + o[field_name]

    @abstractmethod
    def get_objects(self, building) -> List:
        """Returns a list of the object this selector applies to

        :param building: the building to search for objects
        :return: a list of the objects this selector applies to
        """
        pass


class FilterSelector(AbstractFieldSelector):
    """A selector that uses a custom function to find which objects it should modify"""

    def __init__(self, get_objects, field_name):
        """

        :param get_objects: a function that takes a building and returns the objects this selector should modify
        :param field_name: the field to modify
        """
        super().__init__(field_name)
        self._get_objects = get_objects
        self._add_repr("get_objects", "_get_objects")

    def get_objects(self, building):
        return self._get_objects(building)


class FieldSelector(AbstractFieldSelector):
    """A selector that modifies one or more fields in an EnergyPlus building,
    based on the class, object and field names"""

    def __init__(
        self, class_name: str = None, object_name: str = None, field_name: str = None
    ):
        """

        :param class_name: class of the object to modify
            ex: 'Material'
        :param object_name: name of the object to modify
            ex: 'Mass NonRes Wall Insulation'
        :param field_name: name of the field to modify
            ex: Thickness
        """
        super().__init__(field_name=field_name)
        self.class_name = class_name
        self.object_name = object_name
        self._add_reprs(["class_name", "object_name"], check=True)

    def get_objects(self, building) -> List:
        """Retrieves the objects that this selector will affect from the building.

        :param building: the building to search
        :return: a list of the objects found
        """
        mode = ef.get_mode(building)
        if mode == "idf":
            if self.class_name is not None:
                class_name = ef.convert_format(self.class_name, "class", "idf")
            else:
                class_name = None
            if self.object_name == "*":
                if class_name is None:
                    raise TypeError(
                        "When object_name='*', class_name must be specified."
                    )
                return building.idfobjects[class_name]
            if self.object_name and class_name:
                # this is probably the most reliable way to select an idfObject.
                return [building.getobject(key=class_name, name=self.object_name)]
            if self.object_name:
                # There should only one object matching the name, assuming the idf is valid
                return [ef.get_idfobject_from_name(building, self.object_name)]
            if class_name is not None:
                # assume that we want the first object matching the key
                # TODO: is this specific enough, or should we remove it? our JSON code does not support this
                return [building.idfobjects[class_name][0]]
            else:  # we have neither object_name nor class_name
                raise TypeError("Either class_name or object_name must be specified.")
        elif mode == "json":
            if self.object_name == "*":
                if not self.class_name:
                    raise TypeError(
                        "When object_name='*', class_name must be specified."
                    )
                return list(building[self.class_name].values())
            if self.object_name and self.class_name:
                # this is probably the most reliable way to select an idfObject.
                return [building[self.class_name][self.object_name]]
            if self.object_name:
                # There should only one object matching the name, assuming the building is valid
                result = [
                    obj
                    for objs in building.values()
                    for name, obj in objs.items()
                    if name == self.object_name
                ]
                if len(result) != 1:
                    warnings.warn(
                        f"found {len(result)} objects with object_name: {self.object_name}, expected 1"
                    )
                return result
            if self.class_name:
                result = list(building[self.class_name].items())
                if len(result) == 1:
                    return result
                raise ValueError(
                    f"multiple objects with class_name {self.class_name}."
                    f"Cannot guarantee a reliable ordering"
                )
            else:  # we have neither object_name nor class_name
                raise TypeError("Either class_name or object_name must be specified.")
        raise ModeError(mode)


class PathSelector(Selector):
    """A Selector for modifying EnergyHub objects using a path."""

    def __init__(self, parameter_path=None):
        """
        :param parameter_path: the path to the parameter to modify for the EnergyHub
        """
        super().__init__()
        self.parameter_path = parameter_path

    def get(self, hub):
        return pf.get_by_path(hub.__dict__, self.parameter_path)

    def set(self, hub, value):
        pf.set_by_path(hub.__dict__, self.parameter_path, value)

    def multiply(self, hub, value):
        self.set(hub, value * self.get(hub))

    def add(self, hub, value):
        self.set(hub, value + self.get(hub))

    def setup(self, hub) -> None:
        """Modifies the building so that it is ready for this selector"""
        pass


class GenericSelector(Selector):
    """A selector that supports custom get/set functions"""

    def __init__(
        self, set: Callable = None, get: Callable = None, setup: Callable = None
    ):
        """

        :param set: The function to use when setting.
            Must accept a building and a value. Can modify the building in any way.
        :param get: The function to use when getting a value from a building.
            Must accept a building, and should return a list of the current values
            of the fields this selector affects.
        :param setup: The function to use when setting up the building.
            This function must accept a building. It may modify the building in any way.
            This will be run once when the evaluator is initialized with a building.
            (or when the building the evaluator uses is changed.)
        """
        super().__init__()
        self._set = set
        self._get = get
        self._setup = setup
        for attr in ("set", "get", "setup"):
            self._add_repr(attr, f"_{attr}", True)

    def set(self, building, value):
        """A custom function for setting this field in the building to the provided value

        :param building: the building to modify
        :param value: the value to set this field to
        """
        if self._set is not None:
            return self._set(building, value)
        raise NotImplementedError

    def get(self, building):
        """A custom function for getting the current values of this field from a building

        :param building: the building to retrieve values from
        """
        if self._get is not None:
            return self._get(building)
        raise NotImplementedError

    def setup(self, building):
        """A custom function for modifying the building so that it is ready for this selector

        :param building: the building to modify
        """
        if self._setup is None:
            return
        self._setup(building)


# Parameters


class Parameter(IOBase):

    mode_options = {"Set", "Multiply", "Add"}

    def __init__(
        self,
        selector: Selector = None,
        value_descriptor: Descriptor = None,
        mode="Set",
        name="",
    ):
        """

        :param selector: a Selector describing how to modify the building
        :param value_descriptor: a Descriptor specifying which values to use
        :param mode: the desired transformation function to use
            Set: set the sample as the value
            Multiply: multiply the pre-existing value by the sample factor
            Add: add the sample value onto the pre-existing value
        :param name: the name of the Parameter. Used for readability
            and column labelling.
        """
        super().__init__(name=name)
        self.selector = selector or DummySelector()
        self.value_descriptor = value_descriptor or AnyValue()
        assert mode in self.mode_options, f"Invalid mode option"
        self.mode = mode
        self._add_reprs(["selector", "value_descriptor"], True)

    def transformation_function(self, building, value) -> None:
        """Mutates the building based on the value provided."""
        if self.mode == "Multiply":
            self.selector.multiply(building, value)
        if self.mode == "Add":
            self.selector.add(building, value)
        if self.mode == "Set":
            self.selector.set(building, value)

    def sample(self, value: float):
        """Takes a value in the range 0-1 and returns a valid value for this parameter"""
        return self.value_descriptor.sample(value)

    def validate(self, value):
        """Checks if value is a valid value for this parameter.

        :param value:
        :return: True if the value is valid False otherwise
        """
        return self.value_descriptor.validate(value)

    def setup(self, building) -> None:
        self.selector.setup(building)

    @property
    def _default_name(self):
        """The name to use for this Parameter if no name was provided"""
        if hasattr(self.selector, "field_name"):
            return self.selector.field_name

    @property
    def platypus_type(self):
        """The platypus equivalent of this parameter"""
        return self.value_descriptor.platypus_type


@deprecated(
    version="1.6.0",
    reason=(
        "Use a :class:`PathSelector` and a :class:`Parameter` instead. "
        "These have been swapped in automatically."
    ),
)
class ParameterEH:
    """A parameter for use with EnergyHub"""

    mode_options = {"Set", "Multiply", "Add"}

    # this method overrides the default behaviour when trying to create a new ParameterEH
    # instead of creating a ParameterEH, it creates a PathSelector,
    # puts it in a Parameter, and returns that parameter.
    def __new__(
        cls,
        parameter_path: List[str] = None,
        value_descriptor: Descriptor = None,
        mode: str = "Set",
        **kwargs,
    ):
        """Swaps out the ParameterEH for a Parameter and PathSelector for backwards compatibility.

        :param parameter_path: the path to the parameter to modify for the EnergyHub
        :param value_descriptor: a Descriptor specifying which values to use
        :param mode: the desired transformation function to use
          Set: set the sample as the value
          Multiply: multiply the pre-existing value by the sample factor
          Add: add the sample value onto the pre-existing value
        """
        selector = PathSelector(parameter_path)
        return Parameter(
            selector=selector, value_descriptor=value_descriptor, mode=mode, **kwargs
        )


class wwrSelector(Selector):
    """
    :class:`Selector <IO_Objects.Selector>` for window to wall ratio.
    """

    def __init__(self):
        super().__init__()

    def set(self, building, value):
        """Sets the window to wall ratio of the building to the provided value

        :param building: the building to modify
        :param value: the value of the wwr
        """
        ef.wwr_all(building, value)

    def get(self, building):
        # This feature has not yet been requested
        raise NotImplementedError(
            "Calculation of window to wall ratio is not supported."
        )

    def setup(self, building) -> None:
        """Adjusts the building to have at most one window per wall,
        making it ready to have its window to wall ratio modified.

        :param building: The building to adjust
        """
        ef.one_window(building)


def wwr(value_descriptor=RangeParameter(0.01, 0.99), **kwargs) -> Parameter:
    """Makes a window-to-wall-ratio parameter.

    :param value_descriptor: a parameter describing the valid window-wall-ratios
    :return: Parameter
    """
    if isinstance(value_descriptor, RangeParameter):
        min_val, max_val = value_descriptor.min, value_descriptor.max
        if not (0 < min_val < max_val < 1):
            if 0 == min_val:
                raise ValueError("min must be strictly greater than 0")
            if 1 == max_val:
                raise ValueError("max must be strictly less than 1")
            raise ValueError(
                "Invalid min and max values. 0 < min < max < 1 must be satisfied."
            )
    else:
        warnings.warn(
            f"wwr is intended to be used with RangeParameter. Your value_descriptor is {value_descriptor}"
        )

    selector = wwrSelector()
    name = kwargs.pop("name", "Window to Wall Ratio")
    return Parameter(
        selector=selector, value_descriptor=value_descriptor, name=name, **kwargs
    )


# Simpler ways to get specific transformers
keyFormat = Dict[str, Dict[str, Tuple[float, float]]]


# TODO: Formalize this syntax, maybe add a guaranteed order
def expand_plist(pList: keyFormat) -> List:
    """This function expands a nested dictionary of the correct format into a list of inputs.

    The dictionary should have the format:
    {'idf object name': {'idf object1 property name': (min_value, max_value)}

    Both layers of the dictionaries can have as many names as desired"""
    return [
        Parameter(
            FieldSelector(object_name=name, field_name=prop),
            RangeParameter(min_val=min_, max_val=max_),
            name=prop,
        )
        for name, subProps in pList.items()
        for prop, (min_, max_) in subProps.items()
    ]
