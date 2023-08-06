import toml
from datetime import datetime, date
import os
import sys
import numpy as np
import logging
import pandas as pd
import functools
from dotmap import DotMap
import unittest
from pathlib import Path
from .dtgs import DtgContainer

logger = logging.getLogger(__name__)


class UndefinedValueType:
    """
    This class is defined such that any instance foo satisfies:
        (a) bool(foo) is False
        (b) If return_self_on_attr_error=True, then, for any attribute bar,
            foo.bar is foo. This implies that, for any N>1,
            foo.bar1.bar2.(...).barN is foo

    We will use instances of this class to mark things such as missing
    config file values, unspecified defaults in functions, etc. We don't
    want to use None in these cases, as None may be a valid arg value.
    """

    def __init__(
        self,
        name="<UndefinedValueType object>",
        return_self_on_attr_error=False,
    ):
        self._name = name
        self._return_self_on_attr_error = return_self_on_attr_error

    # Define __setstate__ and __getstate__ to handle serialisation (pickling)
    # and avoid recursion errors (UndefinedConfigValue is a recursive object)
    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def __getattr__(self, item):
        if self._return_self_on_attr_error:
            return self
        else:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, item
                )
            )

    def __bool__(self):
        return False

    def __repr__(self):
        return self._name

    __str__ = __repr__


UndefinedConfigValue = UndefinedValueType(
    name="UndefinedConfigValue", return_self_on_attr_error=True
)
NoDefaultProvided = UndefinedValueType(name="NoDefaultProvided")


class UndefinedConfigValueError(Exception):
    pass


class ConfigParsingError(Exception):
    pass


class _ConfigDict(DotMap):
    """
    Acts like a normal dictionary, except for:
        (a) Accepts getting/setting values using dot notation (inherited from
            the dotmap package). This means that instance.key is equivalent
            to instance[key].
        (b) Returns UndefinedConfigValue if a key is not present instead
            of raising KeyError.
    """

    def __init__(self, *args, **kwargs):
        kwargs["_dynamic"] = False
        super(_ConfigDict, self).__init__(*args, **kwargs)

    # Handling value if retrieving as dict key
    def __getitem__(self, item):
        return self.get(item, default=UndefinedConfigValue)

    # Handling value if using dot notation
    # __getattr__ is only called if the attribute does NOT exist
    def __getattr__(self, item):
        return self.get(item, default=UndefinedConfigValue)


def _rgetattr(obj, attr, *args):
    """
    Works similarly to getattr, but:
        (a) Handles dotted attr strings. Adapted from:
            <https://stackoverflow.com/questions/31174295/
             getattr-and-setattr-on-nested-subobjects-chained-properties>
        (b) Converts input/output dictionaries into objects of our module's
            _ConfigDict class
    """

    def _getattr(obj, attr):
        if type(obj) == dict or isinstance(obj, DotMap):
            obj = _ConfigDict(obj)
        rtn = getattr(obj, attr, *args)
        if isinstance(rtn, DotMap):
            rtn = _ConfigDict(rtn)
        return rtn

    return functools.reduce(_getattr, [obj] + attr.split("."))


def _parse_dtg_entires(dtgs_config):
    try:
        cycle_length = dtgs_config["cycle_length"]
    except (KeyError):
        cycle_length = "3H"
        logger.warning("Missing cycle_length in config. Setting it to 3H.")

    dtg_range_opt_labels = set(["start", "end"])
    if "list" in dtgs_config.keys():
        if not dtg_range_opt_labels.isdisjoint(dtgs_config.keys()):
            logger.warning(
                'Found DTG options "list" and also at least '
                + 'one of [%s]. Parsing only values passed in "list".',
                ", ".join(dtg_range_opt_labels),
            )
        try:
            dtgs = DtgContainer(dtgs_config["list"], cycle_length=cycle_length)
        except (ValueError) as e:
            logger.exception(e)
            raise ValueError("Bad 'dtg.list' or 'dtg.cycle_length' config.")
    else:
        try:
            start = dtgs_config["start"]
            end = dtgs_config["end"]
        except (KeyError) as e:
            logger.exception(e)
            msg = " Either 'dtgs.list' or both 'dtgs.start' and "
            msg += "'dtgs.end' must specified in config file."
            raise UndefinedConfigValueError(msg)
        try:
            dtgs = DtgContainer(
                start=dtgs_config["start"],
                end=dtgs_config["end"],
                cycle_length=cycle_length,
            )
        except (ValueError, TypeError) as e:
            logger.exception(e)
            raise ValueError("Bad 'dtg.start/end/cycle_length' config.")

    return dtgs


