from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

# Pengecekan login
def login_required():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.session.get('kode_superadmin'):
                # Jika pengguna memiliki session id_admin (sudah login)
                return view_func(request, *args, **kwargs)
            else:
                # Jika pengguna tidak memiliki session userid (belum login)
                messages.error(request, "Anda tidak memiliki akses ke halaman ini !")
                return redirect('superadmin_login')
        return wrapper
    return decorator

# Hak akses
def hak_akses(user_level):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.session.get('status_login') == user_level:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Anda tidak memiliki akses ke halaman ini !')
                return redirect('superadmin_login')
        return wrapper
    return decorator