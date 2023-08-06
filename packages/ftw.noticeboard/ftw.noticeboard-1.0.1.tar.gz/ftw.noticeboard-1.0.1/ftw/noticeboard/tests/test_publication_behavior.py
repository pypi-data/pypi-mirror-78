from datetime import datetime
from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testing import freeze
from plone.app.textfield.value import RichTextValue


class TestBehaviors(FunctionalTestCase):

    def setUp(self):
        super(TestBehaviors, self).setUp()
        self.grant('Manager')

        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))
        self.category = create(Builder('noticecategory')
                               .having(conditions=RichTextValue('Something'))
                               .titled(u'Category')
                               .within(noticeboard))

    @browsing
    def test_default_values_of_effective_and_expiration_date(self, browser):
        browser.login().visit(self.category)

        with freeze(datetime(2014, 5, 7, 12, 30)):
            factoriesmenu.add('Notice')
            browser.fill(
                {
                    'Title': u'This is a Notice',
                    'Price': '100',
                    'Terms and Conditions': True,
                    'E-Mail': u'hans@peter.example',
                    'Text': u'Anything',
                }
            )

            browser.find_button_by_label('Save').click()

            context = browser.context
            self.assertEquals(DateTime(), context.effective())
            self.assertEquals(DateTime('2014/06/06 12:30:00'), context.expires())
