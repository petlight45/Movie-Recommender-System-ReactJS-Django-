from django.http import JsonResponse,HttpResponse
from .scripts.main import get_recommendations_
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Serve Single Page Application
index = never_cache(TemplateView.as_view(template_name='index.html'))

def get_recommendations(request):
	response_ = get_recommendations_(**dict(request.GET.copy()))
	if response_[0]:
		response =  JsonResponse({"recommended_ids":response_[0],"matched_id":response_[1]})
		response.status_code = 200
		return response
	response = HttpResponse('Error Encountered')
	response.status_code = 404
	return response