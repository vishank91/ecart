from django import template

register = template.Library()

@register.filter(name="paymentStatusFilter")
def paymentStatusFilter(Request, status):
    if(status==1):
        return "Pending"
    else:
        return "Done"


@register.filter(name="paymentModeFilter")
def paymentModeFilter(Request, mode):
    if(mode==1):
        return "COD"
    else:
        return "Net Banking"

@register.filter(name="orderStatusFilter")
def orderStatusFilter(Request, status):
    if(status==1):
        return "Order Placed"
    elif(status==2):
        return "Ready to Dispatch"
    elif(status==3):
        return "Dispatched"
    elif(status==4):
        return "Out for Delivery"
    else:
        return "Delivered"
    

@register.filter(name="checkForRepayment")
def checkForRepayment(Request, checkout):
    if(checkout.paymentStatus==1 and checkout.paymentMode==2):
        return True
    else:
        return False