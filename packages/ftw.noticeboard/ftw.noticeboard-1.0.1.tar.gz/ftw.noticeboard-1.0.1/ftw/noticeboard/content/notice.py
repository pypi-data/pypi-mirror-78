from ftw.noticeboard import _
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.dexterity.utils import safe_unicode
from plone.supermodel import model
from z3c.form import validator
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from zope.interface import Invalid


class INotice(Interface):
    """Marker interface for the Notice"""


def user_mail():
    if not api.user.is_anonymous():
        email = api.user.get_current().getProperty('email')
        return safe_unicode(email) or u''
    return u''


class INoticeSchema(model.Schema):
    """A Folderish type for notices, which may hold images"""

    price = schema.TextLine(
        title=_(u'label_price', default=u'Price'),
        required=True,
    )

    email = schema.TextLine(
        title=_(u'label_email', default=u'E-Mail'),
        required=True,
        defaultFactory=user_mail,
    )

    text = RichText(
        title=_(u'label_text', default=u'Text'),
        required=True,
        allowed_mime_types=('text/html',)
    )

    directives.order_after(accept_conditions='*')
    accept_conditions = schema.Bool(
        title=_(u'label_accept_conditions', default=u'Terms and Conditions'),
        description=_(u'description_accept_conditions',
                      default=u'Please accept the '
                      '<a target="_blank" href="./terms-and-conditions">terms and conditions</a>'),
        default=False)


class Notice(Container):
    implements(INotice)


alsoProvides(INoticeSchema, IFormFieldProvider)


class AcceptedTermsAndConditions(validator.SimpleFieldValidator):
    """ z3c.form validator class for international phone numbers """

    def validate(self, value):
        if not value:
            raise Invalid(_(u'error_not_accepted',
                            default=u'You need to accept the terms and conditions'))
        return


validator.WidgetValidatorDiscriminators(
    AcceptedTermsAndConditions,
    field=INoticeSchema['accept_conditions']
)
