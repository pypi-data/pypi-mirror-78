from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from ftw.noticeboard.content.category import INoticeCategory
from ftw.noticeboard.content.notice import INotice


class TermsAndConditions(BrowserView):

    template = ViewPageTemplateFile('templates/conditions.pt')

    def __call__(self):
        self.category = None
        if INoticeCategory.providedBy(self.context):
            self.category = self.context
        elif INotice.providedBy(self.context):
            self.category = self.context.aq_parent
        return self.template()
