import json
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import Resource
from tastypie.http import HttpCreated


class MultipleSearchResource(Resource):
    class Meta:
        resource_name = 'search'
        allowed_methods = ['get']

    def obj_get_list(self, bundle, **kwargs):
        query = bundle.request.GET.get('q')
        async = bundle.request.GET.get('async')

        if not query:
            response = {'status': 0, 'message': 'Empty query'}

        else:
            from search_app.tasks import google, duck_duck_go, twitter

            if async:
                # Async process
                from celery.result import ResultSet
                rs = ResultSet([])
                # Following tasks will run asynchronously
                rs.add(google.delay(query))
                rs.add(duck_duck_go.delay(query))
                rs.add(twitter.delay(query))
                response = rs.get()  # waiting for the results

                try:
                    response = {'google': {'result': response[0], 'query': query},
                                'duckduckgo': {'result': response[1], 'query': query},
                                'twitter': {'result': response[2], 'query': query}
                                }
                except AttributeError:
                    response = {'status': 0, 'message': 'Result Timeout'}
            else:
                google = google(query)
                duck_duck_go = duck_duck_go(query)
                twitter = twitter(query)
                response = {'google': google, 'duckduckgo': duck_duck_go, 'twitter': twitter}

        # For immediate response
        raise ImmediateHttpResponse(
            response=HttpCreated(content=json.dumps(response), content_type='application/json; charset=UTF-8'))
