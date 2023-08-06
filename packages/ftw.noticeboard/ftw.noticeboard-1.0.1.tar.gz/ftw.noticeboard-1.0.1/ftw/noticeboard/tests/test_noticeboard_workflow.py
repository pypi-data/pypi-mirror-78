from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.exceptions import InsufficientPrivileges
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import plone
from plone.app.textfield.value import RichTextValue


class TestNoticeBoardWorkflow(FunctionalTestCase):

    def setUp(self):
        super(TestNoticeBoardWorkflow, self).setUp()
        self.grant('Manager')

    @browsing
    def test_user_can_only_add_and_edit_notices(self, browser):
        user = create(Builder('user'))
        browser.login(user).visit()
        with self.assertRaises(ValueError):
            # ValueError: Cannot add "NoticeBoard": no factories menu visible
            factoriesmenu.add('NoticeBoard')

        noticeboard = create(Builder('noticeboard'))
        browser.visit(noticeboard)

        with self.assertRaises(ValueError):
            # ValueError: Cannot add "NoticeBoard": no factories menu visible
            factoriesmenu.add('NoticeCategory')

        category = create(Builder('noticecategory').within(noticeboard))
        browser.visit(category)
        browser.css('a.add-link').first.click()  # factoriesmenu.add('Notice')

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

        browser.visit('@@edit')
        browser.fill(
            {
                'Title': u'Changed',
            }
        )
        browser.find_button_by_label('Save').click()
        self.assertEquals(u'Changed (Edit)', plone.first_heading())

    @browsing
    def test_user_can_only_add_images_on_notices_he_created(self, browser):
        user = create(Builder('user'))

        noticeboard = create(Builder('noticeboard'))
        category = create(Builder('noticecategory').within(noticeboard))
        othernotice = create(Builder('notice')
                             .titled(u'This is a Notice')
                             .having(accept_conditions=True,
                                     text=RichTextValue('Something'),
                                     price='100')
                             .within(category))

        browser.login(user).visit(othernotice)
        self.assertFalse(factoriesmenu.visible())

        browser.visit(category)
        browser.css('a.add-link').first.click()  # factoriesmenu.add('Notice')

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
        self.assertEqual(
            ['NoticeImage', ],
            factoriesmenu.addable_types())

    @browsing
    def test_user_can_delete_its_notices_but_not_from_others(self, browser):
        user = create(Builder('user'))

        noticeboard = create(Builder('noticeboard'))
        category = create(Builder('noticecategory').within(noticeboard))
        othernotice = create(Builder('notice')
                             .titled(u'This is a Notice')
                             .having(accept_conditions=True,
                                     text=RichTextValue('Something'),
                                     price='100')
                             .within(category))

        with self.assertRaises(InsufficientPrivileges):
            browser.login(user).visit(othernotice, view='delete_confirmation')
            browser.find_button_by_label('Delete').click()

        browser.visit(category)
        browser.css('a.add-link').first.click()  # factoriesmenu.add('Notice')
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
        notice = browser.context

        browser.visit(notice, view='delete_confirmation')
        browser.find_button_by_label('Delete').click()

        self.assertNotIn(notice, category.objectValues())