def _validate_value(
    optname,
    optval=None,
    default=None,
    choices=None,
    maxval=None,
    minval=None,
    astype=None,
):
    if optval is None:
        optval = default
    # Pre-parsing choices. They may sometimes be functions.
    try:
        choices = choices()
    except (TypeError):
        pass
    # Cast to desired type, if passed
    if astype is not None:
        try:
            optval = astype(optval)
            if default is not None:
                default = astype(default)
            if maxval is not None:
                maxval = astype(maxval)
            if minval is not None:
                minval = astype(minval)
            if choices is not None:
                choices = list(map(astype, choices))
        except (TypeError, ValueError) as e:
            logger.exception(e)
            msg = 'Could not parse "{0}" using "astype={1}"'.format(
                optname, astype
            )
            raise ValueError(msg)

    if (choices is not None) and (optval not in choices):
        raise ValueError(
            '{0} "{1}" not valid. Valid choices are: {2}'.format(
                optname, optval, ", ".join(map(str, choices))
            )
        )
    if (minval is not None) and optval < minval:
        raise ValueError(
            "{0} value ({1}) smaller than the allowed min ({2})".format(
                optname, optval, minval
            )
        )
    if (maxval is not None) and optval > maxval:
        raise ValueError(
            "{0} value ({1}) larger than the allowed max ({2})".format(
                optname, optval, maxval
            )
        )
    return optval


def _validate_outlier_rm_method_config(clustering_method, config):
    if clustering_method in ["dbscan", "rsl"]:
        valid_out_rm_methods = ["lof", "iterative", "reclustering"]
    elif clustering_method == "hdbscan":
        valid_out_rm_methods = ["glosh", "lof", "iterative", "reclustering"]
    else:
        logger.warning(
            "Cannot verify validity of outlier_removal for  "
            + 'clustering method "%s". Passing on "as is"',
            clustering_method,
        )
        return config

    if config["method"] not in valid_out_rm_methods:
        raise ValueError(
            (
                'outlier_removal method "{}" not valid for '
                + 'clustering_method "{}". Valid values are: {}'
            ).format(
                config["method"],
                clustering_method,
                ", ".join(valid_out_rm_methods),
            )
        )

    if config["method"] == "iterative":
        recognised_opts = dict(
            max_n_iter=dict(default=100, minval=0),
            max_n_stdev=dict(default=2, minval=0),
        )
        for optname in config:
            if optname == "method":
                continue
            try:
                optconfigs = recognised_opts[optname]
            except (KeyError):
                logger.warning(
                    'Config opt "%s" (in %s->outlier_removal->iterative)'
                    + ' not recognised. Passing on "as is"',
                    optname,
                    clustering_method,
                )
                continue
            try:
                optval = config[optname]
            except (KeyError):
                optval = None
            config[optname] = _validate_value(
                optname="{} ({} -> outlier_removal -> iterative)".format(
                    optname, clustering_method
                ),
                optval=optval,
                **optconfigs
            )

    return config


