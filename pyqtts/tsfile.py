from lxml import etree

class tslocation (object):
    def __init__(self, filename=None, line=None):
        self.filename = filename
        self.line = line

    def __str__(self):
        return (self.filename or "None") + "(" + (self.line or "None") + ")"

    def __repr__(self):
        start = "{tslocation("
        end   = ")}"
        tokens = ["filename=" + repr(self.filename),
                "line=" + repr(self.line)]
        return start + ",".join(tokens) + end

    def __eq__(self, other):
        return (self.filename == other.filename and
            self.line == other.line)

    def etree_element(self):
        elem = etree.Element("location")
        if self.filename != None:
            elem.attrib["filename"] = self.filename
        if self.line != None:
            elem.attrib["line"] = self.line
        return elem

    @staticmethod
    def from_etree_element(elem):
        filename = None
        line = None
        if "filename" in elem.attrib:
            filename = elem.attrib["filename"]
        if "line" in elem.attrib:
            line = elem.attrib["line"]
        return tslocation(filename, line)

class tstranslation (object):
    def __init__(self, text, status):
        self.text = text
        self.status = status

    def __str__(self):
        lines = []
        lines.append(self.text or "")
        lines.append("status: " + str(self.status))
        return " ".join(lines)

    def __repr__(self):
        start = "{tstranslation("
        end   = ")}"
        tokens = ["text="+repr(self.text),
        "status="+repr(self.status)]
        return start + ",".join(tokens) + end

    def __eq__(self, other):
        return (self.text == other.text and
            self.status == other.status)

    def etree_element(self):
        elem = etree.Element("translation")
        elem.text = self.text
        if self.statut:
            elem.attrib["type"] = self.statut
        return elem

    @staticmethod
    def from_etree_element(elem):
        text = ""
        for child in elem:
            if child.tag == "numerusform":
                text = child.text
            break
        else:
            text = elem.text
        status = ""
        if "type" in elem.attrib:
            status = elem.attrib["type"]
        return tstranslation(text, status)


class tsmessage (object):
    def __init__(self, locations=None, source=None, translation=None, comment=None):
        self.locations = locations or []
        self.source = source
        self.translation = translation
        self.comment = comment

    def __str__(self):
        lines = []
        lines.append("Locations:")
        for location in self.locations:
            lines.append(str(location))
        else:
            lines.append("empty")
        lines.append("Source: " + (self.source or "empty"))
        lines.append(str(self.translation))
        lines.append("Comment: " + (self.comment or "empty"))
        return "\n".join(lines)

    def __repr__(self):
        start = "{tsmessage("
        end   = ")}"
        tokens = ["location="+repr(self.locations),
        "source="+repr(self.source),
        "translation="+repr(self.translation),
        "comment="+repr(self.comment)]
        return start + ",".join(tokens) + end

    def __eq__(self, other):
        return (self.locations == other.locations and
            self.source == other.source and
            self.translation == other.translation and
            self.comment == other.comment)

    def etree_element(self):
        elem = etree.Element("message")
        for loc in self.locations:
            elem.append(loc.etree_element())
        src = etree.Element("source")
        src.text = self.source
        elem.append(src)
        elem.append(self.translation.etree_element())
        if self.comment != None:
            comm = etree.Element("comment")
            comm.text = self.comment
            elem.append(comm)
        return elem

    @staticmethod
    def from_etree_element(elem):
        locations = []
        source = None
        translation = None
        comment = None
        for child in elem:
            if child.tag == "location":
                locations.append(tslocation.from_etree_element(child))
            elif child.tag == "source":
                source = child.text
            elif child.tag == "translation":
                translation = tstranslation.from_etree_element(child)
            elif child.tag == "comment":
                comment = child.text
        return tsmessage(locations, source, translation, comment)




class tscontext (object):
    def __init__(self, name, messages = None):
        self.name = name
        self.message_list = messages or []

    def __str__(self):
        lines = []
        lines.append(self.name)
        for message in self.message_list:
            lines.append(str(message))
        return "\n".join(lines)

    def __repr__(self):
        start = "{tscontext("
        end   = ")}"
        tokens = ["name="+repr(self.name),
                "messages="+repr(self.message_list)]
        return start + ",".join(tokens) + end

    def __eq__(self, other):
        return (self.name == other.name and
            self.message_list == other.message_list)

    def etree_element(self):
        elem = etree.Element("context")
        name = etree.Element("name")
        name.text = self.name
        elem.append(name)
        for message in self.message_list:
            elem.append(message.etree_element())
        return elem

    @staticmethod
    def from_etree_element(elem):
        name = None
        message_list = []
        for child in elem:
            if child.tag == "name":
                name = child.text
            elif child.tag == "message":
                message_list.append(tsmessage.from_etree_element(child))
        return tscontext(name, message_list)


class tsfile (object):
    def __init__(self, version=None, language=None, context_list=None):
        self.version = version or ""
        self.language = language or ""
        self.context_list = context_list or []

    def __str__(self):
        lines = []
        lines.append("TsFile(" + str(self.version) + " " + str(self.language) + ")")
        for context in self.context_list:
            lines.append(str(context))
        return "\n".join(lines)

    def __repr__(self):
        start = "{tsfile("
        end   = ")}"
        tokens = ["version="+repr(self.version),
                "language="+repr(self.language),
                "context_list="+repr(self.context_list)]
        return start + ",".join(tokens) + end

    def __eq__(self, other):
        return (self.version == other.version and
            self.language == other.language and
            self.context_list == other.context_list)

    def load_file(self, path):
        doc = etree.parse(path)
        root = doc.getroot()
        self.version = root.attrib["version"]
        self.language = root.attrib["language"]
        for context in root :
            self.context_list.append(tscontext.from_etree_element(context))

    def save_file(self, path):
        ts = etree.Element("TS")
        ts.attrib["version"] = self.version
        ts.attrib["language"] = self.language
        for context in self.context_list:
            ts.append(context.etree_element())
        doc = etree.ElementTree(ts)
        s = etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="utf-8", doctype="<!DOCTYPE TS>")
        with open(path, "wb") as f:
            f.write(s)


if __name__ == "__main__":
    import tsfile_test
    tsfile_test.run_tests()

