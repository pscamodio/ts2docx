from tsfile import *
import unittest
import random
import itertools

locations_data = [("pippo.cpp", "-10"),
    ("pippo.cpp", "+0"),
    ("pippo.cpp", "+10"),
    ("pippo.cpp", None),
    ("pippo.cpp", ""),
    ("", "10"),
    (None, "10"),
    (None, None)]

translations_data = [("Prova", True),
    ("Prova", False),
    ("", True),
    ("", False),
    (None, True),
    (None, False)]

simpletext_data = ["Testo",
    "Testo lungo con spazi",
    "Testo lungo con caratteri speciali\t\t&gt;",
    "",
    None]


class TestLocation(unittest.TestCase):

    def setUp(self):
        self.data = locations_data

    def test_creation(self):
        for data in self.data:
            loc = tslocation(data[0], data[1])
            self.assertEqual(loc.filename, data[0])
            self.assertEqual(loc.line,  data[1])

    def test_xml(self):
        for data in self.data:
            loc = tslocation(data[0], data[1])
            elem = loc.etree_element()
            loc2 = tslocation.from_etree_element(elem)
            self.assertEqual(loc, loc2)

class TestTranslation(unittest.TestCase):

    def setUp(self):
        self.data = translations_data

    def test_creation(self):
        for data in self.data:
            transl = tstranslation(data[0], data[1])
            self.assertEqual(transl.text, data[0])
            self.assertEqual(transl.finished, data[1])

    def test_xml(self):
        for data in self.data:
            transl = tstranslation(data[0], data[1])
            elem = transl.etree_element()
            transl2 = tstranslation.from_etree_element(elem)
            self.assertEqual(transl, transl2)

class TestMessage(unittest.TestCase):

    def setUp(self):
        locations = [tslocation(*data) for data in locations_data]
        translations = [tstranslation(*data) for data in translations_data]
        locations_lists = [None, [], [locations[0]], [locations[0], locations[1]], locations]
        self.data = list(itertools.product(locations_lists, simpletext_data, translations, simpletext_data))

    def test_creation(self):
        for data in self.data:
            mess = tsmessage(data[0], data[1], data[2], data[3])
            self.assertEqual(mess.locations, data[0] or [])
            self.assertEqual(mess.source, data[1])
            self.assertEqual(mess.translation, data[2])
            self.assertEqual(mess.comment, data[3])

    def test_xml(self):
        for data in self.data:
            mess = tsmessage(data[0], data[1], data[2], data[3])
            elem = mess.etree_element()
            mess2 = tsmessage.from_etree_element(elem)
            self.assertEqual(mess, mess2)


class TestContext(unittest.TestCase):

    def setUp(self):
        locations = [tslocation(fname, line) for fname, line in locations_data]
        translations = [tstranslation(text, finish) for text, finish in translations_data]
        locations_lists = [None, [], [locations[0]], [locations[0], locations[1]], locations]
        messages_data = list(itertools.product(locations_lists, simpletext_data, translations, simpletext_data))
        messages = [tsmessage(*data) for data in messages_data]
        messages_lists = [None, [], [messages[0]], [messages[0], messages[1]], messages]
        self.data = list(itertools.product(simpletext_data, messages_lists))

    def test_creation(self):
        for data in self.data:
            context = tscontext(data[0], data[1])
            self.assertEqual(context.name, data[0])
            self.assertEqual(context.message_list, data[1] or [])

    def test_xml(self):
        for data in self.data:
            context = tscontext(data[0], data[1])
            elem = context.etree_element()
            context2 = context.from_etree_element(elem)
            self.assertEqual(context, context2)


def printIfDiff(val1, val2):
    if val1 != val2:
        print("Left: " + val1 + " Right: " + val2)

def testEqual(tsfile1, tsfile2):
    printIfDiff(tsfile1.version, tsfile2.version)
    printIfDiff(tsfile1.language, tsfile2.language)
    for context1, context2 in zip(tsfile1.context_list, tsfile2.context_list):
        printIfDiff(context1.name, context2.name)
        for message1, message2 in zip(context1.message_list, context2.message_list):
            printIfDiff(message1, message2)


class TextTsFile(unittest.TestCase):

    def setUp(self):
        self.path_data = [("qt_zh_tw.ts", "qt_zh_tw2.ts"),
            ("dental_zh_tw.ts", "dental_zh_tw2.ts")]

    def test_read(self):
        for read_path, out_path in self.path_data:
            f = tsfile()
            f.load_file(read_path)
            f.save_file(out_path)
            f2 = tsfile()
            f2.load_file(out_path)
            testEqual(f, f2)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocation)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestTranslation)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestMessage)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(TestContext)
    suite5 = unittest.TestLoader().loadTestsFromTestCase(TextTsFile)
    unittest.TextTestRunner(verbosity=3).run(suite)
    unittest.TextTestRunner(verbosity=3).run(suite2)
    unittest.TextTestRunner(verbosity=3).run(suite3)
    unittest.TextTestRunner(verbosity=3).run(suite4)
    unittest.TextTestRunner(verbosity=3).run(suite5)


if __name__ == "__main__":
    run_tests()