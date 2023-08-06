from django.conf.urls import include, url
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from wagtailvideos import urls
from wagtailvideos.forms import GroupVideoPermissionFormSet


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^videos/', include(urls)),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
        <script>
            window.chooserUrls.videoChooser = '{0}';
        </script>
        """,
        reverse('wagtailvideos:chooser')
    )


@hooks.register('register_group_permission_panel')
def register_video_permissions_panel():
    return GroupVideoPermissionFormSet


@hooks.register('register_admin_menu_item')
def register_images_menu_item():
    return MenuItem(
        _('Videos'), reverse('wagtailvideos:index'),
        name='videos', classnames='icon icon-media', order=300
    )
