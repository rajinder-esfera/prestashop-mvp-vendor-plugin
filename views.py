from django.shortcuts import render
from django.views.generic import TemplateView,View
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from images.models import Images
from mailjet_rest import Client
from django.conf import settings
import pycountry,requests,json
mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET))

def send_template(emailid, Vars, template_id):
	data = {
		'FromEmail': 'info@fashioncircle.de',
		'FromName': 'Chris Weber',
		'MJ-TemplateID': template_id,
		'MJ-TemplateLanguage': True,
		'Recipients': [
			{ "Email": emailid}
		],
		'Vars': Vars
	}
	result = mailjet.send.create(data=data)
	return

class VendorRegister(TemplateView):
	template_name = 'vendor/per_vend_register.html'

	def post(self, request, *args, **kwargs):
		response={}

		context = super(VendorRegister, self).get_context_data()
		name = request.POST['name']

		email=request.POST['email']
		platform=request.POST['platform']
		website=request.POST['website']
		country=request.POST['country']
		api_key ="pbkdf2_sha256$29000$p7lpJChcK4Lo$IHMul9j5lcPNJP4f/W1nXZknVi2N+GJIR1tZCo5C7uM="
		data ={"api_key":api_key,"name":name,"email":email,"platform":platform,"website":website,"country":country}
		headers={'HTTP_API_KEY':'de'}
		url=  settings.SITE_URL+'/vendors/add'
		try:
			posted=requests.post(url,params=data,headers=headers)
			response=posted.text


		except Exception as r:
			response['exception']=r

		return HttpResponse(json.dumps(response))

	def get_context_data(self, *args, **kwargs):
		context = super(VendorRegister, self).get_context_data(**kwargs)
		all_countries = []

		countries_list = list(pycountry.countries)
		for country in countries_list:
			all_countries.append(country.name)
		context['all_countries']=all_countries
		return context





class VendorLogin(TemplateView):
	template_name = 'vendor/per_vend_login.html'
	def post(self, request, *args, **kwargs):

		response={}
		context = super(VendorLogin, self).get_context_data()
		email = request.POST['loginemail']
		password = request.POST['loginpassword']
		email_obj=Account.objects.filter(emailid=email)
		if not email_obj:
			response['emailerror']='email'
		else:
			status=email_obj[0].status
			if status==0:
				response['status']='status'
				return HttpResponse(response)
			added_shop=email_obj[0].added_shop
			if added_shop!='yes':
				response['shop']='shop'
				return HttpResponse(response)

			# print ('email matched')
			hash_password = email_obj[0].password
			verify_password = handler.verify(password, hash_password)
			print ('\n\n' +str(verify_password))
			if verify_password is False:
				response['passworderror']='password'
			else:
				token=email_obj[0].token
				request.session['vendor_token'] = token
				print (request.session['vendor_token'])
				response['success']='success'
		return HttpResponse(response)


		# email=request.POST['email']
		# platform=request.POST['platform']
		# website=request.POST['website']
		# country=request.POST['country']
		# api_key ="pbkdf2_sha256$29000$p7lpJChcK4Lo$IHMul9j5lcPNJP4f/W1nXZknVi2N+GJIR1tZCo5C7uM="
		# data ={"api_key":api_key,"name":name,"email":email,"platform":platform,"website":website,"country":country}
		# headers={'HTTP_API_KEY':'de'}
		# url=  settings.SITE_URL+'/vendors/add'
		# try:
		# 	posted=requests.post(url,params=data,headers=headers)
		# 	response=posted.text
		#
		#
		# except Exception as r:
		# 	response['exception']=r


	def get_context_data(self, *args, **kwargs):

		context = super(VendorLogin, self).get_context_data(**kwargs)
		all_countries = []

		countries_list = list(pycountry.countries)
		for country in countries_list:
			all_countries.append(country.name)
		context['all_countries']=all_countries
		return context

class VendorForgetPassword(TemplateView):

	template_name = 'vendor/per_vend_forget_password.html'

	def get_context_data(self, *args, **kwargs):
		context = super(VendorForgetPassword, self).get_context_data(**kwargs)
		return context

	def post(self, request, *args, **kwargs):
		response={}
		email=request.POST.get("email")
		try:
			account=Account.objects.get(emailid=email)
			if account.status==0:
				response['status']=0
				response['msg']="This is a inactive account. Contact with administrator to activate your account."
			elif account.added_shop=="no":
				response['status']=0
				response['msg']="There is no shop associated with this account."
			elif account.platform !="Magento":
				response['status']=0
				response['msg']="This is not right platform for this email. This email is associated with Magento."
			else:
				password = binascii.hexlify(os.urandom(16)).decode()
				encrypted = handler.encrypt(password)
				account.password=encrypted
				account.save()
				first_name = account.first_name
				Vars = {"first_name": first_name, "merchant_name": account.platform,"password":password}
				template_id = "253891"
				send_template(email, Vars, template_id)
				response['status']=1
				response['msg']="New password is send to "+email+". Please check your email."
		except Account.DoesNotExist:
			response['status']=0
			response['msg']="There is no account associated with this email."
		return HttpResponse(json.dumps(response), content_type='application/json')


class VendorDashboard(TemplateView):

	template_name = 'vendor/per_vend_dashboard.html'

	def get(self, request, *arg, **kwargs):

		return render(request, self.template_name,{})

	def post(self, request, *args, **kwargs):

		return HttpResponse("")
