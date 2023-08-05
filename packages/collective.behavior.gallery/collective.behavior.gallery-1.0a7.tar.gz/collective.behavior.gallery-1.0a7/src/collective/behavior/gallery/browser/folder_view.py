# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.folder import FolderView


class PicturelessFolderView(FolderView):

    @property
    def friendly_types(self):
        friendly_types = self.portal_state.friendly_types()
        if 'Image' in friendly_types:
            friendly_types.remove('Image')
        return friendly_types
