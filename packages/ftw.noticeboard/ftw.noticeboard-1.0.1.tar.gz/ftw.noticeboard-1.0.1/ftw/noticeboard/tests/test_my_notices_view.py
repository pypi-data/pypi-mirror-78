from datetime import datetime
from datetime import timedelta
from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.textfield.value import RichTextValue


class TestMyNoticeBoardView(FunctionalTestCase):

    def setUp(self):
        super(TestMyNoticeBoardView, self).setUp()
        self.grant('Manager')

    def _create_content(self):
        user = create(Builder('user'))
        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))
        category1 = create(Builder('noticecategory')
                           .having(conditions=RichTextValue('Something'))
                           .titled(u'Category 1')
                           .within(noticeboard))
        category2 = create(Builder('noticecategory')
                           .having(conditions=RichTextValue('Something'))
                           .titled(u'Category 2')
                           .within(noticeboard))

        for number in range(1, 4):
            create(Builder('notice')
                   .titled(u'Notice {0}'.format(str(number)))
                   .having(accept_conditions=True,
                           text=RichTextValue('Something'),
                           price='100',
                           expires=datetime.now() - timedelta(days=10))
                   .within(category1))

        login(self.portal, user.getId())
        for number in range(1, 2):
            create(Builder('notice')
                   .titled(u'Notice {0}'.format(str(number)))
                   .having(accept_conditions=True,
                           text=RichTextValue('Something'),
                           price='100',
                           expires=datetime.now() - timedelta(days=10))
                   .within(category2))
        logout()

        return noticeboard, user

    @browsing
    def test_show_only_my_notices_and_inactive_notices(self, browser):
        board, user = self._create_content()

        browser.login(user).visit(board)
        self.assertFalse(
            len(browser.css('.collapsible-content h3')),
            'Expect no notices, since all of them are expired'
        )

        browser.login(user).visit(board, view='my-notices')
        self.assertEqual(
            1,
            len(browser.css('.collapsible-content h3')),
            'Expect one notices, since the logged in user is owner of 1 Notice'
        )
