from django.shortcuts import render,redirect
from .models import account as model_account,category as model_category,transaction as model_transaction
from django.contrib import messages
from django.utils import timezone
from .utils import create_chart
# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    if request.method == "GET":
        context = {}
        account_array = []
        for accounts in model_account.objects.filter(user=request.user):
            temporary_account_details = {}
            temporary_account_details['name'] = accounts.name
            temporary_account_details['id'] = accounts.id
            account_array.append(temporary_account_details)

        category_income_array = []
        for category in model_category.objects.filter(user=request.user).filter(is_credit=True):
            temporary_category_income_details = {}
            temporary_category_income_details['name'] = category.name
            temporary_category_income_details['id'] = category.id
            temporary_category_income_details['type'] = str(category.is_credit).lower()
            category_income_array.append(temporary_category_income_details)
        
        category_expense_array = []
        for category in model_category.objects.filter(user=request.user).filter(is_credit=False):
            temporary_category_expense_details = {}
            temporary_category_expense_details['name'] = category.name
            temporary_category_expense_details['id'] = category.id
            temporary_category_expense_details['type'] = str(category.is_credit).lower()
            category_expense_array.append(temporary_category_expense_details)
        context['account'] = account_array
        context['category_income'] = category_income_array
        context['category_expense'] = category_expense_array
        context['report']=False
        return render(request,"dashboard/index.html",context)
    elif request.method == "POST":
        request_data = request.POST
        if 'category' not in request_data or 'account' not in request_data:
            messages.add_message(request, messages.ERROR,
                                 'Invalid Data', "alert-danger")
            return redirect("dashboard:home")
        transaction_account = model_account.objects.get(pk=request_data.get('account'))
        transaction_category = model_category.objects.get(pk=request_data.get('category'))
        transaction_type = False
        if request_data.get('type') == 'income':
            transaction_type = True
        new_transaction = model_transaction(account=transaction_account,category=transaction_category,user=request.user,transaction_description=request_data.get('description'),transaction_amount=request_data.get('amount'),is_credit=transaction_type)
        new_transaction.save()
        if(transaction_type):
           balance = transaction_account.balance
           transaction_account.balance = balance + int(request_data.get('amount'))
        else:
           balance = transaction_account.balance
           transaction_account.balance = balance - int(request_data.get('amount'))
        transaction_account.save()
        messages.add_message(request, messages.SUCCESS,
                                 'Data Saved', "alert-success")
        return redirect("dashboard:report")

def usercontrol(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    try:
        if not request.method == "POST":
            return redirect("dashboard:home")
        request_data = request.POST
        if request_data.get('type') == "Account":
            new_Account = model_account(user = request.user,name = request_data.get('name'))
            new_Account.save()
        elif request_data.get('type') == "Category":
            is_credit = False
            if  request_data.get('type-iscredit') == 'true':
                is_credit = True
            new_category = model_category(user = request.user,name = request_data.get('name'),is_credit = is_credit)
            new_category.save()
        messages.add_message(request, messages.SUCCESS,
                                 'Data Added', "alert-success")
    except:
        messages.add_message(request, messages.SUCCESS,
                                 'Duplicate Data', "alert-success")
        return redirect("dashboard:home")
    return redirect("dashboard:home")

def report(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    if request.method == "GET":
        context = {}
        context['report'] = True
        account_array = []
        for accounts in model_account.objects.filter(user=request.user):
            temporary_account_details = {}
            temporary_account_details['name'] = accounts.name
            temporary_account_details['id'] = accounts.id
            temporary_account_details['balance'] = accounts.balance
            account_array.append(temporary_account_details)

        category_income_array = []
        for category in model_category.objects.filter(user=request.user).filter(is_credit=True):
            temporary_category_income_details = {}
            temporary_category_income_details['name'] = category.name
            temporary_category_income_details['id'] = category.id
            temporary_category_income_details['type'] = str(category.is_credit).lower()
            category_income_array.append(temporary_category_income_details)
        
        category_expense_array = []
        for category in model_category.objects.filter(user=request.user).filter(is_credit=False):
            temporary_category_expense_details = {}
            temporary_category_expense_details['name'] = category.name
            temporary_category_expense_details['id'] = category.id
            temporary_category_expense_details['type'] = str(category.is_credit).lower()
            category_expense_array.append(temporary_category_expense_details)

        transaction_elements = model_transaction.objects.filter(user=request.user)
        transaction_details = []
        balance = 0
        for element in transaction_elements:
            temporary_transaction_details = {}
            temporary_transaction_details['id'] = element.id
            temporary_transaction_details['account'] = element.account.name
            temporary_transaction_details['category'] = element.category.name
            temporary_transaction_details['description'] = element.transaction_description
            temporary_transaction_details['amount'] = element.transaction_amount
            if(element.is_credit):
                temporary_transaction_details['type'] = "Income"
                balance += int(element.transaction_amount)
            else:
                temporary_transaction_details['type'] = "Expense"
                balance -= int(element.transaction_amount)
            temporary_transaction_details['balance'] = str(balance)
            temporary_date = element.created_on.strftime("%d-%m-%Y")
            temporary_transaction_details['date'] = temporary_date
            transaction_details.append(temporary_transaction_details)
            
        report_data_category_expense = {}
        for element in model_category.objects.filter(user=request.user):
            if not element.is_credit:
                amount = 0
                for transaction in element.transaction_set.all():
                    amount =amount + transaction.transaction_amount
                report_data_category_expense[element.name] = amount
        value = []
        label = []
        temporary_report = {}
        for element in report_data_category_expense:
            label.append(element)
            value.append(report_data_category_expense[element])
        temporary_report['label'] = label
        temporary_report['value'] = value
        
        context['transactions'] = transaction_details
        context['account'] = account_array
        context['category_income'] = category_income_array
        context['category_expense'] = category_expense_array
        context['today_date'] = timezone.now().strftime("%Y-%m-%d")
        context['report_data'] = temporary_report
        print(temporary_report)
        return render(request,'dashboard/report.html',context)
    
def transaction_control(request,transaction_id):
    if not request.user.is_authenticated:
        return redirect("login:login")
    trasaction_to_delete = model_transaction.objects.get(pk=transaction_id)
    if(trasaction_to_delete.is_credit):
        trasaction_to_delete.account.balance = trasaction_to_delete.account.balance - trasaction_to_delete.transaction_amount
    else:
        trasaction_to_delete.account.balance = trasaction_to_delete.account.balance + trasaction_to_delete.transaction_amount
    trasaction_to_delete.account.save()
    trasaction_to_delete.delete()
    return redirect("dashboard:report")