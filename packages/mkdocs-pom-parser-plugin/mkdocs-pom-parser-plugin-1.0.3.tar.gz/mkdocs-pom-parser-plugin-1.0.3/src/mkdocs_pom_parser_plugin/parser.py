import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

namespaces = {'': 'http://maven.apache.org/POM/4.0.0', 'mvn': 'http://maven.apache.org/POM/4.0.0'}


class PomParser:
    """
    This class is simply a wrapper around ElementTree
    """

    oldPython = True

    def __init__(self, fileOrContent: str, **kwargs):
        version = sys.version_info
        if kwargs.get("version_info", None):
            version = kwargs.get("version_info")

        self.oldPython = version < (3, 8)

        path = Path(fileOrContent)
        # arg is the xml string. (easier testing)
        if path.exists() is not True:
            self.tree = ET.fromstring(fileOrContent)

        # arg is file
        else:
            self.tree = ET.parse(fileOrContent)

    def getTree(self):
        return self.tree

    def getModelVersion(self):
        return self.findTextByXpath("./modelVersion")

    def getGroupId(self):
        return self.findTextByXpath("./groupId")

    def getArtifactId(self):
        return self.findTextByXpath("./artifactId")

    def getPackaging(self):
        return self.findTextByXpath("./packaging")

    def getVersion(self):
        return self.findTextByXpath("./version")

    def getName(self):
        return self.findTextByXpath("./name")

    def getDescription(self):
        return self.findTextByXpath("./description")

    def getUrl(self):
        return self.findTextByXpath("./url")

    def findTextByXpath(self, xpath: str):
        element = self.findByXpath(xpath)
        # print(element.text) if element is not None else None
        return element.text if element is not None else None

    def findByXpath(self, xpath: str):
        # Add support for older Python versions - necessary for Netlify since it does not support >= 3.8 at the time of
        # writing this.
        defaultNamespace = "./{" + namespaces.get('') + "}"
        if self.oldPython and xpath.startswith(defaultNamespace) is False and xpath.startswith("./mvn:") is False:
            xpath = re.sub(r"^\./(.+)$", r'./mvn:\1', xpath)

        return self.tree.find(xpath, namespaces)
