from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q

from fperms import get_perm_model

from fperms_iscore import enums

from is_core.auth.permissions import IsAuthenticated


Perm = get_perm_model()


permissions = {}


GENERAL_CACHE_NAME = '__all__'


class FPermPermission(IsAuthenticated):

    def __init__(self, name, verbose_name=None, register=True):
        """
        :param name: name of the permission stored as codename in `Perm` model
        :param verbose_name: verbose name of the permission
        """
        self.name = name
        self.verbose_name = verbose_name
        if register:
            self._register()

    def _register(self):
        if self.name in permissions:
            raise ImproperlyConfigured('Duplicite permission with name {}'.format(self.name))
        permissions[self.name] = self

    def _get_cache(self, request):
        request._permissions_cache = getattr(request, '_permissions_cache', {})
        return request._permissions_cache

    def _add_to_cache(self, request, key, has_perm):
        self._get_cache(request).setdefault(self.name, {})[key] = has_perm

    def _get_perm(self, obj=None):
        """
        Return permission according to permission name and object ID (if permission is related to some object)
        if permission is not found the None value is returned.
        :param obj: model instance of the Core
        :return: `Perm` object or None
        """
        perms = Perm.objects.filter(
            Q(
                type=enums.PERM_TYPE_CORE,
                codename=self.name,
            ),
            Q(
                Q(object_id=obj.pk if obj else None) |
                Q(object_id=None)
            )
        )
        return perms.order_by('-object_id').first()

    def has_permission(self, name, request, view, obj=None):
        """
        Return `True` if user has set permission of is superuser
        """
        cache = self._get_cache(request).get(self.name, {})
        if not super().has_permission(name, request, view, obj):
            return False
        elif obj is None:
            has_general_perm = cache.get(GENERAL_CACHE_NAME)
            if has_general_perm is None:
                has_general_perm = request.user.perms.has_perm(self._get_perm())
                self._add_to_cache(request, GENERAL_CACHE_NAME, has_general_perm)
            return has_general_perm
        else:
            has_general_perm = cache.get(GENERAL_CACHE_NAME)
            if has_general_perm:
                return has_general_perm

            has_obj_perm = cache.get(str(obj.pk))
            if has_obj_perm is None:
                perm = self._get_perm(obj=obj)
                has_obj_perm = request.user.perms.has_perm(perm)
                self._add_to_cache(request, str(obj.pk), has_obj_perm)
                if perm and not perm.object_id:
                    # Object perm is same as general perm
                    self._add_to_cache(request, GENERAL_CACHE_NAME, has_obj_perm)
            return has_obj_perm
