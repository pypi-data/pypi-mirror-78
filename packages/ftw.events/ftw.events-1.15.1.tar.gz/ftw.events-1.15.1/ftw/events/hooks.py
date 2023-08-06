from Products.CMFCore.utils import getToolByName


def default_profile_installed(portal):
    reindex_indexes(portal)


def reindex_indexes(portal):
    """
    `plone.app.events` replaces the start and end index by a
    RecurringDateIndex (before DateIndex) but it omits to reindex
    the new index. This causes the loss of the start and end index
    data of every content. So we need to take care of reindexing
    the indexes.
    """
    catalog = getToolByName(portal, 'portal_catalog')

    # Only reindex start/end if the index is empty
    if not len(catalog.Indexes['start']):
        catalog.reindexIndex('start', None)

    if not len(catalog.Indexes['end']):
        catalog.reindexIndex('end', None)
