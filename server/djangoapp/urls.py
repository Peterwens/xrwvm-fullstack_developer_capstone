from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
      path('register', views.registration, name='register'),
    
    # Path for login
    path('login', views.login_user, name='login'),

    # Path for logout
    path('logout', views.logout_request, name='logout'),

    # Placeholder for dealer reviews view (uncomment and implement the view logic)
    # path('dealer-reviews/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),

    # Placeholder for adding a review view (uncomment and implement the view logic)
    # path('add-review', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
