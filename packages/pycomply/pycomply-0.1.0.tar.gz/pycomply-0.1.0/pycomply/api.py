from requests import Session
from typing import List
import inspect


class Connection(Session):
    def __init__(self, api_url="https://api.complyadvantage.com", api_key=None):
        super().__init__()
        self.api_url = api_url
        self.headers.update({"Authorization": f"Token {api_key}"})

    def get_users(self) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#get-users

        :return:
        """
        response = self.get(f"{self.api_url}/users")
        response.raise_for_status()
        return response.json()["content"]["data"]

    def create_search(
        self,
        search_term: str = None,
        client_ref: str = None,
        search_profile: str = None,
        fuzziness: float = 0.5,
        offset: int = 0,
        limit: int = 100,
        filters: dict = None,
        tags: dict = None,
        share_url: int = 0,
        country_codes: str = None,
        exact_match: bool = False,
    ) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#post-searches

        :param search_term: (required, max 255 characters) A string representing the name of the entity or an Object
        :param client_ref: (optional) Your reference for this person/entity for which you are searching. Used for tracking searches and auto-whitelisting recurring results
        :param search_profile: (optional) The slug of any of your previously created search profiles, which can be found in the main platform UI for search profiles
        :param fuzziness: (optional) Determines how closely the returned results must match the supplied name. Overridden by exact_match
        :param offset: (optional) Match results from the database, starting from the offset value
        :param limit: (optional) Match results from the database, taking up to this many matches each search
        :param filters: (optional) Specify filters within the search to narrow down the results. These are specified below, and are all optional
        :param tags: (optional) Object of name => value pairs (name must be string), must be existing tags
        :param share_url: (optional) Include a shareable URL to access search publicly
        :param country_codes: (optional) Array of ISO 3166-1 alpha-2 strings. Results are filtered by the entity nationality or country of residence
        :param exact_match: (optional) Exact match disables all standard and optional matching behaviours (Honorifics, affixes, initials, glued name, name variation, equivalent names, extra words in entity,...) 0% fuzziness disables 1 letter typo matching but keeps all other matching behaviours (standard and optional)
        :return:
        """
        pass

    def get_searches(
        self,
        search_term: str = None,
        submitted_term: str = None,
        assignee_id: int = None,
        client_ref: str = None,
        searcher_id: int = None,
        risk_level: str = None,
        created_at_from: str = None,
        created_at_to: str = None,
        sort_by: str = "id",
        sort_dir: str = "DESC",
        per_page: int = 100,
        page: int = 1,
        tags: str = None,
        monitored: str = None,
    ) -> list:
        """
        https://docs.complyadvantage.com/api-docs/#get-searches

        :param search_term: Searches that match search term (3 characters min)
        :param submitted_term: Show searches where the term is unsanitised and includes symbols and punctuation marks
        :param assignee_id: Show searches assigned to a specific user
        :param client_ref:
        :param searcher_id: Show searches performed by a specific user
        :param risk_level: Show searches where the risk level is one of the specified options: ('low', 'medium', 'high', 'unknown'). Use commas to separate multiple options, eg &risk_level=medium,high
        :param created_at_from: Searches made from date (yyyy-mm-dd)
        :param created_at_to: Searches made to date (yyyy-mm-dd)
        :param sort_by: One of 'id', 'created_at', 'updated_at', 'assignee_id', 'searcher_id'
        :param sort_dir: One of 'ASC, 'DESC'
        :param per_page: Number of searches to return per "page" (integer, max 100)
        :param page: Which page to fetch (integer)
        :param tags: Searches registered against given tags, comma separated represented as 'name:value', eg 'internal_ref:1234' or internal_ref:1234,t_type:custom'
        :param monitored: Searches with a specific monitored status, eg. suspended for suspended searches, un-suspended for actively monitored searches and false for searches which are not monitored
        :return:
        """
        argspec = inspect.getargvalues(inspect.currentframe())
        search_params = {
            k: v for (k, v) in argspec.locals.items() if v is not None and k != "self"
        }
        response = self.get(f"{self.api_url}/searches", params=search_params)
        response.raise_for_status()
        return response.json()["content"]["data"]

    def get_search(self, search_id: str = None, share_url: int = 0) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#get-searches-id

        :param search_id: Either the numeric search ID, or the search REF
        :param share_url: 1 or 0 - include a shareable URL in response.
        :return:
        """
        response = self.get(
            f"{self.api_url}/searches/{search_id}", params={share_url: share_url}
        )
        response.raise_for_status()
        return response.json()["content"]["data"]

    def get_search_certificate(self, search_id: str = None):
        """
        https://docs.complyadvantage.com/api-docs/#get-searches-id-certificate

        :param search_id: Either the numeric search ID, or the search REF
        :return:
        """
        response = self.get(f"{self.api_url}/searches/{search_id}/certificate")
        response.raise_for_status()
        return response.content

    def get_search_details(self, search_id: str = None, share_url: int = 0) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#get-searches-id-details

        :param search_id: Either the numeric search ID, or the search REF
        :param share_url: 1 or 0 - include a shareable URL in response.
        :return:
        """
        response = self.get(
            f"{self.api_url}/searches/{search_id}/details",
            params={share_url: share_url},
        )
        response.raise_for_status()
        return response.json()["content"]["data"]

    def update_search(
        self,
        search_id: str = None,
        match_status: str = None,
        risk_level: str = None,
        assignee_id: int = None,
        tags: dict = None,
    ):
        """
        https://docs.complyadvantage.com/api-docs/#patch-searches-id

        :param search_id: Either the numeric search ID, or the search REF
        :param match_status: One of 'unknown', 'no_match', 'potential_match', 'false_positive', 'true_positive', 'true_positive_approve', 'true_positive_reject'
        :param risk_level:One of 'low', 'medium', 'high', 'unknown'
        :param assignee_id: The ID of the user to whom the case should be assigned
        :param tags: Object of name => value pairs ( name must be string ), must be existing tags
        :return:
        """
        argspec = inspect.getargvalues(inspect.currentframe())
        request_data = {
            k: v
            for (k, v) in argspec.locals.items()
            if v is not None and k in ["self", "search_id"]
        }
        response = self.patch(
            f"{self.api_url}/searches/{search_id}",
            data=request_data,
        )
        response.raise_for_status()
        return response.json()["content"]["data"]

    def update_search_entities(
        self,
        search_id: str = None,
        entities: List[str] = None,
        match_status: str = None,
        risk_level: str = None,
        is_whitelisted: bool = None,
    ):
        """
        https://docs.complyadvantage.com/api-docs/#patch-searches-id-entities

        :param search_id: Either the numeric search ID, or the search REF
        :param entities: Array of entity ids to be updated (list of strings)
        :param match_status: One of 'no_match', 'false_positive', 'potential_match', 'true_positive','unknown'
        :param risk_level: One of 'low', 'medium', 'high', 'unknown'
        :param is_whitelisted: true or false
        :return:
        """
        argspec = inspect.getargvalues(inspect.currentframe())
        request_data = {
            k: v
            for (k, v) in argspec.locals.items()
            if v is not None and k in ["self", "search_id"]
        }
        response = self.patch(
            f"{self.api_url}/searches/{search_id}/entities",
            data=request_data,
        )
        response.raise_for_status()
        return response.json()["content"]["data"]

    def get_monitors(self, search_id: str = None) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#get-searches-id-monitors

        :param search_id: Either the numeric search ID, or the search REF
        """
        response = self.get(f"{self.api_url}/searches/{search_id}/monitors")
        response.raise_for_status()
        return response.json()["content"]

    def update_monitors(
        self, search_id: str = None, is_monitored: bool = None, monitored_by: int = None
    ) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#patch-searches-id-monitors

        :param search_id: Either the numeric search ID, or the search REF
        :param is_monitored: Start on true and stop on false. For monitored searches, the original search will be updated with the latest results from monitor runs.
        :param monitored_by: (optional) The ID of the user who will start/stop monitoring (please note if monitored_by is not provided all users will be affected )
        """
        argspec = inspect.getargvalues(inspect.currentframe())
        request_data = {
            k: v
            for (k, v) in argspec.locals.items()
            if v is not None and k in ["self", "search_id"]
        }
        response = self.patch(
            f"{self.api_url}/searches/{search_id}/monitors",
            data=request_data,
        )
        response.raise_for_status()
        return response.json()["content"]

    def get_monitor_updates(self, search_id: str = None, date: str = None) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#get-searches-id-monitor-differences

        :param search_id: Either the numeric search ID, or the search REF
        :param date: (optional) The reference date format: yyyy-mm-dd if missing, the current day will be used
        :return:
        """
        argspec = inspect.getargvalues(inspect.currentframe())
        search_params = {
            k: v
            for (k, v) in argspec.locals.items()
            if v is not None and k in ["self", "search_id"]
        }
        response = self.get(
            f"{self.api_url}/searches/{search_id}/monitors/differences",
            params=search_params,
        )
        response.raise_for_status()
        return response.json()["content"]

    def get_comment(self, search_id: str = None) -> dict:
        """
        https://docs.complyadvantage.com/api-docs/#get-searches-id-comments

        :param search_id: Either the numeric search ID, or the search REF
        :return:
        """
        response = self.get(
            f"{self.api_url}/searches/{search_id}/comments",
        )
        response.raise_for_status()
        return response.json()["content"]

    def create_comment(
        self, search_id: str = None, comment: str = None, entity_id: str = None
    ) -> bool:
        """
        https://docs.complyadvantage.com/api-docs/#post-searches-id-comments

        :param search_id: Either the numeric search ID, or the search REF
        :param comment: The comment that will be added
        :param entity_id: The entity id (required for adding comment on entity)
        """
        argspec = inspect.getargvalues(inspect.currentframe())
        request_data = {
            k: v
            for (k, v) in argspec.locals.items()
            if v is not None and k in ["self", "search_id"]
        }
        response = self.post(
            f"{self.api_url}/searches/{search_id}/comments", data=request_data
        )
        response.raise_for_status()

        if response.status_code == 204:
            return True

        return False
