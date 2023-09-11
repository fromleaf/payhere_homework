from rest_framework import status


def reform_response(instance, response):
    if response.status_code == status.HTTP_204_NO_CONTENT:
        return response

    if hasattr(instance, 'queryset') and hasattr(instance.queryset, 'model'):
        model_name = instance.queryset.model._meta.model_name
        if hasattr(response.data, 'result'):
            response.data[model_name] = response.data['result']
            del response.data['result']
        elif hasattr(response.data, 'results'):
            model_name = '{}s'.format(model_name)
            response.data[model_name] = response.data['results']
            del response.data['results']

    response.data = {
        "meta": {
            "code": response.status_code,
            "message": response.status_text,
        },
        "data": response.data
    }
    return response
