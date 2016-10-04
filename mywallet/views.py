from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, View

from .models import Wallet, Currency, AccountStatement, DiffOperation

from datetime import datetime
import json as simplejson

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import detail_route
from .serializers import WalletSerializer


class IndexView(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            operation_list = DiffOperation.objects.filter(user=request.user).order_by('date')
            paginator = Paginator(operation_list, 6)
            page = request.GET.get('page')
            try:
                operations = paginator.page(page)
            except PageNotAnInteger:
                operations = paginator.page(paginator.num_pages)
            except EmptyPage:
                operations = paginator.page(paginator.num_pages)

            return render(request, 'mywallet/mywallet.html', {'operations': operations})
        return HttpResponseRedirect('/')


class LogoutView(TemplateView):
    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class NewWallet(View):
    @staticmethod
    def validate_data(title, code, value, request):
        error_msg = {}
        try:
            float(value)
        except ValueError:
            error_msg['sum'] = 'Currency must be a numeric'

        if len(code) != 3:
            error_msg['type'] = 'Enter correct currency code'

        if title == '':
            error_msg['name'] = 'Title can not be empty'

        if Wallet.objects.filter(user=request.user, title=title):
            error_msg['name'] = 'You are already have this wallet'

        if error_msg:
            error_msg['status'] = '400'
        return error_msg

    @staticmethod
    def add_wallet(user, currency_type, name, value):
        wallet = Wallet(title=name)
        wallet.user = user
        wallet.save()

        statement = AccountStatement(value=value)
        statement.wallet = wallet
        statement.save()

        currency = Currency(code=currency_type)
        currency.value = statement
        currency.save()

    def post(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                name = request.POST.get('name')
                currency_type = request.POST.get('type').upper()
                value = request.POST.get('sum')

                error_msg = self.validate_data(name, currency_type, value, request)

                if not error_msg:
                    self.add_wallet(request.user,
                                    currency_type,
                                    name,
                                    value)

                    error_msg['status'] = '200'
                return HttpResponse(json.dumps(error_msg),
                                    content_type="application/json")

        return HttpResponseRedirect('/')


class NewOperation(View):
    @staticmethod
    def validate_data(operation_type, operation_title, operation_value,
                      date, request, wallet_title):
        error_msg = {}

        try:
            float(operation_value)
        except ValueError:
            error_msg['sum'] = 'Currency must be a numeric'

        if operation_title == '':
            error_msg['name'] = 'Title can not be empty'

        if operation_type != 'SP' and operation_type != 'DP':
            error_msg['type'] = 'Wrong type operation'

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:  # find correct exception
            error_msg['date'] = 'Wrong date'

        wallet = Wallet.objects.filter(user=request.user, title=wallet_title)
        if not wallet:
            error_msg['wallet'] = 'Wrong wallet title'

        return error_msg

    @staticmethod
    def add_operation(request, wallet_title, select_value, code, operation_type, operation_value, operation_title,
                      date):
        wallet = Wallet.objects.get(user=request.user, title=wallet_title)
        account = AccountStatement.objects.get(wallet=wallet, value=select_value)
        currency = Currency.objects.get(value=account, code=code)

        new_operation = DiffOperation(title=operation_title, date=date,
                                      sum=operation_value, operation_type=operation_type)
        new_operation.currency = currency
        new_operation.user = request.user
        new_operation.wallet_title = wallet_title
        new_operation.save()
        if operation_type == 'SP':
            account.value -= float(operation_value)
        else:
            account.value += float(operation_value)
        account.save()

    def post(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                operation_type = request.POST.get('type')
                operation_title = request.POST.get('title')
                operation_value = request.POST.get('sum')
                wallet_title = request.POST.get('wallet')
                code = request.POST.get('code')
                date = request.POST.get('date')
                select_value = request.POST.get('select_value')

                error_msg = self.validate_data(operation_type, operation_title, operation_value,
                                               date, request, wallet_title)
                if not error_msg:
                    self.add_operation(request, wallet_title, select_value, code, operation_type, operation_value,
                                       operation_title, date)

                    error_msg['status'] = '200'

                return HttpResponse(json.dumps(error_msg),
                                    content_type="application/json")

            return HttpResponseRedirect('/')


class NewCurrency(View):
    @staticmethod
    def validate_data(title, code, value, request):
        error_msg = {}
        try:
            float(value)
        except ValueError:
            error_msg['sum'] = 'Currency must be a numeric'

        if len(code) != 3:
            error_msg['type'] = 'Enter correct currency code'

        wallet = Wallet.objects.filter(user=request.user, title=title)
        accounts = AccountStatement.objects.filter(wallet=wallet)
        for account in accounts:
            if Currency.objects.filter(value=account, code=code):
                error_msg['type'] = 'You are already have this currency'

        if error_msg:
            error_msg['status'] = '400'

        return error_msg

    @staticmethod
    def add_currency(title, code, value, request):
        wallet = Wallet.objects.get(user=request.user, title=title)

        statement = AccountStatement(value=value)
        statement.wallet = wallet
        statement.save()

        currency = Currency(code=code)
        currency.value = statement
        currency.save()

    def post(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                title = request.POST.get('title')
                code = request.POST.get('code').upper()
                value = request.POST.get('sum')

                error_msg = self.validate_data(title, code, value, request)

                if not error_msg:
                    self.add_currency(title, code, value, request)

                    error_msg['status'] = '200'

                return HttpResponse(json.dumps(error_msg),
                                    content_type="application/json")

        return HttpResponseRedirect('/')


class EditWalletTitle(View):
    def post(self, request):
        if request.method == "POST":
            if request.is_ajax():
                old_title = request.POST.get('oldTitle')
                new_title = request.POST.get('newTitle')
                if new_title != '' and len(new_title) <= 20:
                    error_msg = {'status': '200'}
                    wallet = Wallet.objects.get(user=request.user, title=old_title)
                    wallet.title = new_title
                    wallet.save()
                    return HttpResponse(json.dumps(error_msg),
                                        content_type="application/json")
                else:
                    error_msg = {'title': 'Wrong title'}
                    return HttpResponse(json.dumps(error_msg),
                                        content_type="application/json")
        return HttpResponseRedirect('/')


class GetWalletTitles(View):
    def get(self, request, **kwargs):
        if request.method == 'GET':
            if request.is_ajax():
                wallets = Wallet.objects.filter(user=request.user)
                wallets_data = [{'title': item.title} for item in wallets]
                return HttpResponse(json.dumps(wallets_data), content_type="application/json")
        return HttpResponseRedirect('/')


class GetCodes(View):
    @staticmethod
    def get_values(accounts):
        accounts_dict = {}
        for account in accounts:
            code = Currency.objects.filter(value=account)
            for value in code:
                accounts_dict[str(account)] = str(value)
        return accounts_dict

    def get(self, request, **kwargs):
        if request.method == 'GET':
            if request.is_ajax():
                title = request.GET.get('walletTitle')
                wallet = Wallet.objects.filter(user=request.user, title=title)
                accounts = AccountStatement.objects.filter(wallet=wallet)
                codes = self.get_values(accounts)
                return HttpResponse(json.dumps(codes), content_type="application/json")
        return HttpResponseRedirect('/')


# class GetWallets(View):
#     @staticmethod
#     def get_values(accounts):
#         accounts_dict = {}
#         for account in accounts:
#             code = Currency.objects.filter(value=account)
#             for value in code:
#                 accounts_dict[str(account)] = str(value)
#         return accounts_dict
#
#     def get(self, request, **kwargs):
#         if request.method == 'GET':
#             if request.is_ajax():
#                 result_dict = {}
#                 wallets = Wallet.objects.filter(user=request.user)
#                 for wallet in wallets:
#                     accounts = AccountStatement.objects.filter(wallet=wallet)
#                     result_dict[str(wallet)] = self.get_values(accounts)
#                 return HttpResponse(json.dumps(result_dict), content_type="application/json")
#         return HttpResponseRedirect('/')


class WalletList(APIView):
    authentication_classes = (authentication.CsrfViewMiddleware,)
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get_values(accounts):
        accounts_dict = {}
        for account in accounts:
            code = Currency.objects.filter(value=account)
            for value in code:
                accounts_dict[str(account)] = str(value)
        return accounts_dict

    def get(self, request, format=None):
        result_dict = {}
        wallets = Wallet.objects.filter(user=request.user)
        for wallet in wallets:
            accounts = AccountStatement.objects.filter(wallet=wallet)
            result_dict[str(wallet)] = self.get_values(accounts)
        return Response(result_dict)
