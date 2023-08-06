class CrossSiteMiddleware():

    def process_reponse(self, request, response):

        response["name"] = "shenxianjie"
        return response
