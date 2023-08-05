import copy
import logging
import sys
from pathlib import Path
from typing import Dict

import mkdocs
from jinja2 import Template
from mkdocs.config import Config
from mkdocs.plugins import BasePlugin

from mkdocs_pom_parser_plugin.parser import PomParser

if sys.version_info[0] >= 3:
    str_type = str
else:
    str_type = mkdocs.utils.string_types

log = logging.getLogger("PomParserPlugin")


# flake8: noqa
class PomParserPlugin(BasePlugin):
    """
    Inject parsed pom values as template variables into the markdown
    """

    config_scheme = (
        ("path", mkdocs.config.config_options.Type(str_type, default="../pom.xml")),
        ("additional", mkdocs.config.config_options.Type(Dict, default=None)),
        ("debug", mkdocs.config.config_options.Type(bool, default=False))
    )

    DEFAULT_ENV_VARS = {
        "POM_MODEL_VERSION": "./modelVersion",
        "POM_GROUP_ID": "./groupId",
        "POM_ARTIFACT_ID": "./artifactId",
        "POM_PACKAGING": "./packaging",
        "POM_VERSION": "./version",
        "POM_NAME": "./name",
        "POM_DESCRIPTION": "./description",
        "POM_URL": "./url"
    }

    def on_config(self, config: Config):
        env_vars = {}
        for name, plugin in config.get('plugins').items():
            if name == 'mkdocs-pom-parser-plugin':
                plugin_config = plugin.__getattribute__("config")

                if plugin_config.get("debug"):
                    log.setLevel(logging.DEBUG)
                else:
                    log.setLevel(logging.INFO)

                path = plugin_config.get('path')
                if path is not None:
                    log.debug("Configured pom file: %s", path)
                    path = Path(path).resolve().__str__()
                    log.info("Resolved pom file: %s", path)

                    additional = plugin_config.get('additional', {})
                    env_vars = copy.copy(self.DEFAULT_ENV_VARS)

                    if additional is not None:
                        log.debug("Additional pom variables detected: %s", additional)
                        for key, value in additional.items():
                            env_vars["POM_" + key.upper()] = value

                    parser = PomParser(path)
                    for key, xpath in env_vars.items():
                        value = parser.findTextByXpath(xpath)
                        env_vars[key] = value

        config.update({"pom_env_vars": env_vars})
        if env_vars.__sizeof__() > 0:
            log.info("Exposed pom values as environment variables")

        log.debug("on_config[POM_ENV_VARS: %s]", config.get("pom_env_vars"))

        return config

    def on_page_markdown(self, markdown, page, config, files):
        log.debug("on_page_markdown[POM_ENV_VARS: %s]", config.get("pom_env_vars"))
        md_template = Template(markdown)
        return md_template.render(copy.copy(config.get("pom_env_vars")))
