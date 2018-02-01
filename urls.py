





            # MAGENTO URLS






from django.conf.urls import url
from django.contrib.auth import views
from .views import *

urlpatterns = [
	url(r'^vendor_register$', VendorRegister.as_view(), name="pre_vend_register"),
	url(r'^vendor_login$', VendorLogin.as_view(), name="pre_vend_login"),
	url(r'^vendor_forget-password$', VendorForgetPassword.as_view(), name="pre_vend_forget_password"),
	url(r'^vendor_dashboard$',VendorDashboard.as_view(),name="pre_vend_dashboard"),
	# url(r'^vendor-logout/$',views.logout, {'next_page': '/magento/vendor_login'}),
	# url(r'^vendor-add-products$',AddVendorProduct.as_view(),name="mag_ven_add_product"),
	# url(r'^vendor-remove-products$',VendorRemoveProduct.as_view(),name="mag_ven_remove_product"),
]
