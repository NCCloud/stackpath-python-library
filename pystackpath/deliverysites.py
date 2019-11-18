from .util import BaseObject, PageInfo, pagination_query


class DeliverySites(BaseObject):
    base_api = "/delivery"

    def index(self, first="", after="", filter="", sort_by=""):
        pagination = pagination_query(first=first, after=after, filter=filter, sort_by=sort_by)
        response = self._client.get("{}/v1/stacks/{}/sites".format(self.base_api, self._parent_id), params=pagination)
        response.raise_for_status()
        items = []
        for item in response.json()["results"]:
            items.append(self.loaddict(item))
        pageinfo = PageInfo(**response.json()["pageInfo"])

        return {"results": items, "pageinfo": pageinfo}

    def get(self, site_id):
        response = self._client.get("{}/v1/stacks/{}/sites/{}".format(self.base_api, self._parent_id, site_id))
        response.raise_for_status()
        return self.loaddict(response.json()["site"])

    def create(self, **payload):
        """
        Create a new site
        :param payload: dict according to https://stackpath.dev/reference/sites#createsite-1
        :return: dict with created site
        String	id         A CDN site's unique identifier.
        String	stackId    The ID of the stack to which a CDN site belongs.
        String	label      A CDN site's name. Site names correspond to their fully-qualified domain name.
        String	status     A CDN site's internal state. Site status is controlled by StackPath as sites
                           are provisioned and managed by StackPath's accounting and security teams.
        String	createdAt  The date that a CDN site was created.
        String	updatedAt  The date that a CDN site was last updated.
        List	features   A CDN site's associated features.
                           Features control how StackPath provisions and configures a site.
        """
        response = self._client.post(
            "{}/v1/stacks/{}/sites".format(self.base_api, self._parent_id),
            json=payload
        )
        response.raise_for_status()
        return self.loaddict(response.json()["site"])

    def delete(self):
        """
        Delete a CDN site
        :return: a stackpath site object with the deleted cdn site
        """
        response = self._client.delete("{}/v1/stacks/{}/sites/{}".format(self.base_api, self._parent_id, self.id))
        response.raise_for_status()
        return self

    def disable(self):
        """
        Disable a CDN site
        :return: a stackpath site object with the disabled cdn site
        """
        response = self._client.post("{}/v1/stacks/{}/sites/{}/disable".format(self.base_api, self._parent_id, self.id))
        response.raise_for_status()
        return self

    def enable(self):
        """
        Enable a CDN site
        :return: a stackpath site object with the enabled cdn site
        """
        response = self._client.post("{}/v1/stacks/{}/sites/{}/enable".format(self.base_api, self._parent_id, self.id))
        response.raise_for_status()
        return self
