# django-admin-global-sidebar

Provide a global left sidebar for django admin site.

## Install

```shell
pip install django-admin-global-sidebar
```

## Usage

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_static_fontawesome',
    'django_static_jquery3',
    'django_admin_global_sidebar',
    ...
]

DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS = [
    {
        "title": "Home",
        "icon": "fa fa-home",
        "url": "/admin/",
    },{
        "title": "Settings",
        "icon": "fa fa-cogs",
        "children": [
            {
                "title": "User",
                "icon": "fas fa-user",
                "model": "auth.user",
                "permissions": ["auth.view_user",],
            },
            {
                "title": "Group",
                "icon": "fas fa-users",
                "model": "auth.group",
                "permissions": ["auth.view_group",],
            }
        ]
    }
]
```

- Add django_static_fontawesome, django_static_jquery3 and django_admin_global_sidebar in INSTALLED_APPS.
- Add sidebar menu settings in DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS.

## DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS

- Two level menu supported.
- Menu item config options:
    - title
    - icon
    - children
    - url
    - model
    - view
    - permissions
    - active_patterns
- `title` is the display title.
- `icon` is fontawesome class.
- `children` is sub-menu list settings.
- `url`, `model` or `view` will be used to calc the menu link. Only one option will be applied.
- `url` means a fixed link.
- `model` means model's changelist view.
- `view` means django's view name and the result link is calced with: revered(`view`).
- `permissions` is the permission array.
    - Using `or` logic for permission elements.
    - A permission element can be a permission-tag or permission-tags.
    - Using `and` logic for permission-tags.
- `active_patterns` used to determine the active status of the menu item.
    - Pattern will be used to test against the request.path.
    - It can be a pattern string or pattern string list.
    - Use `or` logic for patterns.

## Releases

### v0.1.2 2020/09/01

- Depends on django-static-jquery3>=5.0.0.

### v0.1.1 2020/06/20

- Fix popup problem.

### v0.1.0 2020/04/23

- First release.