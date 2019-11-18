from pystackpath.util import BaseObject, pagination_query, PageInfo


class DeliveryDomains(BaseObject):
    def index(self, first="", after="", filter="", sort_by=""):
        """
        Retrieve the delivery domains configured on a site
        :return: a list of domains configures on a site
        """
        pagination = pagination_query(first=first, after=after, filter=filter, sort_by=sort_by)
        response = self._client.get(f"{self._base_api}/delivery-domains",
                                    params=pagination)
        response.raise_for_status()
        items = [self.loaddict(item) for item in response.json()["results"]]
        pageinfo = PageInfo(**response.json()["pageInfo"])

        return {"results": items, "pageinfo": pageinfo}
