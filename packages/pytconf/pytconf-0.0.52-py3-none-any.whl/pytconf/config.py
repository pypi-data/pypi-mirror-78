import itertools
import json
import os
import sys
from collections import defaultdict
from typing import Union, List, Any, Callable, Type, Dict, Set

from yattag import Doc

from pytconf.color_utils import (
    print_highlight,
    color_hi,
    print_title,
    color_ok,
    color_warn,
    print_error,
)
from pytconf.errors_collector import ErrorsCollector
from pytconf.param import Param, NO_DEFAULT
from pytconf.utils import get_logger

PARAMS_ATTRIBUTE = "_params"
DEFAULT_GROUP_NAME: str = "default"
SPECIAL_COMMANDS = {"help", "help-suggest", "help-all"}


class MetaConfig(type):
    """
    base class for all configs
    """

    def __new__(mcs, name, bases, cls_dict):
        if name != "Config":
            params_dict = dict()
            cls_dict[PARAMS_ATTRIBUTE] = params_dict
            for k, d in cls_dict.items():
                if isinstance(d, Param):
                    # assert d.default is not NO_DEFAULT
                    params_dict[k] = d
                    cls_dict[k] = d.default
        return type.__new__(mcs, name, bases, cls_dict)

    def __init__(cls, name, bases, cls_dict):
        # print(name, bases, cls_dict)
        # if len(cls.mro()) > 2:
        #     register_config(cls, name)
        #     # print("was subclassed by " + name)
        if name != "Config":
            # noinspection PyTypeChecker
            get_pytconf().register_config(cls, name)
        # print(name, cls_dict)
        super(MetaConfig, cls).__init__(name, bases, cls_dict)


class Config(metaclass=MetaConfig):
    """
        base class for all configs
    """

    @classmethod
    def get_attributes(cls: Any) -> List[str]:
        return getattr(cls, PARAMS_ATTRIBUTE).keys()
        # return [attr for attr in dir(cls) if not callable(getattr(cls, attr))
        #        and not attr.startswith("__")]

    @classmethod
    def get_params(cls: Any) -> Dict[str, Param]:
        return getattr(cls, PARAMS_ATTRIBUTE)

    @classmethod
    def get_param_by_name(cls: Any, name: str) -> Param:
        return cls.get_params()[name]


class HtmlGen:
    def __init__(self):
        document, tag, text, line = Doc().ttl()
        self.document = document
        self.tag = tag
        self.text = text
        self.line = line


def get_first_line(doc: Union[str, None]) -> Union[str, None]:
    if doc is None:
        return None
    lines = doc.split("\n")
    for line in lines:
        if line == "" or line.isspace():
            continue
        return line.strip()
    return None


