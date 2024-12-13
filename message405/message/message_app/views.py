
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Msg

def hello(request):
    return HttpResponse("Hello, linked successfully")

def create(request):
    # print("request is: ",request.method)
    # return render(request,'create.html')
    if request.method=="POST":
        n=request.POST['name']
        email=request.POST['email']
        mob=request.POST['mobile']
        msg=request.POST['message']
        # print(n)
        # print(email)
        # print(mob)
        # print(msg)
        m=Msg.objects.create(name=n,email=email,mobile=mob,message=msg)
        m.save()
        # return HttpResponse("data inserted successfully")
        return redirect('/dashboard')
    else:
        print("request is: ",request.method)
        return render(request,'create.html')
    
# def form(request):
#     # print("request is: ",request.method)
#     # return render(request,'create.html')
#     if request.method=="POST":
#         c_name=request.POST['course name']
#         name=request.POST['name']
#         mob=request.POST['mobile']
#         msg=request.POST['message']
#         # print(n)
#         # print(email)
#         # print(mob)
#         # print(msg)
#         m=Msg.objects.create(name=n,email=email,mobile=mob,message=msg)
#         m.save()
#         return HttpResponse("data inserted successfully")
#     else:
#         print("request is: ",request.method)
#         return render(request,'create.html')
    
    
def dashboard(request):
    m=Msg.objects.all()
    print(m)
    context={}
    context['data']=m
    #return HttpResponse("Data fetch successfully....")
    return render(request,'dashboard.html',context)
    
def delete(request,rid) :
    print("Id of record to be deleted: "+rid)
    m=Msg.objects.filter(id=rid)
    m.delete()
    # return HttpResponse("id: "+rid)
    return redirect('/dashboard')

def edit(request,rid):
    # print("Id to be edited: "+rid)
    # return HttpResponse("Id: "+rid)
    if request.method=="POST":
        n=request.POST['name']
        email=request.POST['email']
        mob=request.POST['mobile']
        msg=request.POST['message']
        m=Msg.objects.filter(id=rid)
        m.update(name=n,email=email,mobile=mob,message=msg)
        return redirect("/dashboard")
    else:
         message = Msg.objects.get(id=rid)
         context = {'data': message}
         return render(request, 'edit.html', context)
