# django-item-owner-model

Data item has owner and can be shared to other users. Login user can only see owned or shared data items. User with permit_all permission can see all data items.

## Install

```bash
pip install django-item-owner-model
```

## Installed utils

- django_item_owner_model.models.DjangoItemManager
- django_item_owner_model.models.DjangoItemOwnerModel
    - extra permissions: `("django_item_owner_model_permit_all", _("Permit All")),`
- django_item_owner_model.models.DjangoItemShareModel
    - extra permissions: `("django_item_share_model_permit_all", _("Permit All")),`

**Note:**

- DjangoItemOwnerModel and DjangoItemShareModel use the same custom manager: DjangoItemManager.

## Usage

**pro/settings.py**

```python

INSTALLED_APPS = [
    ....
    "django_middleware_global_request",
    "django_item_owner_model",
    ...
]

MIDDLEWARE = [
    ...
    "django_middleware_global_request.middleware.GlobalRequestMiddleware",
    ...
]
```

- We requires `request` instance in Model's Manager, so we have to use django_middleware_global_request to get request instance. See detail about `django_middleware_global_request` at https://pypi.org/project/django-middleware-global-request/.

**app/models.py**

```python
from django.db import models
from django_item_owner_model.models import DjangoAdminItemOwnerModel
from django_item_owner_model.models import DjangoAdminItemShareModel

class Category(DjangoAdminItemOwnerModel, models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

class Book(DjangoAdminItemOwnerModel, DjangoAdminItemShareModel, models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

```

**app/admin.py**


```python
from django.contrib import admin
from django import forms
from .models import Category
from .models import Book

class BookInline(admin.TabularInline):
    model = Book

class CategoryAdmin(admin.ModelAdmin):
    allow_super_user_see_all_items = True
    list_display = ["title"]
    inlines = [
        BookInline,
    ]

class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "share_users_display"]

    def share_users_display(self, obj):
        users = [str(x) for x in obj.share_users.all()]
        return ",".join(users)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)

```

## Bug report

Please report any issues at https://github.com/zencore-cn/zencore-issues.

## Releases

### v0.3.1 2020-09-07

- Doc fix.
- Add i18n.
- Rename django_item_owner_model.models.DjangoItemManager to django_item_owner_model.models.DjangoItemOwnerManager.

### v0.3.0 2020-06-22

- Change app's name from `django-admin-item-owner` to `django-item-owner-model`.
- Use custom model Manager to control item access.
- Note: `New version changes a lot.`

### v0.2.0 2020-01-08

- Add ItemShareMixin for models and admins.

### v0.1.0 2019-12-01

- First release.
