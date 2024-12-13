from random import randrange
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate,login,logout
from ecomm_app.models import product,Cart,Order
from django.db.models import Q
import razorpay

# def about(request):
#     return HttpResponse("This is about page")

def contact(request):
    return HttpResponse("This is contact page")



def edit_fun(request,sid):
    print("Id is edited",sid)
    return HttpResponse("Id to be edited: "+sid)

def delete(request,sid):
    print("Id is deleted",sid)
    return HttpResponse("Id to be deleted: "+sid)

class SimpleView(View):
    def get(self,request):
        return HttpResponse("This is simple view--get")
    
    def post(self,request):
        return HttpResponse("Data added from simple view")

#Render function
def hello(request):
    context={}
    context['greet']="Good afternoon, we are learning DTL"
    
    context['x']=20
    context['y']=100
    
    context['li']=[20,30,10,33,55]
    context['product']=[
        {'id':101,'name':'Samsung','cat':'mobile','price':'20000'},
        {'id':102,'name':'Smart TV','cat':'TV','price':'25000'},
        {'id':103,'name':'Fan','cat':'electronic','price':'3000'},
        {'id':104,'name':'Whirlpool','cat':'washing machine','price':'40000'},
        {'id':105,'name':'Bajaj AC','cat':'electronics','price':'50000'},
        {'id':106,'name':'Water heater','cat':'electroics','price':'2000'},
        
    
    ]

    return render(request,'hello.html',context)  
    
def home(request):
    userid=request.user.id
    # print("id of logged in user: ",userid)
    # print("result is: ",request.user.is_authenticated)
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    print(p)
    return render(request,'index.html',context)

def product_details(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'product_details.html',context)

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    for x in c:
        s=s+x.pid.price * x.qty
    print(s)    
    context={}
    context['products']=c 
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)  

 
def user_register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="feilds cannot be empty.."
            return render(request,'register.html',context)
        elif upass != ucpass:
            context['errmsg']="password and confirm password didn't match.."
            return render(request,'register.html',context)
        else:  
            try:  
                u = User.objects.create(username=uname, password=upass,email=uname)
                u.set_password(upass)       #encrypt format
                u.save()
                context['success']="User created successfully"
                return render(request, 'register.html',context)
            except Exception:
                context['errmsg']="user with same username already present.."
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    
    
def user_login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="fields cannot be empty.."
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            if u is not None:
                login(request,u)    # start the session
                return redirect('/home')
            else:
                context['errmsg']="Invalid username and password.."
                return render(request,'login.html',context)            
    else:
     return render(request,'login.html')
       
def user_logout(request):
    logout(request)
    return redirect('/home')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    context={}
    context['products']=p 
    return render(request,'index.html',context) 

def sort(request,sv):  #sv=0 or 1
    if sv=='0':
        col='price'  #ascending
    else :
        col='-price' #decending
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min= request.GET.get('min')
    max=request.GET.get('max')
    # print(min)
    # print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    
def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u[0])
        p=product.objects.filter(id=pid)
        print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['product']=p
        if n==1:
            context['msg']="product already exist in the cart"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added successfully in cart"
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')
    
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c)             #object queryset
    print(c[0])          #object
    print(c[0].qty)      #quantity only
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:      #1>1=F
            t=c[0].qty-1
            c.update(qty=t)    
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    # print(userid)
    c=Cart.objects.filter(uid=userid)
    # print(c)
    oid=randrange(1000,9999)
    print("order_id: ", oid)
    for x in c:
        o=Order.objects.create(order_id=oid,uid=x.uid,pid=x.pid,qty=x.qty)
        o.save()
        x.delete()  #to delete cart data
        orders=Order.objects.filter(uid=request.user.id)
        context={}
        context['products']=orders
        np=len(orders)
        s=0
        for x in orders:
            s=s+x.pid.price + x.qty
            context['total']=s
            context['n']=np
            
    return render(request,"placeorder.html",context)  

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
         s=s+x.pid.price * x.qty
         oid= x.order_id
    
    client = razorpay.Client(auth=("rzp_test_a4ZXWOWwnsyyaF", "oKBc64i89fKN0JvESmUbR1qN"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)  