from dataclasses import fields
import dataclasses
from importlib.resources import Resource
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.http import request, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView
from general.forms import MsgSentForm, empID, EmployeeForm, EmployeeUpdateForm, LettersForm, RscForm
from general.models import Employee, MsgSent, Letters, Resources
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.views.decorators.clickjacking import xframe_options_exempt  


# Create your views here.
class homeview(TemplateView):
    form_class = empID
    def get(self, request, *args, **kwargs):
        msgs = MsgSent.objects.filter(sent_to_id=7).count()
        try:
            user = Employee.objects.get(username_id=request.user.pk)
            dscrp = user.job
            initial = {'staffid': dscrp}
            form = self.form_class(initial=initial)
            return render(request, 'pages/home.html', {'form':form,'msgs':msgs})
        except:
            form = self.form_class()
            return render(request, 'pages/home.html', {'form':form, 'msgs':msgs})
    

    #def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        #if form.is_valid():
            # what you want to do

            #return HttpResponseRedirect('/')
            #return redirect('userpage')# takes name
        #print(form.errors.as_data)
        #return render(request, 'pages/home.html', {'form': form})
    





class formsubmit(TemplateView):
    form_class = EmployeeForm

    def get(self, request, *args, **kwargs):
        form =  self.form_class()
        return render(request, 'pages/formsubmit.html', {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)    
        if form.is_valid():
            try:
                form.save()        
                return redirect('home')
            except:
                print(form.errors.as_data)
                messages.error(self.request, "This staffid already has information!!")
                return redirect('home')
        print(form.errors.as_data)
        messages.error(self.request, "username is wrong or you already have information")
        return redirect('home')
        # return render(request, 'pages/formsubmit.html', {"form":form})








#get data from table
class get_data:
    def records(self, request, *args, **kwargs):
        user = request.user.pk
        staff = get_object_or_404(Employee, username_id=user)
        fields = staff._meta.get_fields()

        #return field label and values
        label = [field.name for field in fields]
        val = [getattr(staff,field.name) for field in fields]
        data = dict(zip(label,val))

        #return name and values
        name = [field.verbose_name for field in fields]
        val1 = [getattr(staff,field.name) for field in fields]
        data1 = dict(zip(name,val))
        return data,data1,label





class userpage(TemplateView):
    def get(self, request, *args, **kwargs):              
         try:
            data = get_data.records(self, request)[1]
            return render(request, 'pages/userpage.html', {"fields":fields, 'data':data})
         except:       
            messages.error(self.request, "Don't have any profile, submit your infomation")
            return redirect('home')
             #return redirect('userpage')# takes name







class empUpdate(UpdateView):
    form_class = EmployeeUpdateForm
            
    def get(self, request, *args, **kwargs):
        context = {} 
        data = get_data.records(self, request)[0]
        form = self.form_class(initial=data)
        context['form'] = form
        return render(request, 'pages/update.html', context)
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user.pk
        print(user)
        if form.is_valid():
            staff = form.cleaned_data
            # print(staff)
            Employee.objects.filter(username_id=user).update(**staff)
            messages.success(self.request, 'Your records have been updated successfully.') 
            return redirect('home')

        print(form.errors.as_data)
        messages.error(self.request, "Sorry, could not update your records" )
        return redirect('home')





class MsgToStaff(TemplateView):
    form_class = MsgSentForm
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user = request.user.pk
        msgs = MsgSent.objects.filter(sent_to_id=user).count()
        return render(request, 'pages/messages.html', {'form':form, 'msgs':msgs})


  
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        sent_by = request.user
        
        if form.is_valid():           
            msg = form.save(commit=False)
            sent_to = form.cleaned_data['sent_to']

            if sent_to == None:
                recepients = User.objects.all()
                sent_to = recepients.exclude(username=sent_by)
                for user in sent_to:
                    msg.pk = None
                    msg.sent_by = sent_by
                    msg.sent_to = user
                    msg.save()
            else:
                msg.sent_by = sent_by
                msg.sent_to = sent_to
                msg.save()

            return redirect('home')
        print(form.errors.as_data)
        return redirect('home')
            





class UserMsg(TemplateView):    
    def get(self, request, *args, **kwargs):
        user_msg = MsgSent.objects.filter(sent_to_id=request.user.pk).all()
        return render(request, 'pages/UserMsg.html', {'user_msg':user_msg})


class AllMsgs(TemplateView):   
    def get(self, request, *args, **kwargs):
        msg = MsgSent.objects.all()
        head = [field.verbose_name for field in MsgSent._meta.get_fields()]
        head = head[1:]
        return render(request, 'pages/AllMsg.html', {'msg':msg, 'head':head}) 







class SendLetters(TemplateView):
    form_class = LettersForm    
    def get(self, request, *args, **kwargs):
        form = self.form_class()  
        return render(request, 'pages/letters.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(self.request, "Sent Successfully")
            return redirect('home')

        messages.error(self.request, "Couldn't save!! Retry")
        print(form.errors.as_data)
        return redirect('letters')  
       



class UserLtrs(TemplateView):   
    def get(self, request, *args, **kwargs):
        userLtrs = Letters.objects.filter(employee_id=request.user.pk).all()
        return render(request, 'pages/UserLtrs.html', {'userLtrs':userLtrs})



class AllLtrs(TemplateView):   
    def get(self, request, *args, **kwargs):
        Ltrs = Letters.objects.all()
        head = [field.verbose_name for field in Letters._meta.get_fields()]
        head = head[1:]
        return render(request, 'pages/AllLtrs.html', {'Ltrs':Ltrs, 'head':head})




class StaffLst(TemplateView):    
    def get(self, request, *args, **kwargs):
        mgnt = Employee.objects.filter(group='management')
        stff = Employee.objects.filter(group='staff')
        trne = Employee.objects.filter(group='trainee')
        return render(request, 'pages/StaffLst.html', {'mgnt':mgnt, 'stff':stff, 'trne':trne})



class StaffLstDtls(TemplateView):
    form_class = EmployeeForm    
    def get(self, request, *args, **kwargs):
        data = Employee.objects.all()
        head = [field.verbose_name for field in Employee._meta.get_fields()]
        return render(request, 'pages/StaffLstDtls.html', {'head':head, 'data':data})



class RscMaterail(TemplateView):   
    def get(self, request, *args, **kwargs):
        doc = Resources.objects.filter(filetype='Resource')
        return render(request, 'pages/resources.html', {'doc':doc})







class DocView(TemplateView): 
    def get(self, request, pk,  *args, **kwargs):
        doc = Resources.objects.get(pk=pk)
        print(doc.pk)
        return render(request, 'Docs/docV.html', {'doc':doc})



class LtrsView(TemplateView): 
    def get(self, request, *args, **kwargs):
        pk = request.user.pk
        doc = Letters.objects.filter(employee_id=pk)
        return render(request, 'Docs/LtrsV.html', {'doc':doc})




class Acrdtation(TemplateView): 
    def get(self, request, *args, **kwargs):
        pk = request.user.pk
        doc = Resources.objects.filter(staff_id=pk)
        return render(request, 'Docs/Acrdtn.html', {'doc':doc})





class RscView (TemplateView):
    form_class = RscForm 
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'Docs/rsc.html', {'form':form}) 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)

            aprsl = form.cleaned_data.get('filetype')
            staff = form.cleaned_data.get('staff')

            if aprsl != 'Resource' and staff == None:
                messages.error(self.request, 'If Accreditation or Appraisal, choose staff') 
                return redirect('rsc')   

            form.save()
            return redirect('home')
        print(form.errors.as_data)
        return redirect('rsc')
        
    


class AllRsc(TemplateView):   
    def get(self, request, *args, **kwargs):
        Rsc = Resources.objects.all()
        head = [field.verbose_name for field in Resources._meta.get_fields()]
        head = head[1:]
        return render(request, 'pages/Allrsc.html', {'Rsc':Rsc, 'head':head})            





class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_message = ''
    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response
    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data













































































        
"""class DownloadFile:  
    def download(self, request, *args, **kwargs):
        file_path =  r'C:/Users/User\Desktop/induction.docx' #can change
        with open(file_path,'rb') as doc:
            response = HttpResponse(doc.read(), content_type='application/ms-word')
            response['Content-Disposition'] = 'attachment;filename=induction.docx'
            return response"""
