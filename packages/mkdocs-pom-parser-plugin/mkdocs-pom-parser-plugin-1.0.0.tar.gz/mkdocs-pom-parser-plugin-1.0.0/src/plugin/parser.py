import xml.etree.ElementTree as ET

import re

namespaces = {
    '': 'http://maven.apache.org/POM/4.0.0',
}


class PomParser:
    """
    This class is simply a wrapper around ElementTree
    """

    def __init__(self, arg: str):
        result = re.search("([\n+])", arg)

        # arg is the xml string. (easier testing)
        if result is not None:
            self.tree = ET.fromstring(arg)

        # arg is file
        else:
            self.tree = ET.parse(arg)

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

    def findByXpath(self, xpath: str):
        return self.tree.find(xpath, namespaces)

    def findTextByXpath(self, xpath: str):
        element = self.tree.find(xpath, namespaces)
        return element.text if element is not None else None
