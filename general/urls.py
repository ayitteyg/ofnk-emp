from django.urls import path 
from general.views import *
from accounts_set import views as account_views
# from general.views import homeview,userpage, formsubmit ,empUpdate, MsgToStaff,UserMsg, Letters, UserLtrs,
from django.contrib.auth import views as auth_views


urlpatterns = [ 
    path('', homeview.as_view(template_name='pages/home.html'), name='home'),
    path('user/records/update', empUpdate.as_view(template_name='pages/update.html'), name='update'),
    path('login/success', userpage.as_view(template_name='pages/userpage'), name='userpage'),
    path('staff/formsubmit', formsubmit.as_view(template_name='pages/formsubmit'), name='formsubmit'),

    path('staff/records', MsgToStaff.as_view(template_name='pages/messages'), name='MsgToStaff'),
    path('staff/messages', UserMsg.as_view(template_name='pages/UserMsg.html'), name='UserMsg'),
    path('emp-ofnk-mgnt-all-mgs', AllMsgs.as_view(template_name='pages/AllMsg.html'), name='AllMsg'),

    path('mgnt/actions/letters', SendLetters.as_view(template_name='pages/letters.html'), name='letters'),
    path('staff/records/letters', UserLtrs.as_view(template_name='pages/UserLtrs.html'), name='UserLtrs'),
    path('emp-ofnk-mgnt-all-ltrs', AllLtrs.as_view(template_name='pages/AllLtrs.html'), name='AllLtrs'),

    path('staff/records/?Acrdtation/aprasl', Acrdtation.as_view(template_name='Docs/Acrdtn.html'), name='Acrdtn'),
    path('staff/records?/letters/view', LtrsView.as_view(template_name='Doc/LtrsV.html'), name='LtrsV'),
    path('staff/records/resources', RscMaterail.as_view(template_name='pages/resources.html'), name='resources'),
    path('emp-ofnk-Rcs-fl?/<int:pk>/docs-docV', DocView.as_view(template_name='Docs/docV.html'), name='docV'),
    path('emp-ofnk-mgnt-Rcs', RscView.as_view(template_name='Docs/rsc.html'), name='rsc'),
    path('emp-ofnk-mgnt-All_?/Rcs', AllRsc.as_view(template_name='Docs/Allrsc.html'), name='Allrsc'),




    path('accounts/login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/signup', account_views.signup, name='signup'),




    #managers-page
    path('emp-mgnt-?-staff', StaffLst.as_view(template_name='pages/StaffLst.html'), name='StaffLst'),
    path('emp-ofnkstaff?/details', StaffLstDtls.as_view(template_name='pages/StaffLstDtls.html'), name='StaffLstDtls'),






]