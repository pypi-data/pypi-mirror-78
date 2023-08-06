from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages
from ftw.testbrowser.pages import plone
from plone.app.textfield.value import RichTextValue
from plone.app.testing import login


class TestContentTypes(FunctionalTestCase):

    def setUp(self):
        super(TestContentTypes, self).setUp()
        self.grant('Manager')

    def _create_content(self):
        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))
        category = create(Builder('noticecategory')
                          .having(conditions=RichTextValue('Something'))
                          .titled(u'Category')
                          .within(noticeboard))
        return noticeboard, category

    @browsing
    def test_add_noticeboard(self, browser):
        browser.login().visit()
        factoriesmenu.add('NoticeBoard')
        browser.fill({'Title': u'This is our NoticeBoard'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is our NoticeBoard', plone.first_heading())

    @browsing
    def test_add_noticecategory(self, browser):
        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))

        browser.login().visit(noticeboard)
        factoriesmenu.add('NoticeCategory')
        browser.fill({'Title': u'This is a Category', 'Terms and Conditions': 'Anything'})
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'This is a Category', plone.first_heading())

    @browsing
    def test_add_notice(self, browser):
        board, category = self._create_content()
        browser.login().visit(category)
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
        self.assertEquals(u'This is a Notice (Edit)', plone.first_heading())

    @browsing
    def test_notice_default_value_email_field(self, browser):
        board, category = self._create_content()
        user = create(Builder('user').with_roles('Site Administrator'))
        login(self.portal, user.getId())

        notice = create(Builder('notice')
                        .titled(u'This is a Notice')
                        .having(accept_conditions=True,
                                text=RichTextValue('Something'),
                                price='100')
                        .within(category))
        self.assertTrue(user.getProperty('email'))
        self.assertEqual(user.getProperty('email'), notice.email)

    @browsing
    def test_terms_and_conditions_need_to_be_accepted(self, browser):
        board, category = self._create_content()
        browser.login().visit(category)
        factoriesmenu.add('Notice')
        browser.fill(
            {
                'Title': u'This is a Notice',
                'E-Mail': u'hans@peter.example',
                'Price': '100',
                'Text': u'Anything',
            }
        )
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'Add Notice', plone.first_heading())
        statusmessages.assert_message('There were some errors.')
        self.assertEqual(
            u'You need to accept the terms and conditions',
            browser.css('.fieldErrorBox > .error').first.text
        )