class PytconfConf:
    def __init__(self):
        self._configs = set()
        self._config_names = set()
        self.main_function = None
        self.function_name_to_configs: Dict[str, List[Type[Config]]] = dict()
        self.function_name_to_suggest_configs: Dict[str, List[Type[Config]]] = dict()
        self.function_name_to_callable: Dict[str, Callable] = dict()
        self.function_group_names: Dict[str, Set[str]] = defaultdict(set)
        self.allow_free_args: Dict[str, bool] = dict()
        self.min_free_args: Dict[str, Union[int, None]] = dict()
        self.max_free_args: Dict[str, Union[int, None]] = dict()
        self.function_group_descriptions: Dict[str, str] = dict()
        self.function_group_list = []
        self.attribute_to_config: Dict[str, Type[Config]] = dict()
        self.free_args: List[str] = []
        self.app_name: Union[str, None] = None

    def register_main(self, f):
        self.main_function = f

    def register_config(self, config: Type[Config], name):
        """
        register a configuration class
        :param config:
        :param name:
        :return:
        """
        self._configs.add(config)
        self._config_names.add(name)
        # update the attributes_to_config map
        for attribute in config.get_attributes():
            if attribute in self.attribute_to_config:
                raise ValueError(
                    "pytconf: attribute [{}] appears more than once".format(attribute)
                )
            self.attribute_to_config[attribute] = config

    @classmethod
    def print_errors(cls, errors: ErrorsCollector) -> None:
        for error in errors.errors:
            print_error(error)

    def show_help(self) -> None:
        print("Usage: {} [OPTIONS] COMMAND [ARGS]...".format(self.app_name))
        doc = get_first_line(self.main_function.__doc__)
        if doc is not None:
            print()
            doc = "\n".join(map(lambda x: "  {}".format(x.strip()), doc.split("\n")))
            print_highlight("{}".format(doc))
        print()
        print("Options:")
        print("  --help         Show mandatory help")
        print("  --help-suggest Show mandatory+suggestions help")
        print("  --help-all     Show all help")
        print()
        print("Commands:")
        for function_group in self.function_group_list:
            description = self.function_group_descriptions[function_group]
            print("  {}: {}".format(function_group, description))
            for name in sorted(self.function_group_names[function_group]):
                f = self.function_name_to_callable[name]
                doc = get_first_line(f.__doc__)
                if doc is None:
                    print_highlight("    {}".format(name))
                else:
                    print("    {}: {}".format(color_hi(name), doc))
            print()

    def show_help_for_function(
        self, function_name: str, show_help_full: bool, show_help_suggest: bool
    ) -> None:
        print("Usage: {} {} [OPTIONS] [ARGS]...".format(self.app_name, function_name,))
        function_selected = self.function_name_to_callable[function_name]
        doc = get_first_line(function_selected.__doc__)
        if doc is not None:
            print()
            print_highlight("  {}".format(doc))
        print()
        print("Options:")
        print()
        for config in self.function_name_to_configs[function_name]:
            self.show_help_for_config(config)
        if show_help_suggest:
            for config in self.function_name_to_suggest_configs[function_name]:
                self.show_help_for_config(config)
        if show_help_full:
            for config in self._configs:
                self.show_help_for_config(config)

    @classmethod
    def show_help_for_config(cls, config):
        if config == Config:
            return
        doc = get_first_line(config.__doc__)
        if doc is not None:
            print_title("  {}".format(doc))
        else:
            print_title("  Undocumented parameter set")
        for name, param in config.get_params().items():
            if param.default is NO_DEFAULT:
                default = color_warn("MANDATORY")
            else:
                default = color_ok(param.t2s(param.default))
            print(
                "    {} [{}]: {} [{}]".format(
                    color_hi(name), param.get_type_name(), param.help_string, default,
                )
            )
            more_help = param.more_help()
            if more_help is not None:
                print("      {}".format(more_help))
        print()

    def process_flags(
        self, command_selected: str, flags: Dict[str, str], errors: ErrorsCollector,
    ) -> None:
        """
        Parse the args and fill the global data
        :param command_selected:
        :param flags:
        :param errors:
        """

        # set the flags into the "default" field and collect unknown flags
        unknown_flags = []
        for flag_raw, value in flags.items():
            if flag_raw not in self.attribute_to_config:
                unknown_flags.append(flag_raw)
                continue
            config = self.attribute_to_config[flag_raw]
            param = config.get_param_by_name(flag_raw)
            edit = value.startswith("=")
            if edit:
                v = param.s2t_generate_from_default(value[1:])
            else:
                v = param.s2t(value)
            setattr(config, flag_raw, v)
        if unknown_flags:
            errors.add_error("unknown flags [{}]".format(",".join(unknown_flags)))

        # check for missing parameters
        missing_parameters = []
        configs = self.function_name_to_configs[command_selected]
        for config in configs:
            for attribute in config.get_attributes():
                value = getattr(config, attribute)
                if value is NO_DEFAULT:
                    missing_parameters.append(attribute)
        if missing_parameters:
            errors.add_error(
                "missing parameters [{}]".format(",".join(missing_parameters))
            )

        # move all default values to place (this will not be needed in the new scheme)
        for config in itertools.chain(configs, self._configs):
            for attribute in config.get_attributes():
                param: Param = getattr(config, attribute)
                if isinstance(param, Param):
                    if param.default is not NO_DEFAULT:
                        setattr(config, attribute, param.default)

    @staticmethod
    def read_flags_from_config(file_name: str, flags: Dict[str, str]) -> None:
        if os.path.isfile(file_name):
            with open(file_name, "rt") as json_file:
                new_flags: Dict[str, str] = json.load(json_file)
                assert type(flags) is dict
            for k, v in new_flags.items():
                flags[k] = v

    def get_system_config(self):
        return "/etc/{}.json".format(self.app_name)
    
    def get_user_config(self):
        return os.path.expanduser("~/.config/{}.json".format(self.app_name))

    def config_arg_parse_and_launch(
        self, args: Union[List[str], None] = None, launch=True, app_name=None,
    ) -> None:
        # if we are given no args then take the from sys.argv
        if args is None:
            args = sys.argv

        # set app name
        if app_name is None:
            if args:
                self.app_name = os.path.basename(args[0])
            else:
                self.app_name = "UNKNOWN APP NAME"
        else:
            self.app_name = app_name

        # we don't need the first argument which is the script path
        if args:
            args = args[1:]

        flags: Dict[str, str] = dict()
        special_flags = set()
        errors = ErrorsCollector()
        self.free_args = []

        # read config files
        self.read_flags_from_config(file_name=self.get_system_config(), flags=flags)
        self.read_flags_from_config(file_name=self.get_user_config(), flags=flags)

        self.parse_args(args, errors, flags, special_flags)

        # handle help flags
        show_help = False
        show_help_full = False
        show_help_suggest = False

        if "help" in special_flags:
            show_help = True
        if "help-suggest" in special_flags:
            show_help = True
            show_help_suggest = True
        if "help-all" in special_flags:
            show_help = True
            show_help_full = True

        # find the selected command
        command_selected = None

        # if there are free args then the command is the first of these
        if len(self.free_args) >= 1:
            command = self.free_args.pop(0)
            if command in self.function_name_to_callable:
                command_selected = command
            else:
                errors.add_error("unknown command [{}]".format(command))

        # if there are no free args and just one function then this is it
        if len(self.function_name_to_callable) == 1:
            command_selected = list(self.function_name_to_callable.keys())[0]

        # if we have command we can check free args errors
        if command_selected is not None:
            if self.allow_free_args[command_selected]:
                min_args = self.min_free_args[command_selected]
                if min_args is not None:
                    if len(self.free_args) < min_args:
                        errors.add_error("too few free args - {} required".format(min_args))
                max_args = self.max_free_args[command_selected]
                if max_args is not None:
                    if len(self.free_args) >= max_args:
                        errors.add_error("too many free args - {} required".format(max_args))
            else:
                if len(self.free_args) > 0:
                    errors.add_error("free args are not allowed")

        if command_selected is None:
            if not show_help:
                errors.add_error("no command is selected")
        else:
            self.process_flags(command_selected, flags, errors)

        if errors.have_errors() and not show_help:
            self.print_errors(errors)
            return

        if show_help:
            if command_selected:
                self.show_help_for_function(
                    command_selected, show_help_full, show_help_suggest,
                )
            else:
                self.show_help()
            return

        if launch:
            function_to_run = self.function_name_to_callable[command_selected]
            function_to_run()

    def parse_args(self, args, errors, flags, special_flags):
        free_args_started = False
        while args:
            current = args.pop(0)
            if current.startswith("--") and not free_args_started:
                real = current[2:]
                number_of_equals = real.count("=")
                if number_of_equals == 1:
                    flag_name, flag_value = real.split("=")
                    flags[flag_name] = flag_value
                elif number_of_equals == 0:
                    if args:
                        more = args.pop(0)
                        flags[real] = more
                    elif real in SPECIAL_COMMANDS:
                        special_flags.add(real)
                    else:
                        errors.add_error(
                            "argument [{}] needs a follow-up argument".format(real)
                        )
                else:
                    errors.add_error("can not parse argument [{}]".format(real))
            else:
                self.free_args.append(current)
                free_args_started = True

    def get_html(self) -> str:
        html_gen = HtmlGen()
        doc = get_first_line(self.main_function.__doc__)
        assert doc is not None
        html_gen.line("h1", doc)
        html_gen.line("h2", "API specifications")
        with html_gen.tag("ul"):
            for function_group_name in self.function_group_list:
                function_group_description = self.function_group_descriptions[
                    function_group_name
                ]
                html_gen.line("li", function_group_name, title="function group name: ")
                html_gen.line(
                    "li",
                    function_group_description,
                    title="function group description: ",
                )
                with html_gen.tag("li"):
                    for function_name in sorted(
                        self.function_group_names[function_group_name]
                    ):
                        self.get_html_for_function(function_name, html_gen)
        return html_gen.document.getvalue()

    def get_html_for_function(self, function_name, html_gen):
        with html_gen.tag("ul"):
            f = self.function_name_to_callable[function_name]
            function_doc = get_first_line(f.__doc__)
            if function_doc is None:
                function_doc = "not description for this function"
            html_gen.line("li", function_name, title="function name: ")
            html_gen.line("li", function_doc, title="function description: ")
            with html_gen.tag("li"):
                with html_gen.tag("ul"):
                    for config in self.function_name_to_configs[function_name]:
                        with html_gen.tag("li"):
                            self.get_html_for_config(config, html_gen)

    @classmethod
    def get_html_for_config(cls, config, html_gen):
        if config == Config:
            return
        doc = get_first_line(config.__doc__)
        if doc is None:
            doc = "undocumented config"
        html_gen.line("h3", doc, title="config: ")
        with html_gen.tag("table"):
            for name, param in config.get_params().items():
                with html_gen.tag("tr"):
                    if param.default is NO_DEFAULT:
                        default = "MANDATORY"
                    else:
                        default = param.t2s(param.default)
                    if param.more_help() is None:
                        more_help = "No more help is documented"
                    else:
                        more_help = param.more_help()
                    html_gen.line("td", name)
                    html_gen.line("td", param.help_string)
                    html_gen.line("td", param.get_type_name())
                    html_gen.line("td", default)
                    html_gen.line("td", more_help)

    def write_config_file_json(self, filename):
        values: Dict[str, str] = dict()
        for config in self._configs:
            for name, param in config.get_params().items():
                if param.default is not NO_DEFAULT:
                    values[name] = param.t2s(param.default)
        with open(filename, "wt") as f:
            json.dump(values, f, indent=4)

    def write_config_file_json_user(self):
        self.write_config_file_json(self.get_user_config())

    def write_config_file_json_system(self):
        self.write_config_file_json(self.get_system_config())


