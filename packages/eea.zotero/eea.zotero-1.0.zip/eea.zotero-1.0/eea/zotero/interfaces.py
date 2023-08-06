"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.zotero import EEAMessageFactory as _


class IEeaZoteroLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IZoteroClientSettings(Interface):
    """ Client settings for Zotero
    """
    server = schema.TextLine(
        title=_(u"Zotero API URL"),
        description=_(u"Zotero API URL including user/group id"),
        default=u"https://api.zotero.org/users/12345"
    )

    password = schema.TextLine(
        title=_(u"Zotero API KEY"),
        description=(u"Zotero API KEY with read/write permissions"),
        default=u""
    )

    style = schema.TextLine(
        title=_(u"Zotero citation style"),
        description=_(
            "Zotero citation style, e.g.: oxford or an URL to a .csl file"),
        default=u"https://www.eea.europa.eu/zotero/eea.csl"
    )
