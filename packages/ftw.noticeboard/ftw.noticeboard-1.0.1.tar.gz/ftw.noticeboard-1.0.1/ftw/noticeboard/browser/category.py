from ftw.noticeboard.browser.noticeboard import NoticeBoardView


class NoticeCategoryView(NoticeBoardView):

    def get_categories(self):
        return [self.context]
