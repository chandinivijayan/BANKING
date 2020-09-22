from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from django.conf import settings
from django.db import transaction
from datetime import datetime
import sys, os
from django.contrib.auth import authenticate, login
import requests
import json
from django.db.models import  Q



from django.contrib.auth.models import User
from user_details.models import UserDetails,AccountType,AccountDetails

# Create your views here.


class CreateAccount(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            with transaction.atomic():
                # import pdb; pdb.set_trace()
                """create account"""
                user_name = request.data.get('strUserName')
                login_name = request.data.get('strLoginName')
                mail = request.data.get('strUserEmail')

                if UserDetails.objects.filter(username = login_name):
                    return Response({'status':2,'message':'Login name already exists'})

                abc = " "
                ins_user = UserDetails.objects.create(username = login_name,
                                                    LoginName = login_name,
                                                    vchr_UserName = user_name,
                                                    first_name = user_name.split(" ")[0],
                                                    last_name = abc.join(user_name.split(" ")[1:]),
                                                    vchr_email = mail,
                                                    email = mail,
                                                    is_active = True,
                                                    is_superuser = False
                                                    )

                ins_user.set_password(request.data.get('strUserPassword'))
                ins_user.save()


                return Response({'status':1})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

class loginCheck(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        try :
            # import pdb; pdb.set_trace()
            str_username= request.data['str_username']
            str_password=request.data['str_password']
            user = authenticate(request, username=str_username, password=str_password)
            # import pdb; pdb.set_trace()
            # if user.userdetails.fk_desig.vchr_name == "CLIENT":
            #     return Response({'status':0,'reason':'No user'})
            if user:
                if user.is_staff:
                    login(request, user)
                    token_json = requests.post(request.scheme+'://'+request.get_host()+'/api-token-auth/',{'username':str_username,'password':str_password})
                    token = json.loads(token_json._content.decode("utf-8"))['token']
                    str_name='Super User'
                    email = user.email or ''
                    userdetails={'Name':str_name,'email':email}

                    return Response({'status':1,'token':token,'userdetails':userdetails,"str_session_key":request.session.session_key})
                else:
                    login(request,user)
                    token_json = requests.post('http://'+request.get_host()+'/api-token-auth/',{'username':str_username,'password':str_password})
                    token = json.loads(token_json._content.decode("utf-8"))['token']

                    email=user.email or ''

                    rst_user = UserDetails.objects.filter(user_ptr_id=request.user.id).values('id','first_name','last_name')

                    str_name = rst_user[0]['first_name'] +" "+rst_user[0]['last_name']

                    userdetails={'Name':str_name.title(),'int_user_id':rst_user[0]['id'],'email':email}

                    return Response({'status':1,'token':token,'userdetails':userdetails,"str_session_key":request.session.session_key})
            else:
                return Response({'status':0,'reason':'No user'})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

class AccountTypeAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try :
            with transaction.atomic():
                """add account type"""
                # import pdb; pdb.set_trace()
                account_type_name = request.data.get('AccountTypeName')
                account_type_short_name = request.data.get('AccountTypeShortName')
                createdBy = request.user.userdetails
                createdOn = datetime.now()

                if AccountType.objects.filter(Q(AccountTypeName__iexact = account_type_name) | Q(AccountTypeShortName__iexact = account_type_short_name)).values():
                    return Response({'status':2,'message':'Account Type already exists'})

                ins_account_type = AccountType.objects.create(AccountTypeName = account_type_name,
                                                                AccountTypeShortName = account_type_short_name,
                                                                createdBy = createdBy,
                                                                createdOn = createdOn,
                                                                )

                return Response({'status':1,'data':"success"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

    def get(self,request):
        try :
            """list account type"""
            lst_account_type = list(AccountType.objects.values('AccountTypeId','AccountTypeName','AccountTypeShortName','createdBy__vchr_UserName','createdOn'))
            return Response({'status':1,'data':"success" ,'lst_account_type':lst_account_type})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


    def put(self,request):
        try :
            """update account type"""
            # import pdb; pdb.set_trace()
            int_account_type_id = request.data.get('intAccountTypeId')
            account_type_name = request.data.get('AccountTypeName')
            account_type_short_name = request.data.get('AccountTypeShortName')

            AccountType.objects.filter(AccountTypeId = int(int_account_type_id)).update(AccountTypeName = account_type_name,AccountTypeShortName = account_type_short_name)

            return Response({'status':1,'data':"success"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

    def patch(self,request):
        try :
            """update account type"""
            # import pdb; pdb.set_trace()
            int_account_type_id = request.data.get('intAccountTypeId')

            AccountType.objects.filter(AccountTypeId = int(int_account_type_id)).delete()

            return Response({'status':1,'data':"success"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


class AccountDetailsAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try :
            with transaction.atomic():
                """add account Details"""
                # import pdb; pdb.set_trace()
                AccountNo = request.data.get('AccountNo')
                AccountHoldersName = request.data.get('AccountHoldersName')
                Address = request.data.get('Address')
                Country = request.data.get('Country')
                State = request.data.get('State')
                DateOfBirth = request.data.get('DateOfBirth')
                Age = request.data.get('Age')
                Sex = request.data.get('Sex')
                ContactNo = request.data.get('ContactNo')
                ContactEmail = request.data.get('ContactEmail')
                AccountTypeId = request.data.get('AccountTypeId')
                createdBy = request.user.userdetails
                createdOn = datetime.now()

                if AccountDetails.objects.filter(AccountNo__iexact = AccountNo).values():
                    return Response({'status':2,'message':'Account Number already exists'})

                ins_account_type = AccountDetails.objects.create(AccountNo = AccountNo,
                                                                AccountHoldersName = AccountHoldersName,
                                                                Address = Address,
                                                                Country = Country,
                                                                State = State,
                                                                DateOfBirth = DateOfBirth,
                                                                Age = Age,
                                                                Sex = Sex,
                                                                ContactNo = ContactNo,
                                                                ContactEmail = ContactEmail,
                                                                AccountTypeId = AccountType.objects.get(AccountTypeId = int(AccountTypeId)),
                                                                createdBy = createdBy,
                                                                createdOn = createdOn,
                                                                )

                return Response({'status':1,'data':"success"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

    def get(self,request):
        try :
            """list account details"""
            lst_account_details = list(AccountDetails.objects.values('AccountId','AccountNo','AccountHoldersName','Address','Country','State','DateOfBirth','Age','Sex','ContactNo','ContactEmail','AccountTypeId','AccountTypeId__AccountTypeShortName','createdBy__vchr_UserName','createdOn'))
            return Response({'status':1,'data':"success",'lst_account_details':lst_account_details})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


    def put(self,request):
        try :
            """update account details"""
            AccountNo = request.data.get('AccountNo')
            AccountHoldersName = request.data.get('AccountHoldersName')
            Address = request.data.get('Address')
            Country = request.data.get('Country')
            State = request.data.get('State')
            DateOfBirth = request.data.get('DateOfBirth')
            Age = request.data.get('Age')
            Sex = request.data.get('Sex')
            ContactNo = request.data.get('ContactNo')
            ContactEmail = request.data.get('ContactEmail')
            AccountTypeId = request.data.get('AccountTypeId')
            int_account_details_id = request.data.get('intAccountDetailsId')

            AccountDetails.objects.filter(AccountId = int(int_account_details_id)).update(AccountHoldersName = AccountHoldersName,Address = Address,Country = Country,State = State,DateOfBirth = DateOfBirth,Age = Age,Sex = Sex,ContactNo = ContactNo,ContactEmail = ContactEmail,AccountTypeId = AccountType.objects.get(AccountTypeId = int(AccountTypeId)))

            return Response({'status':1,'data':"success"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

    def patch(self,request):
        try :
            """update account details"""

            int_account_details_id = request.data.get('intAccountDetailsId')

            AccountDetails.objects.filter(AccountId = int(int_account_details_id)).delete()

            return Response({'status':1,'data':"success"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})
