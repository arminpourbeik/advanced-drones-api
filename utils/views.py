from django.http import JsonResponse


def error_404(request, exception):
    message = "The endpoint does not found"

    response = JsonResponse(data={"message": message, "statusCode": 404})
    response.status_code = 404

    return response


def error_500(request):
    message = "An error occurred. its on us!"

    response = JsonResponse(data={"message": message, "statusCode": 500})
    response.status_code = 500

    return response