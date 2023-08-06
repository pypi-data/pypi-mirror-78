from plone.app.layout.viewlets import ViewletBase
from plone.dexterity.utils import safe_utf8
from plone.event.interfaces import IRecurrenceSupport
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider


class EventDetailsViewlet(ViewletBase):

    def events(self):
        return IRecurrenceSupport(self.context).occurrences()

    def formatted_date(self, occurance):
        provider = getMultiAdapter((self.context, self.request, self.view),
                                   IContentProvider, name=u'formatted_date')
        return provider(occurance)

    def google_maps_link(self):
        query = safe_utf8(self.context.location.replace(" ", "+"))
        return 'https://www.google.com/maps/search/?api=1&query={}'.format(query)
