from django.conf.urls import url
from user_details.views import *

urlpatterns = [
    url(r'^create_account/',CreateAccount.as_view(), name='CreateAccount'),
    url(r'^login/',loginCheck.as_view(), name='loginCheck'),
    url(r'^account_type/',AccountTypeAPI.as_view(), name='AccountTypeAPI'),
    url(r'^account_details/',AccountDetailsAPI.as_view(), name='AccountDetailsAPI'),
]
