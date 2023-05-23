from django.shortcuts import render,HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from ecart.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay

from .models import *
def homePage(Request):
    # Request.session.flush()
    products = Product.objects.all().order_by("-id")[0:8]
    brands = Brand.objects.all()
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    data = []
    for item in brands:
        data.append(item.name)
    Request.session['brand']=data
    data = []
    for item in maincategory:
        data.append(item.name)
    Request.session['maincategory']=data
    data = []
    for item in subcategory:
        data.append(item.name)
    Request.session['subcategory']=data
    return render(Request,"index.html",{'products':products,'brands':brands})

def shopPage(Request,mc,sc,br):
    if(mc=="All" and sc=="All" and br=="All"):
        data = Product.objects.all().order_by("-id")
    elif(mc!="All" and sc=="All" and br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("-id")
    elif(mc=="All" and sc!="All" and br=="All"):
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("-id")    
    elif(mc=="All" and sc=="All" and br!="All"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br)).order_by("-id")    
    elif(mc!="All" and sc!="All" and br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")    
    elif(mc!="All" and sc=="All" and br!="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by("-id")
    elif(mc=="All" and sc!="All" and br!="All"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    else:
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    maincategories = Maincategory.objects.all()
    subcategories = Subcategory.objects.all()
    brands = Brand.objects.all()
    return render(Request,"shop.html",{'data':data,'maincategories':maincategories,'subcategories':subcategories,'brands':brands,'mc':mc,'sc':sc,'br':br})

def filterPage(Request,mc,sc,br,filter):
    if(filter=="Latest"):
        if(mc=="All" and sc=="All" and br=="All"):
            data = Product.objects.all().order_by("-id")
        elif(mc!="All" and sc=="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("-id")
        elif(mc=="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("-id")    
        elif(mc=="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br)).order_by("-id")    
        elif(mc!="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")    
        elif(mc!="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by("-id")
        elif(mc=="All" and sc!="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
        else:
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    elif(filter=="LTOH"):
        if(mc=="All" and sc=="All" and br=="All"):
            data = Product.objects.all().order_by("finalprice")
        elif(mc!="All" and sc=="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("finalprice")
        elif(mc=="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("finalprice")    
        elif(mc=="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br)).order_by("finalprice")    
        elif(mc!="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("finalprice")    
        elif(mc!="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by("finalprice")
        elif(mc=="All" and sc!="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("finalprice")
        else:
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("finalprice")
    else:
        if(mc=="All" and sc=="All" and br=="All"):
            data = Product.objects.all().order_by("-finalprice")
        elif(mc!="All" and sc=="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("-finalprice")
        elif(mc=="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("-finalprice")    
        elif(mc=="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br)).order_by("-finalprice")    
        elif(mc!="All" and sc!="All" and br=="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("-finalprice")    
        elif(mc!="All" and sc=="All" and br!="All"):
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by("-finalprice")
        elif(mc=="All" and sc!="All" and br!="All"):
            data = Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("-finalprice")
        else:
            data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("-finalprice")

    maincategories = Maincategory.objects.all()
    subcategories = Subcategory.objects.all()
    brands = Brand.objects.all()

    return render(Request,"shop.html",{'data':data,'maincategories':maincategories,'subcategories':subcategories,'brands':brands,'mc':mc,'sc':sc,'br':br})


def priceFilterPage(Request,mc,sc,br):
    option = Request.POST.get("price")
    if(option=="1"):
        min = 0
        max =1000000
    elif(option=="2"):
        min = 0
        max = 1000
    elif(option=="3"):
        min = 1000
        max = 2000
    elif(option=="4"):
        min = 2000
        max = 3000
    elif(option=="5"):
        min = 3000
        max = 4000
    elif(option=="6"):
        min = 4000
        max = 5000
    elif(option=="7"):
        min = 5000
        max = 1000000
    if(mc=="All" and sc=="All" and br=="All"):
        data = Product.objects.filter(finalprice__gte=min,finalprice__lte=max).order_by("-id")
    elif(mc!="All" and sc=="All" and br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),finalprice__gte=min,finalprice__lte=max).order_by("-id")
    elif(mc=="All" and sc!="All" and br=="All"):
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),finalprice__gte=min,finalprice__lte=max).order_by("-id")    
    elif(mc=="All" and sc=="All" and br!="All"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br),finalprice__gte=min,finalprice__lte=max).order_by("-id")    
    elif(mc!="All" and sc!="All" and br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),finalprice__gte=min,finalprice__lte=max).order_by("-id")    
    elif(mc!="All" and sc=="All" and br!="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),finalprice__gte=min,finalprice__lte=max).order_by("-id")
    elif(mc=="All" and sc!="All" and br!="All"):
        data = Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc),finalprice__gte=min,finalprice__lte=max).order_by("-id")
    else:
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc),finalprice__gte=min,finalprice__lte=max).order_by("-id")
    maincategories = Maincategory.objects.all()
    subcategories = Subcategory.objects.all()
    brands = Brand.objects.all()
    return render(Request,"shop.html",{'data':data,'maincategories':maincategories,'subcategories':subcategories,'brands':brands,'mc':mc,'sc':sc,'br':br})

def searchPage(Request):
    if(Request.method=="POST"):
        search = Request.POST.get("search")
        data = Product.objects.filter(Q(name__contains=search)|Q(color__contains=search)|Q(size__contains=search)|Q(stock__contains=search)|Q(description__contains=search))
        maincategories = Maincategory.objects.all()
        subcategories = Subcategory.objects.all()
        brands = Brand.objects.all()
        return render(Request,"shop.html",{'data':data,'maincategories':maincategories,'subcategories':subcategories,'brands':brands,'mc':'All','sc':"All",'br':'All'})
    else:
        return HttpResponseRedirect("/")

def singleProductPage(Request,id):
    data = Product.objects.get(id=id)
    relatedProducts = Product.objects.filter(maincategory=Maincategory.objects.get(name=data.maincategory))
    return render(Request,"detail.html",{'data':data,'relatedProducts':relatedProducts})

def addToCartPage(Request,num):
    p = Product.objects.get(id=num)
    if(p):
        cart = Request.session.get("cart",None)
        if(cart):
            if(str(num) in cart):
                return HttpResponseRedirect("/cart/")
            else:
                cart.setdefault(str(num),{'id':p.id,'name':p.name,'brand':p.brand.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':1,'total':p.finalprice,'pic':p.pic1.url})
        else:
            cart = {str(num):{'id':p.id,'name':p.name,'brand':p.brand.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':1,'total':p.finalprice,'pic':p.pic1.url}}
        subtotal = 0
        count = 0
        for key,values in cart.items():
            subtotal = subtotal+values['total']
            count = count + values['qty']
        if(subtotal>0 and subtotal<1000):
            shipping = 150
        else:
            shipping =  0
        total = subtotal + shipping
        Request.session['cart']=cart        
        Request.session['subtotal']=subtotal        
        Request.session['shipping']=shipping        
        Request.session['total']=total        
        Request.session['count']=count        
        Request.session.set_expiry(60*60*24*30)
        return HttpResponseRedirect("/cart/")
    else:
        return HttpResponseRedirect("/shop/All/All/All")

def cartPage(Request):
    cart = Request.session.get("cart",None)
    return render(Request,"cart.html",{'cart':cart})

def removeFromCartPage(Request,num):
    cart = Request.session.get("cart",None)
    if(cart and num in cart):
        del cart[num]
        Request.session['cart']=cart
        subtotal = 0
        count = 0
        for key,values in cart.items():
            subtotal = subtotal+values['total']
            count = count + values['qty']
        if(subtotal>0 and subtotal<1000):
            shipping = 150
        else:
            shipping =  0
        total = subtotal + shipping
        Request.session['cart']=cart        
        Request.session['subtotal']=subtotal        
        Request.session['shipping']=shipping        
        Request.session['total']=total        
        Request.session['count']=count
    return HttpResponseRedirect("/cart/")

def updateCartPage(Request,num,op):
    cart = Request.session.get("cart",None)
    if(cart and num in cart):
        item = cart[num]
        if(item['qty']==1 and op=="Dec"):
            return HttpResponseRedirect("/cart/")
        elif(op=="Dec"):
            item['qty'] = item['qty']-1
            item['total'] = item['total']-item['price']
        else:
            item['qty'] = item['qty']+1
            item['total'] = item['total']+item['price']
        Request.session['cart']=cart
        subtotal = 0
        count = 0
        for key,values in cart.items():
            subtotal = subtotal+values['total']
            count = count + values['qty']
        if(subtotal>0 and subtotal<1000):
            shipping = 150
        else:
            shipping =  0
        total = subtotal + shipping
        Request.session['cart']=cart        
        Request.session['subtotal']=subtotal        
        Request.session['shipping']=shipping        
        Request.session['total']=total        
        Request.session['count']=count
        Request.session.set_expiry(60*60*24*30)
    return HttpResponseRedirect("/cart/")

@login_required(login_url="/login/")
def addToWishlist(Request,num):
    try:
        p = Product.objects.get(id=num)
        buyer = Buyer.objects.get(username=Request.user.username)
        try:
            wishlist = Wishlist.objects.get(buyer=buyer,product=p)
        except:
            w = Wishlist()
            w.buyer = buyer
            w.product = p
            w.save()
    except:
        pass
    return HttpResponseRedirect("/profile/")

@login_required(login_url="/login/")
def removeFromWishlistPage(Request,num):
    try:
        item = Wishlist.objects.get(id=num)
        item.delete()
    except:
        pass
    return HttpResponseRedirect("/profile/")

@login_required(login_url="/login/")
def checkoutPage(Request):
    try:
        buyer = Buyer.objects.get(username=Request.user.username)
        return render(Request,"checkout.html",{'buyer':buyer})
    except:
        return HttpResponseRedirect("/cart/")

client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/login/")
def placeOrderPage(Request):
    if(Request.method=="POST"):
        buyer = Buyer.objects.get(username=Request.user.username)
        mode = Request.POST.get("mode")
        subtotal = Request.session.get("subtotal",0)
        shipping = Request.session.get("shipping",0)
        total = Request.session.get("total",0)
        if(subtotal==0):
            return HttpResponseRedirect("/checkout/")

        check = Checkout()
        check.buyer = buyer
        check.subtotal = subtotal
        check.shipping = shipping
        check.final = total
        check.save()

        cart = Request.session.get("cart",None)
        for key,values in cart.items():
            p = Product.objects.get(id=(int(key)))
            cp = CheckoutProducts()
            cp.checkout = check
            cp.product = p
            cp.qty = values['qty']
            cp.total = values['total']
            cp.save()

        Request.session['cart'] = {}
        Request.session['subtotal'] = 0
        Request.session['shipping'] = 0
        Request.session['total'] = 0
        Request.session['count'] = 0


        if(mode=="COD"):
            subject = 'Order Has Been Placed : Team E-Cart'
            message =   """
                        Hello """+buyer.name+"""
                        Your Order Has Been Placed!!!
                        Now Your Track Your Order in Profile Section
                        Team : E-Cart
                        """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [buyer.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect("/confirmation")
        else:
            orderAmount = check.final*100
            orderCurrency = "INR"
            paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
            paymentId = paymentOrder['id']
            check.paymentMode=2
            check.save()
            return render(Request,"pay.html",{
                "amount":orderAmount,
                "api_key":RAZORPAY_API_KEY,
                "order_id":paymentId,
                "User":buyer
            })
    else:
        return HttpResponseRedirect("/checkout/")

@login_required(login_url='/login/')
def paymentSuccessPage(Request,rppid,rpoid,rpsid):
    buyer = Buyer.objects.get(username=Request.user)
    check = Checkout.objects.filter(user=buyer)
    check=check[::-1]
    check=check[0]
    check.rppid=rppid
    check.paymentStatus=2
    check.save()
    
    subject = 'Order Has Been Placed : Team E-Cart'
    message =   """
                Hello """+buyer.name+"""
                Your Order Has Been Placed!!!
                Now Your Track Your Order in Profile Section
                Team : E-Cart
                """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [buyer.email, ]
    send_mail( subject, message, email_from, recipient_list )
    return HttpResponseRedirect('/confirmation/')


@login_required(login_url="/login/")
def payAgainPage(Request,checkid):
    try:
        check = Checkout.objects.get(id=checkid)
        buyer = Buyer.objects.get(username=Request.user)
        orderAmount = check.final*100
        orderCurrency = "INR"
        paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
        paymentId = paymentOrder['id']
        check.paymentMode=2
        check.save()
        return render(Request,"pay.html",{
            "amount":orderAmount,
            "api_key":RAZORPAY_API_KEY,
            "order_id":paymentId,
            "User":buyer
        })
    except:
        return HttpResponseRedirect("/profile/")

@login_required(login_url="/login/")
def confirmationPage(Request):
    return render(Request,"confirmation.html")

def contactPage(Request):
    if(Request.method=="POST"):
        c = Contact()
        c.name = Request.POST.get("name")
        c.email = Request.POST.get("email")
        c.phone = Request.POST.get("phone")
        c.subject = Request.POST.get("subject")
        c.message = Request.POST.get("message")
        c.save()
        messages.success(Request,"Thanks to Share Your Query With Us!!! Our Team Will Contact You Soon!!!")
    return render(Request,"contact.html")


def loginPage(Request):
    if(Request.method=="POST"):
        username = Request.POST.get("username")
        password = Request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if(user is None):
            messages.error(Request,"Invalid Username or Password!!!")
        else:
            auth.login(Request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
    return render(Request,"login.html")

def signupPage(Request):
    if(Request.method=="POST"):
        if(Request.POST.get("password")!=Request.POST.get("cpassword")):
           messages.error(Request,"Password and Confirm Password Doesn't Matched!!!")
        else:
            try:
                user = User.objects.create(username=Request.POST.get("username")) 
                user.set_password(Request.POST.get("password"))
                user.save()

                b = Buyer()
                b.name = Request.POST.get("name")
                b.username = Request.POST.get("username")
                b.email = Request.POST.get("email")
                b.phone = Request.POST.get("phone")
                b.save()

                subject = 'Your Account Has Been Created : Team E-Cart'
                message =   """
                            Hello """+b.name+"""
                            Thanks to Create an Account with us
                            Now you can Buy Latest Products
                            Team : E-Cart
                            """
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [b.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/login/")
            except:
                messages.error(Request,"Username Already Taken!!!")
    return render(Request,"signup.html")

@login_required(login_url="/login/")
def profilePage(Request):
    user = User.objects.get(username=Request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        checkout = Checkout.objects.filter(buyer=buyer)
        orders = []
        for item in checkout:
            cp = CheckoutProducts.objects.filter(checkout=item.id)
            orders.append({'checkout':item,'checkoutProducts':cp})
        print(orders,"\n\n\n\n",wishlist,"\n\n\n\n")
        return render(Request,"profile.html",{'data':buyer,'wishlist':wishlist,'orders':orders})

@login_required(login_url="/login/")
def updateProfilePage(Request):
    user = User.objects.get(username=Request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        if(Request.method=="POST"):
            buyer.name = Request.POST.get("name")
            buyer.email = Request.POST.get("email")
            buyer.phone = Request.POST.get("phone")
            buyer.addressline1 = Request.POST.get("addressline1")
            buyer.addressline2 = Request.POST.get("addressline2")
            buyer.addressline3 = Request.POST.get("addressline3")
            buyer.pin = Request.POST.get("pin")
            buyer.city = Request.POST.get("city")
            buyer.state = Request.POST.get("state")
            if(Request.FILES.get("pic")!=None):
                buyer.pic = Request.FILES.get("pic")
            buyer.save()
            return HttpResponseRedirect("/profile/")
        return render(Request,"update-profile.html",{'data':buyer})

def logoutPage(Request):
    auth.logout(Request)
    return HttpResponseRedirect("/login/")


def forgetPasswordPage1(Request):
    if(Request.method=="POST"):
        username = Request.POST.get("username")
        try:
            user = Buyer.objects.get(username=username)
            otp = randint(100000,999999)
            user.otp = otp
            user.save()
            Request.session['reset-password-username'] = username

            subject = 'OTP for Password Reset : Team E-Cart'
            message =   """
                        Hello """+user.name+"""
                        OTP for Password Reset is """+str(otp)+"""
                        Never Share OTP with anyone
                        Team : E-Cart
                        """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect("/forget-password-2/")
        except:
            messages.error(Request,"Invalid Username")
    return render(Request,"forget-password-1.html")

def forgetPasswordPage2(Request):
    if(Request.method=="POST"):
        otp = int(Request.POST.get('otp'))
        try:
            user = Buyer.objects.get(username=Request.session.get("reset-password-username",None))
            if(otp==user.otp):
                return HttpResponseRedirect("/forget-password-3/")
            else:
                messages.error(Request,"Invalid OTP!!!")
        except:
            messages.error(Request,"Un-Authorized")
    return render(Request,"forget-password-2.html")

def forgetPasswordPage3(Request):
    if(Request.method=="POST"):
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if(password==cpassword):
            try:
                user = User.objects.get(username=Request.session.get("reset-password-username",None))
                user.set_password(password)
                user.save()
                if(Request.session['reset-password-username']):
                    del Request.session['reset-password-username']
                return HttpResponseRedirect("/login/")
            except:
                messages.error(Request,"Un-Authorized")
        else:
            messages.error(Request,"Password and Confirm Password Doesn't Matched!!!")
    return render(Request,"forget-password-3.html")
