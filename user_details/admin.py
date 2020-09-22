from django.contrib import admin

from user_details.models import UserDetails,AccountType,AccountDetails
# Register your models here.

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['vchr_UserName', 'LoginName','vchr_email']
    list_filter = ['vchr_UserName', 'LoginName','vchr_email']
    search_fields = ['vchr_UserName', 'LoginName','vchr_email']

    def full_name(self,obj):
        return obj.first_name+' '+obj.last_name

admin.site.register(UserDetails, UserDetailsAdmin)

class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ['AccountTypeName', 'AccountTypeShortName','createdBy','createdOn']
    list_filter = ['AccountTypeName', 'AccountTypeShortName','createdBy','createdOn']
    search_fields = ['AccountTypeName', 'AccountTypeShortName','createdBy','createdOn']

admin.site.register(AccountType, AccountTypeAdmin)


class AccountDetailsAdmin(admin.ModelAdmin):
    list_display = ['AccountId', 'AccountNo','createdBy','AccountHoldersName','Address','Country','State','DateOfBirth','Age','Sex','ContactNo','ContactEmail','AccountTypeId','createdBy','createdOn']
    list_filter = ['AccountId', 'AccountNo','createdBy','AccountHoldersName','Address']
    search_fields = ['AccountId', 'AccountNo','createdBy','AccountHoldersName','Address']

admin.site.register(AccountDetails, AccountDetailsAdmin)
