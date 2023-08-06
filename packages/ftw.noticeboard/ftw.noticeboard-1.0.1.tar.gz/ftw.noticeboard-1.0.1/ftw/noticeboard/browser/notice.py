from plone import api
from zope.publisher.browser import BrowserView


class NoticeView(BrowserView):

    def get_localized_expiration_date(self):
        return api.portal.get_localized_time(self.context.expires())

    def can_edit(self):
        return api.user.has_permission('Modify portal content', obj=self.context)
