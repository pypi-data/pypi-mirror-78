
from django.db import models
from django.utils.translation import ugettext_lazy as _


class IsVisibleField(models.BooleanField):

    def __init__(
            self,
            verbose_name=_('Is visible'),
            default=True,
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            default=default,
            *args, **kwargs)


class IsNewField(models.BooleanField):

    def __init__(
            self,
            verbose_name=_('Is new'),
            default=False,
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            default=default,
            *args, **kwargs)


class NameField(models.CharField):

    def __init__(
            self,
            verbose_name=_('Product name'),
            max_length=255,
            blank=True,
            db_index=True,
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            blank=blank,
            db_index=db_index,
            *args, **kwargs)


class CodeField(models.CharField):

    def __init__(
            self,
            verbose_name=_('Code'),
            max_length=255,
            blank=True,
            db_index=True,
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            blank=blank,
            db_index=db_index,
            *args, **kwargs)


class AdditionalCodesField(models.CharField):

    def __init__(
            self,
            verbose_name=_('Additional codes'),
            max_length=2700,
            blank=True,
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            blank=blank,
            *args, **kwargs)


class PriceField(models.FloatField):

    def __init__(
            self,
            verbose_name=_('Price'),
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            *args, **kwargs)


class OldPriceField(models.FloatField):

    def __init__(
            self,
            verbose_name=_('Old price'),
            blank=True,
            null=True,
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            blank=blank,
            null=null,
            *args, **kwargs)


class DescriptionField(models.TextField):

    def __init__(
            self,
            verbose_name=_('Description'),
            blank=True,
            *args, **kwargs):
        super().__init__(
            verbose_name=verbose_name,
            blank=blank,
            *args, **kwargs)
