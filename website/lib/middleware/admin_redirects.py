from django.http import HttpResponseRedirect


class AdminRedirectMiddleware:
    """ allows you to customize redirects with the GET line in the admin """

    def process_response(self, request, response):
        # save redirects if given
        try:
            if request.method == "GET" and request.GET.get("next", False):
                request.session["next"] = request.GET.get("next")
                request.session["next_counter"] = 1

            """
            NOT really working...
            """
            if request.method == "POST":
                if request.session.get("next_counter", 0):
                    if request.session.get("next_counter", 0) < 1:
                        del request.session["next"]

                    request.session["next_counter"] = request.session.get("next_counter", 0) - 1


    
            # apply redirects
            if request.session.get("next", False) and \
            type(response) == HttpResponseRedirect and \
            request.path.startswith("/admin/"):
                path = request.session.get("next")
                del request.session["next"]
                return HttpResponseRedirect(path)

            return response
        except:
            return response