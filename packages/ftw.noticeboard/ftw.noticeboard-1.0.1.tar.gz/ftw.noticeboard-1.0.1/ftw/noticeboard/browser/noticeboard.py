from DateTime import DateTime
from ftw.noticeboard import _
from plone import api
from zope.i18n import translate
from zope.publisher.browser import BrowserView


class NoticeBoardView(BrowserView):

    def __call__(self):
        user_roles = api.user.get_roles(obj=self.context)
        if not {'Manager', 'Site Administrator'} & set(user_roles):
            self.request.set('disable_border', True)
        return super(NoticeBoardView, self).__call__()

    def get_title(self):
        return self.context.Title()

    @property
    def name(self):
        return self.__name__

    def _get_base_query(self):
        now = DateTime()
        return {
            'portal_type': 'ftw.noticeboard.Notice',
            'effective': {'query': now, 'range': 'max'},
            'expires': {'query': now, 'range': 'min'}
        }

    def get_categories(self):
        return self.context.listFolderContents()  # not a catalog query

    def get_categories_and_notices(self):
        """
        Return a prepopulated structure for easy rendering in the template.
        This method could be implented with just one catalog query.
        But as off now there are propbably just a few 100 Notices per installation.
        So caching and improved querying is not necessary right now.
        """
        catalog = api.portal.get_tool('portal_catalog')
        results = []

        for category in self.get_categories():
            query = self._get_base_query()
            query['path'] = '/'.join(category.getPhysicalPath())
            notices = catalog(**query)
            results.append(
                {
                    'title': category.Title,
                    'id': category.id,
                    'url': category.absolute_url(),
                    'amount': len(notices),
                    'addview': '{0}/++add++ftw.noticeboard.Notice'.format(category.absolute_url()),
                    'canadd': api.user.has_permission('ftw.noticeboard: Add Notice', obj=category),
                    'notices': [
                        {
                            'title': notice.Title,
                            'url': notice.getURL(),
                            'expires': api.portal.get_localized_time(notice.expires)
                        } for notice in notices
                    ]
                }
            )
        return results


class MyNoticesView(NoticeBoardView):

    def get_title(self):
        return translate(_(u'label_my_notices', default=u'My Notices'), context=self.request)

    def _get_base_query(self):
        query = {
                'portal_type': 'ftw.noticeboard.Notice',
                'show_inactive': True,
                'Creator': api.user.get_current().getId()
            }
        return query
