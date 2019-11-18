from ..util import BaseObject, pagination_query, PageInfo


class DeliverySites(BaseObject):
    base_api = "/delivery"

    def index(self, first="", after="", filter="", sort_by=""):
        """
        Retrieve the delivery domains configured on a site
        :return: a list of domains configures on a site
        """
        pagination = pagination_query(first=first, after=after, filter=filter, sort_by=sort_by)
        response = self._client.get("{}/v1/stacks/{}/delivery-domains".format(self.base_api, self._parent_id),
                                    params=pagination)
        response.raise_for_status()
        items = [self.loaddict(item) for item in response.json()["results"]]
        pageinfo = PageInfo(**response.json()["pageInfo"])

        return {"results": items, "pageinfo": pageinfo}