_pytconf = PytconfConf()


def get_pytconf():
    return _pytconf


def config_arg_parse_and_launch(launch=True, args=None, app_name=None) -> None:
    """
    This is the real API
    """
    get_pytconf().config_arg_parse_and_launch(
        launch=launch, args=args, app_name=app_name,
    )


def get_free_args() -> List[str]:
    return get_pytconf().free_args


def register_function_group(
    function_group_name: str, function_group_description: str
) -> None:
    pt = get_pytconf()
    pt.function_group_descriptions[function_group_name] = function_group_description
    pt.function_group_list.append(function_group_name)


def register_main() -> Callable[[Any], Any]:
    def identity(f):
        get_pytconf().register_main(f)
        return f
    return identity


def register_endpoint(
    configs: List[Type[Config]] = (),
    suggest_configs: List[Type[Config]] = (),
    group: str = DEFAULT_GROUP_NAME,
    allow_free_args: bool = False,
    min_free_args: Union[int, None] = None,
    max_free_args: Union[int, None] = None,
) -> Callable[[Any], Any]:
    logger = get_logger()
    logger.debug("registering endpoint")

    def identity(f):
        register_function(
            f,
            configs=configs,
            suggest_configs=suggest_configs,
            group=group,
            allow_free_args=allow_free_args,
            min_free_args=min_free_args,
            max_free_args=max_free_args,
        )
        return f

    return identity


