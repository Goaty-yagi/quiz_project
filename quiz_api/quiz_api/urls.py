from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.authtoken')),
    path('api/',include('quiz.urls')),
    path('api/',include('user.urls')),
    path('api/board/',include('board.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns