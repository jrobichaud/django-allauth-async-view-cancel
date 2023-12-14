import asyncio

from django.http import HttpResponse

# Create your views here.

async def async_view(request):
    for num in range(1, 2):
        await asyncio.sleep(1)
    return HttpResponse(status=200)
