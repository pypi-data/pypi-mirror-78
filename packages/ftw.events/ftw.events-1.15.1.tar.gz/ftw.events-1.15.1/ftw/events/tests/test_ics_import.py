from ftw.builder import Builder
from ftw.builder import create
from ftw.events.tests import FunctionalTestCase
from plone.app.event.ical.importer import ical_import
import os


class TestICSImport(FunctionalTestCase):

    def test_set_event_location_on_ical_import(self):
        self.grant('Manager')
        folder = create(Builder('event folder').titled(u'Activities'))
        icsfile = open(os.path.join(
            os.path.dirname(__file__),
            'ics_files/single_event.ics'), 'rb')

        ical_import(folder, icsfile.read(), 'ftw.events.EventPage')

        self.assertEqual('London', folder.listFolderContents()[-1].location)
