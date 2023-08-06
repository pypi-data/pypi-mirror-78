from ftw.builder import Builder
from ftw.builder import create
from ftw.noticeboard.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import plone
from plone.app.textfield.value import RichTextValue


class TestNoticeView(FunctionalTestCase):

    def setUp(self):
        super(TestNoticeView, self).setUp()
        self.grant('Manager')

    def _create_content(self):
        noticeboard = create(Builder('noticeboard').titled(u'Noticeboard'))
        category = create(Builder('noticecategory')
                          .having(conditions=RichTextValue('Something'))
                          .titled(u'Category')
                          .within(noticeboard))
        notice = create(Builder('notice')
                        .titled(u'This is a N\xf6tice')
                        .having(accept_conditions=True,
                                text=RichTextValue(u'S\xf6mething'),
                                price='100')
                        .within(category))
        return notice

    @browsing
    def test_list_images(self, browser):
        notice = self._create_content()

        for number in range(4):
            create(Builder('noticeimage').within(notice).with_dummy_content())

        browser.login().visit(notice)
        self.assertEqual(
            4,
            len(browser.css('.notice-image-slider img')),
            'Expect 4 images'
        )

        self.assertEquals(u'This is a N\xf6tice (Edit)', plone.first_heading())
        self.assertEquals(u'S\xf6mething', browser.css('.notice-text').first.text)
