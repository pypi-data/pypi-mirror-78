from ftw.events.testing import FUNCTIONAL_TESTING
from ftw.events.testing import FUNCTIONAL_ZSERVER_TESTING
from lxml import etree
from ftw.referencewidget.tests.widgets import ReferenceBrowserWidget
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from StringIO import StringIO
from unittest import TestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()


class RealFuncitionalTestCase(FunctionalTestCase):
    layer = FUNCTIONAL_ZSERVER_TESTING


class XMLDiffTestCase(TestCase):

    def _canonicalize_xml(self, text, node_sorter=None):
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            xml = etree.fromstring(text, parser)
        except etree.XMLSyntaxError, exc:
            print '-' * 10
            print exc.error_log
            print '-' * 10
            print text
            print '-' * 10
            raise

        norm = StringIO()
        if node_sorter:
            # Search for parent elements
            for parent in xml.xpath('//*[./*]'):
                parent[:] = sorted(parent, node_sorter)

        xml.getroottree().write_c14n(norm)
        xml = etree.fromstring(norm.getvalue())
        return etree.tostring(xml.getroottree(),
                              pretty_print=True,
                              xml_declaration=True,
                              encoding='utf-8')

    def assert_xml(self, xml1, xml2):
        norm1 = self._canonicalize_xml(xml1)
        norm2 = self._canonicalize_xml(xml2)
        self.maxDiff = None
        self.assertMultiLineEqual(norm1, norm2)
