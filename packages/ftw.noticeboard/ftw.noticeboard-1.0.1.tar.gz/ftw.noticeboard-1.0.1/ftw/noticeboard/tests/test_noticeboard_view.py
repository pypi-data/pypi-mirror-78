from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from plone.app.textfield.value import RichTextValue


class TestNoticeBoardView(FunctionalTestCase):

    def setUp(self):
        super(TestNoticeBoardView, self).setUp()
        self.grant('Manager')

    def _create_content(self):
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
                           price='100')
                   .within(category1))

        for number in range(1, 2):
            create(Builder('notice')
                   .titled(u'Notice {0}'.format(str(number)))
                   .having(accept_conditions=True,
                           text=RichTextValue('Something'),
                           price='100')
                   .within(category2))

        return noticeboard, category1, category2

    @browsing
    def test_view(self, browser):
        noticeboard, cat1, cat2 = self._create_content()
        browser.login().visit(noticeboard)

        self.assertListEqual(
            ['Category 1 (3)', 'Category 2 (1)'],
            browser.css('.template-noticeboard_view .collapsible-head').text,
            'Expected two categories'
        )

        self.assertEquals(
            3,
            len(browser.css('.collapsible-content').first.css('h3')),
            'Expect 3 notices in first category'
        )

        self.assertEquals(
            1,
            len(browser.css('.collapsible-content')[1].css('h3')),
            'Expect 1 notice in second category'
        )

    @browsing
    def test_link_to_notice(self, browser):
        noticeboard, cat1, cat2 = self._create_content()
        notice = cat1.objectValues()[0]

        browser.login().visit(noticeboard)
        # Click on first link in first category
        browser.css('.collapsible-content').first.css('h3 a').first.click()
        self.assertEqual(notice.absolute_url(), browser.url)

    @browsing
    def test_category_view(self, browser):
        noticeboard, cat1, cat2 = self._create_content()
        browser.login().visit(cat1)

        self.assertEqual(
            1,
            len(browser.css('.collapsible-content')),
            'Expect 1 content area')

        self.assertEquals(
            3,
            len(browser.css('.collapsible-content').css('h3')),
            'Expect 3 notices in first category'
        )

        browser.login().visit(cat2)

        self.assertEquals(
            1,
            len(browser.css('.collapsible-content').css('h3')),
            'Expect 1 notice in second category'
        )
