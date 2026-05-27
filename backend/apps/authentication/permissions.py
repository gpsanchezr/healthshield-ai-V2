from rest_framework.permissions import BasePermission

class EsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'administrador'

class EsMedico(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol in ['medico', 'administrador']

class EsAnalista(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol in ['analista', 'administrador']
