import sys

import mkdocs
import logging
from mkdocs.plugins import BasePlugin
from mkdocs.utils import warning_filter

from typing import Dict

from jinja2 import Template, Environment

from plugin.parser import PomParser

log = logging.getLogger(__name__)
log.addFilter(warning_filter)

if sys.version_info[0] >= 3:
    str_type = str
else:
    str_type = mkdocs.utils.string_types


# flake8: noqa
class PomParserPlugin(BasePlugin):
    """
    Inject parsed pom values as template variables into the markdown
    """

    config_scheme = (
        ("path", mkdocs.config.config_options.Type(str_type, default="../pom.xml")),
        ("additional", mkdocs.config.config_options.Type(Dict, default=None))
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

    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
        path = self.config.get('path', None)
        additional = self.config.get('additional', {})
        ENV_VARS = self.DEFAULT_ENV_VARS

        if additional is not None:
            for key, value in additional.items():
                ENV_VARS["POM_" + key] = value

        if path is not None:
            parser = PomParser(path)
            for key, xpath in ENV_VARS.items():
                value = parser.findTextByXpath(xpath)
                ENV_VARS[key] = value

            # print("Parsed " + path + ": ", ENV_VARS)

        md_template = Template(markdown)
        return md_template.render({**ENV_VARS})
