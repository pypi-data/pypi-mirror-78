from ftw.datepicker.widget import DateTimePickerWidgetFactory
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides
import datetime


def start_date():
    return datetime.datetime.today()


def end_date():
    return datetime.datetime.today() + datetime.timedelta(30)


class INoticePublication(model.Schema):

    directives.widget(effective=DateTimePickerWidgetFactory)
    effective = schema.Datetime(
        title=_PMF(u'label_effective_date', u'Publishing Date'),
        description=_PMF(
            u'help_effective_date',
            default=u"If this date is in the future, the content will "
                    u"not show up in listings and searches until this date."),
        required=True,
        defaultFactory=start_date
    )

    directives.widget(expires=DateTimePickerWidgetFactory)
    expires = schema.Datetime(
        title=_PMF(u'label_expiration_date', u'Expiration Date'),
        description=_PMF(
            u'help_expiration_date',
            default=u"When this date is reached, the content will no"
                    u"longer be visible in listings and searches."),
        required=True,
        defaultFactory=end_date
    )


class NoticePublication(MetadataBase):
    effective = DCFieldProperty(
        INoticePublication['effective'],
        get_name='effective_date'
    )
    expires = DCFieldProperty(
        INoticePublication['expires'],
        get_name='expiration_date'
    )


alsoProvides(INoticePublication, IFormFieldProvider)