class ParsedConfig:
    def __init__(
        self,
        file=Path().resolve() / "config.toml",
        global_default=NoDefaultProvided,
    ):
        self._file = Path(file)
        # Keep the config's raw data, mostly for debugging purposes
        self._raw = toml.load(self._file.resolve())

        # Directory where NetAtmo data is supposed to be found
        try:
            rootdir = self._raw["general"]["data_rootdir"]
            # expandvars adds support to envvars as part of data_rootdir
            self.data_rootdir = Path(os.path.expandvars(rootdir))
        except (KeyError):
            raise UndefinedConfigValueError(
                "data_rootdir not specified in config file"
            )

        self.global_default = global_default

        # Define some metadata about recognised clustering methods
        # and respective options. This will help parsing.
        self._recog_ops_for_cluster_methods = {}

        self._recog_ops_for_cluster_methods["dbscan"] = dict(
            eps=dict(default=10, minval=0),
            min_samples=dict(default=5, minval=1),
            outlier_removal={},  # This will be parsed separately
            obs_weights=dict(default={}, astype=dict),
        )
        self._recog_ops_for_cluster_methods["hdbscan"] = dict(
            min_samples=dict(default=5, minval=1),
            min_cluster_size=dict(default=5, minval=1),
            max_iter_refine=dict(default=100, minval=0),
            stdev_refine=dict(default=2, minval=0),
            obs_weights=dict(default={}, astype=dict),
            eps=dict(default=10, minval=0),
            outlier_removal={},  # This will be parsed separately
        )
        self._recog_ops_for_cluster_methods["rsl"] = dict()

        # Now parse input data (validate choices, etc)
        #
        # Set self._clustering_method to the chosen clustering_method
        # and set self._parsed to contain the parsed configs for
        # self._clustering_method. self.get will return values from
        # self._parsed.
        try:
            self.set_clustering_method(
                self._raw["general"]["clustering_method"]
            )
        except (KeyError):
            raise UndefinedConfigValueError(
                'clustering_method not defined under "general" in config file'
            )
        # Make sure at least one DTG is defined and that
        # defined DTG(s) are valid
        try:
            dtgs_config_raw = self._raw["general"]["dtgs"]
        except (KeyError):
            raise UndefinedConfigValueError(
                "DTG(s) not specified in config file!"
            )
        self._dtgs = _parse_dtg_entires(dtgs_config_raw)

        # Validate options that are valid for each individual command
        self.commands = _ConfigDict(dict(cluster={}, select={}, apps={},))
        def_stat_rejec_tol = 0.15
        try:
            self.commands.select.station_rejection_tol = _validate_value(
                "commands --> select --> station_rejection_tol",
                self._raw["commands"]["select"]["station_rejection_tol"],
                default=def_stat_rejec_tol,
                minval=0,
                maxval=1,
                astype=type(1.0),
            )
        except (KeyError):
            self.commands.select.station_rejection_tol = def_stat_rejec_tol

    @property
    def clustering_method(self):
        return self._clustering_method

    @property
    def dtgs(self):
        return self._dtgs

    @property
    def recognised_clustering_methods(self):
        return self._recog_ops_for_cluster_methods.keys()

    def set_clustering_method(self, method):
        self._clustering_method = method
        self._parsed = self._parse_selected_clustering_method_opts()

    def _parse_selected_clustering_method_opts(self):
        try:
            raw = self._raw["clustering_method"][self.clustering_method]
        except (KeyError):
            if self.global_default is NoDefaultProvided:
                raise UndefinedConfigValueError(
                    'No "clustering_method.{}"'.format(self.clustering_method)
                    + " block found in the config file"
                )
            else:
                logger.warning(
                    """
                    No "clustering_method.%s" block found in the config file.
                    Using the global default (= %s) for the whole config.
                    """,
                    self.clustering_method,
                    self.global_default,
                )
            return self.global_default
        try:
            opts = self._recog_ops_for_cluster_methods[self.clustering_method]
        except (KeyError):
            logger.warning(
                """
                No sanity checks for clustering method "{0}" are available
                at the moment. The whole "clustering_method.{0}" config file
                block will be used "as is".
                """.format(
                    self.clustering_method
                )
            )
            return raw

        parsed = {}
        for attr, attr_value in raw.items():
            try:
                if attr == "outlier_removal":
                    parsed[attr] = _validate_outlier_rm_method_config(
                        self.clustering_method, attr_value
                    )
                else:
                    opts = self._recog_ops_for_cluster_methods[
                        self.clustering_method
                    ][attr]
                    parsed[attr] = _validate_value(attr, attr_value, **opts)
            except (KeyError):
                logger.warning(
                    'Config opt "%s" not recognised by parser for '
                    + 'clustering method "%s". '
                    + 'Passing on "as is".',
                    attr,
                    self.clustering_method,
                )
                parsed[attr] = attr_value
        return parsed

    # Define __setstate__ and __getstate__ to handle serialisation (pickling)
    # and avoid recursion errors
    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    # Handling the getter method
    # __getattr__ is only called if the attribute does NOT exist
    def __getattr__(self, item):
        return self.get(item)

    def get(self, item, default=NoDefaultProvided):
        """Return parsed config values for the active clustering method"""
        # Re-format item so that the retrievals
        #            instance.get(['at1', 'at2', (...), 'atn']),
        #            instance.get(['at1.at2.(...).atn']),
        #            instance.at1.at2.(...).atn
        # are equivalent.
        if not isinstance(item, str):
            try:
                item = ".".join(iter(item))
            except (TypeError):
                msg = (
                    "The attribute(s) to be retrieved must be specified "
                    + "either as a string or as an iterable type. "
                    + 'Got "{}" instead (type={})'
                ).format(item, type(item))
                raise TypeError(msg)

        try:
            rtn = _rgetattr(self._parsed, item)
            if rtn is UndefinedConfigValue:
                # Handle this in the except block below
                raise AttributeError("{} is UndefinedConfigValue".format(item))
            else:
                return rtn
        except (AttributeError):
            if default is not NoDefaultProvided:
                logger.debug(
                    'No "%s" in config. Using passed default (= %s)',
                    item,
                    default,
                )
                return default
            elif self.global_default is not NoDefaultProvided:
                logger.warning(
                    'No "%s" in config for "%s". Using global_default (= %s)',
                    item,
                    self.clustering_method,
                    self.global_default,
                )
                return self.global_default
            else:
                raise UndefinedConfigValueError(
                    'Config has no value for "{}", '.format(item)
                    + "and no default has been passed."
                )


def read_config(config_path):
    logging.info("Reading config file %s", Path(config_path).resolve())
    config = ParsedConfig(
        file=config_path, global_default=UndefinedConfigValue
    )
    return config
