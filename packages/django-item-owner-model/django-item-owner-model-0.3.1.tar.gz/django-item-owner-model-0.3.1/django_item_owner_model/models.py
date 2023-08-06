from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django_middleware_global_request.middleware import get_request



class DjangoItemOwnerManager(models.Manager):

    def get_queryset(self):
        request = get_request()
        app_label = self.model._meta.app_label
        django_item_owner_model_permit_all = "{}.django_item_owner_model_permit_all".format(app_label)
        django_item_share_model_permit_all = "{}.django_item_share_model_permit_all".format(app_label)
        queryset = super().get_queryset()
        if request.user.has_perm(django_item_owner_model_permit_all) or request.user.has_perm(django_item_share_model_permit_all):
            return queryset
        else:
            filter_expr = Q(pk=0)
            if issubclass(self.model, DjangoItemOwnerModel):
                filter_expr = filter_expr | Q(**{
                    self.model.owner_field_name: request.user,
                })
            if issubclass(self.model, DjangoItemShareModel):
                filter_expr = filter_expr | Q(**{
                    self.model.share_users_field_name: request.user
                })
            queryset = queryset.filter(filter_expr)
            return queryset

class DjangoItemOwnerModel(models.Model):

    owner_field_name = "owner"
    objects = DjangoItemOwnerManager()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="+", verbose_name=_("Owner"))

    class Meta:
        abstract = True
        permissions = [
            ("django_item_owner_model_permit_all", _("Permit To See All Data")),
        ]

    def save(self, *args, **kwargs):
        if not hasattr(self, self.owner_field_name) or not getattr(self, self.owner_field_name):
            request = get_request()
            if request.user and request.user.pk:
                setattr(self, self.owner_field_name, request.user)
        super().save(*args, **kwargs)

class DjangoItemShareModel(models.Model):

    share_users_field_name = "share_users"
    objects = DjangoItemOwnerManager()
    share_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="+", verbose_name=_("Share Users"))

    class Meta:
        abstract = True
        permissions = [
            ("django_item_share_model_permit_all", _("Permit To See All Data")),
        ]