def register_function(
    f: Callable,
    configs: List[Type[Config]] = (),
    suggest_configs: List[Type[Config]] = (),
    group: str = DEFAULT_GROUP_NAME,
    allow_free_args: bool = False,
    min_free_args: Union[int, None] = None,
    max_free_args: Union[int, None] = None,
) -> None:
    function_name = f.__name__
    pt = get_pytconf()
    pt.function_name_to_callable[function_name] = f
    pt.function_name_to_configs[function_name] = configs
    pt.function_name_to_suggest_configs[function_name] = suggest_configs
    pt.function_group_names[group].add(function_name)
    pt.allow_free_args[function_name] = allow_free_args
    pt.min_free_args[function_name] = min_free_args
    pt.max_free_args[function_name] = max_free_args


def write_config_file_json_user():
    filename = get_pytconf().get_user_config()
    if not os.path.isfile(filename):
        get_pytconf().write_config_file_json_user()


def rm_config_file_json_user():
    filename = get_pytconf().get_user_config()
    if os.path.isfile(filename):
        os.unlink(filename)


def write_config_file_json_system():
    filename = get_pytconf().get_system_config()
    if not os.path.isfile(filename):
        get_pytconf().write_config_file_json_system()


def rm_config_file_json_system():
    filename = get_pytconf().get_system_config()
    if os.path.isfile(filename):
        os.unlink(filename)
