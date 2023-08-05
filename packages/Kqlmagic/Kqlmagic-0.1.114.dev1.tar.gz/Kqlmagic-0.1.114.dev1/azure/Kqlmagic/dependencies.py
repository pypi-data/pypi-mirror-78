# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import warnings
import re


from .constants import Constants
from .log import logger, isNullLogger


saved_formatwarning = warnings.formatwarning


class Dependencies(object):

    IGNORE_WARNINGS = "ignore"
    SHOW_WARNINGS = "default"
    RAISE_WARNINGS = "error"

    PREFIX_TAG = "###"
    MANDATORY_TAG = "#M#" # Kqlmagic cannot work without it
    BASE_TAG = "#B#"      # Kqlmagic nase faeture, however they may be disbled
    OPTIONAL_TAG = "#O#"  # Kqlmagic optional feature
    EXTRA_TAG = "#E#"
    DISABLED_TAG = "#D#"
    MANDATORY_MODULES_REGEX = r'^#M#'
    BASE_MODULES_REGEX = r'^#B#'
    OPTIONAL_MODULES_REGEX = r'^#O#'
    EXTRA_MODULES_REGEX = r'^#E#'
    DISABLED_MODULES_REGEX = r'^#D#'
    ALL_MODULES_REGEX = r'^(#M#|#B#|#O#|#E#|#D#)'

    mandatory_if_not_saw_tag = DISABLED_TAG if Constants.IS_SAW_INSTALLATION else MANDATORY_TAG
    optional_if_not_saw_tag = DISABLED_TAG if Constants.IS_SAW_INSTALLATION else OPTIONAL_TAG
    mandatory_if_saw_tag = MANDATORY_TAG if Constants.IS_SAW_INSTALLATION else OPTIONAL_TAG
    mandatory_if_saw_tag = MANDATORY_TAG if Constants.IS_SAW_INSTALLATION else OPTIONAL_TAG

    VERSION_IN_MODULE=True

    dependencies = (
        ('traitlets', 'traitlets', MANDATORY_TAG, "won't be able to use execute Kqlmagic", VERSION_IN_MODULE),
        ('requests', 'requests', MANDATORY_TAG, "won't be able to query sources, except local cache", VERSION_IN_MODULE),
#        ('adal', 'adal', MANDATORY_TAG, "won't be able to authenticate using adal authentication modes", VERSION_IN_MODULE),
        ('msal', 'msal', MANDATORY_TAG, "won't be able to authenticate using msal authentication modes", VERSION_IN_MODULE),
        ('msal_extensions.windows', 'msal_extensions', optional_if_not_saw_tag, "won't be able to authenticate using msal Single-Sign-On authentication modes", 'msal_extensions'),
        ('pandas', 'pandas', BASE_TAG, "won't be able to use dataframes", VERSION_IN_MODULE),
        ('IPython', 'ipython', MANDATORY_TAG, "won't be to execute as an jupyter magic", VERSION_IN_MODULE),
        ('ipykernel', 'ipykernel', MANDATORY_TAG, "won't be to execute as an jupyter magic on some jupyter variants", VERSION_IN_MODULE),
        ('pygments', 'pygments', OPTIONAL_TAG, "json objects won't be decorated with colors", VERSION_IN_MODULE),
        ('pygments.lexers.data', 'pygments', OPTIONAL_TAG, "json objects won't be decorated with colors", 'pygments'),
        ('pygments.formatters.terminal', 'pygments', OPTIONAL_TAG, "json objects won't be decorated with colors", 'pygments'),
        ('pyperclip', 'pyperclip', OPTIONAL_TAG, "copy/paste feature will be disabled in device code authentication", VERSION_IN_MODULE),
        ('azure.common.credentials', 'azure-common', OPTIONAL_TAG, "-try_azcli_login and -try_azcli_login_subscription authentication options will be dsiabled", 'azure.common'),
        ('msrestazure.azure_active_directory', 'msrestazure', OPTIONAL_TAG, "-try_msi authentication options will be dsiabled", 'msrestazure'),
        ('psutil', 'psutil', OPTIONAL_TAG, "some jupyter variants may not be detected correctly", VERSION_IN_MODULE),
        ('prettytable', 'prettytable', mandatory_if_not_saw_tag, "won't be able to display tables", VERSION_IN_MODULE),
        ('tabulate', 'tabulate', mandatory_if_saw_tag, "won't be able to display tables", VERSION_IN_MODULE),
        ('matplotlib.pyplot', 'matplotlib', DISABLED_TAG, 'plotting with matplotlib will be dsiabled', 'matplotlib'),
        ('matplotlib.cm', 'matplotlib', DISABLED_TAG, "matplotlib color maps (palettes) won't be available in plots", 'matplotlib'),
        ('matplotlib.colors', 'matplotlib', DISABLED_TAG, "matplotlib color maps (palettes) won't be available in plots", 'matplotlib'),
        # ('foofoo', 'foofoo', EXTRA_TAG, 'plotting with foofoo will be dsiabled', VERSION_IN_MODULE),
        # ('blabla', 'blabla', OPTIONAL_TAG, 'plotting with blabla will be dsiabled', VERSION_IN_MODULE),
        ('pkg_resources', 'setuptools', OPTIONAL_TAG, 'may not detect new version exist in PyPI', 'setuptools'),

        ('plotly', 'plotly', BASE_TAG, "won't display charts with plotly", VERSION_IN_MODULE),
        ('plotly.graph_objs', 'plotly', BASE_TAG, "won't display charts with plotly", 'plotly'),
        
        ('flask', 'flask', BASE_TAG, "popups and some authentication modes won't work on some local jupyter variants", VERSION_IN_MODULE),
        ('isodate', 'isodate', MANDATORY_TAG, "Azure Monitor AI/LA timespan will be disabled", VERSION_IN_MODULE),
        ('dateutil.parser', 'python-dateutil', MANDATORY_TAG, "won't be able handle datetime properly", 'dateutil'),
        ('markdown', 'markdown', MANDATORY_TAG, "some help information won't be nicely displayed", VERSION_IN_MODULE),
        ('bs4', 'beautifulsoup4', MANDATORY_TAG, "some help information won't be nicely displayed", VERSION_IN_MODULE),
        ('lxml', 'lxml', MANDATORY_TAG, "some help information won't be nicely displayed", VERSION_IN_MODULE),

        ('ipywidgets', 'ipywidgets', EXTRA_TAG, "widget features will be disabled", VERSION_IN_MODULE),

        ('cryptography.fernet', 'cryptography', EXTRA_TAG, "Single Sign On feature will be disabled", 'cryptography'),
        ('cryptography.hazmat.backends', 'cryptography', EXTRA_TAG, "Single Sign On feature will be disabled", 'cryptography'),
        ('cryptography.hazmat.primitives', 'cryptography', EXTRA_TAG, "Single Sign On feature will be disabled", 'cryptography'),
        ('cryptography.hazmat.primitives.kdf.pbkdf2', 'cryptography', EXTRA_TAG, "Single Sign On feature will be disabled", 'cryptography'),
        ('password_strength', 'password_strength', EXTRA_TAG, "Single Sign On feature will be disabled", VERSION_IN_MODULE),
    )


    installed_modules: dict = {}
    installed_versions: dict = {}

    def __init__(self):
        self.set_installed_modules_and_versions()
        # print(f">>> remove 'pandas', just for test")
        # Dependencies.installed_modules["pandas"] = False
        # print(f">>> remove 'plotly', just for test")
        # Dependencies.installed_modules["plotly"] = False


    @classmethod
    def set_installed_modules_and_versions(cls):
        for item in cls.dependencies:
            module_name = item[0]
            package_name = item[1]
            version_location = item[4]
            cls.get_module(module_name, package_name=package_name, version_location=version_location, dont_throw=True)
        logger().debug(f"installed versions: {cls.installed_versions}")


    @classmethod
    def is_installed(cls, module_name):
        return cls.get_module(module_name, dont_throw=True) is not None


    @classmethod
    def installed_packages(cls)-> dict:
        return {package: cls.installed_versions.get(package) for package in cls.installed_versions}



    @classmethod
    def get_module(cls, module_name, package_name=None, version_location=None, dont_throw=False):
        module = cls.installed_modules.get(module_name)
        if module:
            return module
        elif module == False:
            if dont_throw:
                return None
            raise NotImplementedError(f"due to '{module_name}' module/package not installed")

        try:
            import importlib
            module = importlib.import_module(module_name)
            cls.installed_modules[module_name] = module
            if package_name is not None and cls.installed_versions.get(package_name) is None:
                version = None
                if version_location is not None:
                    try:
                        if version_location == cls.VERSION_IN_MODULE:
                            version_module = module
                        else:
                            version_module = cls.installed_modules.get(version_location)
                            if version_module is None:
                                version_module = importlib.import_module(version_location)
                                cls.installed_modules[version_location] = version_module
                        version = version_module.__version__
                    except:
                        try:
                            import pkg_resources  # part of setuptools
                            version = pkg_resources.require(package_name)[0].version
                        except:
                            pass
                cls.installed_versions[package_name] = version or "?.?.?"

            return module
        except:
            cls.installed_modules[module_name] = False
            if dont_throw:
                return None
            raise NotImplementedError(f"due to '{module_name}' module/package not installed")


    @classmethod
    def warn_missing_dependencies(cls, options={}):
        if not isNullLogger:
            for item in cls.dependencies:
                module_name = item[0]
                if cls.is_installed(module_name):
                    package_name = item[1]
                    tail = f"installed version '{cls.installed_versions.get(package_name)}'"
                else:
                    tail = "NOT installed"
                logger().debug(f"dependency -- '{item}' -- {tail}")

        warnings.filterwarnings(cls.RAISE_WARNINGS, message=cls.MANDATORY_MODULES_REGEX, category=ImportWarning)

        warnings.filterwarnings(cls.SHOW_WARNINGS, message=cls.BASE_MODULES_REGEX, category=ImportWarning)

        if Constants.IS_SAW_INSTALLATION:
            warnings.filterwarnings(cls.IGNORE_WARNINGS, message=cls.OPTIONAL_MODULES_REGEX, category=ImportWarning)
        else:
            warnings.filterwarnings(cls.SHOW_WARNINGS, message=cls.OPTIONAL_MODULES_REGEX, category=ImportWarning)

        warnings.filterwarnings(cls.IGNORE_WARNINGS, message=cls.EXTRA_MODULES_REGEX, category=ImportWarning)

        warnings.filterwarnings(cls.IGNORE_WARNINGS, message=cls.DISABLED_MODULES_REGEX, category=ImportWarning)
        # warnings.simplefilter("always")
        warnings.formatwarning = cls._formatwarning

        not_installed_package_list = []
        not_installed_packages = (options.get("not_installed_packages") or "").strip()
        if len(not_installed_packages) > 0:
            not_installed_package_list = [item.strip() for item in not_installed_packages.split(",")]
        for item in cls.dependencies:
            cls._import_warn(not_installed_package_list, *item)


    @classmethod
    def _import_warn(cls, not_installed_package_list, module_name, package, tag, message, version_location):
        if not cls.installed_modules.get(module_name) and package not in not_installed_package_list:
            warnings.warn_explicit(f"{tag}failed to import '{module_name}' from '{package}', {message}", ImportWarning, '', 0)


    @classmethod
    def _formatwarning(cls, message, category, filename, lineno, line=None):
        global saved_formatwarning
        if category.__name__ == 'ImportWarning' and re.match(cls.ALL_MODULES_REGEX, f'{message}'):
            message = f'{message}'[3:]
            return f"{category.__name__}: {message}\n"
        else:
            return saved_formatwarning(message, category, filename, lineno, line=line)
