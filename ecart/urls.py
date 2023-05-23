from django.contrib import admin
from django.urls import path
from mainApp import views as mainApp
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainApp.homePage),
    path('shop/<str:mc>/<str:sc>/<str:br>/',mainApp.shopPage),
    path('filter/<str:mc>/<str:sc>/<str:br>/<str:filter>/',mainApp.filterPage),
    path('price-filter/<str:mc>/<str:sc>/<str:br>/',mainApp.priceFilterPage),
    path('search/',mainApp.searchPage),
    path('single-product/<int:id>',mainApp.singleProductPage),
    path('add-to-cart/<int:num>/',mainApp.addToCartPage),
    path('cart/',mainApp.cartPage),
    path('update-cart/<str:num>/<str:op>/',mainApp.updateCartPage),
    path('remove-from-cart/<str:num>/',mainApp.removeFromCartPage),
    path('checkout/',mainApp.checkoutPage),
    path('place-order/',mainApp.placeOrderPage),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',mainApp.paymentSuccessPage),
    path('re-payment/<str:checkid>/',mainApp.payAgainPage),
    path('confirmation/',mainApp.confirmationPage),
    path('contact/',mainApp.contactPage),
    path('login/',mainApp.loginPage),
    path('logout/',mainApp.logoutPage),
    path('signup/',mainApp.signupPage),
    path('profile/',mainApp.profilePage),
    path('update-profile/',mainApp.updateProfilePage),
    path('add-to-wishlist/<int:num>/',mainApp.addToWishlist),
    path('remove-from-wishlist/<int:num>/',mainApp.removeFromWishlistPage),
    path('forget-password-1/',mainApp.forgetPasswordPage1),
    path('forget-password-2/',mainApp.forgetPasswordPage2),
    path('forget-password-3/',mainApp.forgetPasswordPage3),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
