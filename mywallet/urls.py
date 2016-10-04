from django.conf.urls import url, include

from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'wallets', views.WalletList.as_view())

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.IndexView.as_view(), name="mywallet"),
    url(r'^logout/', views.LogoutView.as_view(), name="log out"),
    url(r'^addwallet/', views.NewWallet.as_view(), name="add wallet"),
    url(r'^add-new-currency/', views.NewCurrency.as_view(), name='add new currency'),
    url(r'^add-new-operation/', views.NewOperation.as_view(), name='add new operation'),
    url(r'^get-codes-by-wallet-title/', views.GetCodes.as_view(), name="return code by wallet title"),
    url(r'^get-wallets-titles/', views.GetWalletTitles.as_view(), name="get wallets-titles"),
    # url(r'^wallets/', views.GetWallets.as_view(), name="get all wallets"),
    url(r'^edit-wallet-title/', views.EditWalletTitle.as_view(), name="Editing wallet title"),

    url(r'^wallets/', views.WalletList.as_view(), name="wallet-list"),
    # url(r'^api/', include(router.urls)),
    # url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]