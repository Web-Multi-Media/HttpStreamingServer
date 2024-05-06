import traceback
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from celery import result

import logging 

logger = logging.getLogger("root")

class Task(APIView):

    def get(self, request, task_id):
        logger.debug("task id = {} ".format(task_id))
        state = result.AsyncResult(task_id).state
        return JsonResponse(status=200, data={'state': str(state)})