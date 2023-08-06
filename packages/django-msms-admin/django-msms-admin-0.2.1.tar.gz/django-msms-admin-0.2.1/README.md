# pip install django-msms-admin

Intelligent management for multiple subclass models in django's admin site.

## Install

```shell
pip install django-msms-admin
```

## Installed Classes

- DjangoMsmsModelAbstractBase

    The base model must inherit from DjangoMsmsModelAbstractBase class. It provides app_label, model_name, type_name fields and auto save the values.

- DjangoMsmsAdmin

    The base model admin must inherit from DjangoMsmsAdmin class.

- DjangoSubclassAdmin

    All subclass models' admin must inherit from DjangoSubclassAdmin class.

## Configurations

- DjangoMsmsAdmin.subclasses

    The config item is used to provide choices in **select_subclass_model_view**. If NOT provide, the system will auto find all registered subclasses. The structure of subclasses is a three-level-tree. e.g.

    ```python
    subclasses = [{
        "title": "category1",
        "children": [{
            "title": "category11",
            "children: [
                Model1,
                Model2,
                Model3,
            ]
        },{
            "title": "category12",
            "children": [
                Model4,
                Model5,
                Model6,
            ]
        }]
    },{
        "title": "category2",
        "children": [{
            "title": "category21",
            "children": [
                Model7,
                Model8,
            ]
        },{
            "title": "category22,
            "children": [
                Model9,
            ]
        }]
    }]
    ```

- DjangoMsmsModelAbstractBase.cascade_select_description
- DjangoMsmsModelAbstractBase.cascade_select_image

    Config item cascade_select_description and cascade_select_image are use to display more information while you selected a subclass. cascade_select_image is url string of an image.


## Usage

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_simple_tags',
    'django_static_jquery3',
    'django_msms_admin',
    ...
]
```

**app/model.py**

```python
from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django_msms_admin.models import DjangoMsmsModelAbstractBase

class Book(DjangoMsmsModelAbstractBase, models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)

    def __str__(self):
        return self.title

class ComputerBook(Book):
    serial = models.CharField(max_length=64)

    cascade_select_description = "These books are all about computers."
    cascade_select_image = static("app/img/computer-book.jpg")

class NovelBook(Book):
    country = models.CharField(max_length=64)

```

**app/admin.py**

```python
from django.contrib import admin
from django_msms_admin.admin import DjangoMsmsAdmin
from django_msms_admin.admin import DjangoSubclassAdmin

from .models import Book
from .models import ComputerBook
from .models import NovelBook

class BookAdmin(DjangoMsmsAdmin, admin.ModelAdmin):

    list_display = ["title", "author", "type_name"]
    list_filter = ["type_name"]


admin.site.register(Book, BookAdmin)
admin.site.register(ComputerBook, DjangoSubclassAdmin)
admin.site.register(NovelBook, DjangoSubclassAdmin)
```

## Release

### v0.2.1 2020/09/09

- No depends on django-static-jquery3.
- Using media.css & media.js to render css/js links.
- Add LICENSE file.

### v0.2.0 2020/03/07

- Use model's msms_category, msm_priority property to do model category and sorting.
- Rename cascade_select_description to msms_description.
- Rename cascade_select_preview_image to msms_image.

### v0.1.2 2020/03/06

- Fix keywords in setup.py and read requirements.txt for install_requires.

### v0.1.1 2020/03/05

- Add DjangoMsmsModelAbstractBase.get_real_object method.

### v0.1.0 2020/03/03

- First release.
