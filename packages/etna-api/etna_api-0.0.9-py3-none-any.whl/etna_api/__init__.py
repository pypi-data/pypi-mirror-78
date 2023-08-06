#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from typing import Dict, List, Tuple
from urllib3.util.retry import Retry

AUTHENTICATION_URL = "https://auth.etna-alternance.net"
MODULES_API = "https://modules-api.etna-alternance.net"
TICKETS_API = "https://tickets.etna-alternance.net/api"


class EtnaSession:
    def _perform_request(self, *, method: str, url: str, json=None, raw=False):
        response = self._session.request(
            method=method,
            url=url,
            json=json,
            cookies=self._cookies
        )
        response.raise_for_status()
        if raw:
            return response
        return response.json()

    def _authenticate(self, username: str, password: str):
        response = self._perform_request(
            method="POST",
            url=f"{AUTHENTICATION_URL}/login",
            json={
                "login": username,
                "password": password,
            },
            raw=True
        )
        return response.cookies.get_dict()

    @staticmethod
    def _create_session(request_retries: int, retry_on_statuses: Tuple[int, ...] = None, backoff_factor: float = None):
        retry_on_statuses = retry_on_statuses or (500, 502, 504)
        backoff_factor = backoff_factor or 0.4
        session = requests.Session()
        retry = Retry(
            total=request_retries,
            read=request_retries,
            connect=request_retries,
            backoff_factor=backoff_factor,
            status_forcelist=retry_on_statuses if request_retries > 1 else None,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def __init__(
            self,
            *,
            username: str,
            password: str,
            request_retries: int = None,
            retry_on_statuses: Tuple[int, ...] = None,
            backoff_factor: float = None
    ):
        """
        Create a Session object by logging-in

        :param username:                the username to use to login
        :param password:                the password to use to login
        :param request_retries:         the number of times requests should be retried on failure
        :param retry_on_statuses:       the HTTP statuses for which retries should be performed
        :param backoff_factor:          the factor used to determine how much time should be waited between retries
        """
        self._username = username
        if request_retries is None:
            self._session = requests
        else:
            self._session = self._create_session(request_retries, retry_on_statuses, backoff_factor)
        self._cookies = {}
        self._cookies = self._authenticate(username, password)

    def __repr__(self):
        return f"etna_api.Session(username={self._username}, cookies={self._cookies})"

    def identity(self):
        """
        Query the API for the user's information

        :return:                        a JSON object containing user information
        """
        return self._perform_request(
            method="GET",
            url=f"{AUTHENTICATION_URL}/identity",
        )

    def logas(self, login: str):
        identity = self.identity()
        identity["login"] = login
        result = self._perform_request(
            method="POST",
            url=f"{AUTHENTICATION_URL}/identity",
            json=identity,
            raw=True
        )
        self._cookies = result.cookies.get_dict()
        return result.json()

    def get_current_modules(self) -> List:
        """
        Get a list of all the ongoing modules

        :return:                        a list containing information about each ongoing module
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/uvs",
        )

    def create_module(
            self,
            *
            name: str,
            version: int = 1,
            duration: int,
            long_name: str,
            description: str,
            average: int,
            equivalence: str,
            nb_marks: int,
            published: int,
            mandatory: bool,
    ):
        raise NotImplementedError()

    def update_module(
            self,
            *
            name: str,
            version: int = 1,
            duration: int,
            long_name: str,
            description: str,
            average: int,
            equivalence: str,
            nb_marks: int,
            published: int,
            mandatory: bool,
    ):
        raise NotImplementedError()

    def get_module_by_id(self, module_id: int):
        """
        Retrieve module information given a module ID

        :param module_id:               the module ID

        :return:                        a JSON object describing the module
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}"
        )

    def get_module_activities(self, module_id: int) -> List:
        """
        Get a list of all the activities in a module

        :param module_id:               the module ID

        :return:                        a list containing information about each activity in the module
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities"
        )

    def get_module_teachers(self, module_id: int) -> List:
        """
        Get a list of all the teachers in a module

        :param module_id:               the module ID

        :return:                        a list containing information about each teacher in the module
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/profs"
        )

    def get_activity_by_id(self, module_id: int, activity_id: int):
        """
        Get the information associated with a single activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :return:                        the information associated with the given activity
        """

        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}"
        )

    def get_current_student_activities(self, student_login: str):
        """
        Get a given student's current activities

        :param student_login:           the login of the student whose activities are to be retrieved

        :return:                        a list containing information about each ongoing activity
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/students/{student_login}/currentactivities",
        )

    def get_current_student_modules(self, student_login: str):
        """
        Get a given student's current modules

        :param student_login:           the login of the student whose modules are to be retrieved

        :return:                        a list containing information about each ongoing module
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/students/{student_login}/search"
        )

    def delete_activity(self, activity_id: int):
        raise NotImplementedError()  # The documentation doesn't show any successful example of deleting an activity

    def get_activity_stages(self, module_id: int, activity_id: int) -> List:
        """
        Get a list of stages for the quest

        :return:                        a list of objects containing information about each stage
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/stages"
        )

    def get_stage_requests(self, module_id: int, activity_id: int, group_id: int, stage_name: str) -> List:
        """
        Get a list of validation requests and their status for a given stage and group ID

        :param module_id:               the module ID
        :param actvity_id:              the activity ID
        :param group_id:                the group ID
        :param stage_name:              the name of the stage (in the URL)

        :return:                        a list of objects containing information about each validation request
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/stages/{stage_name}/groups/{group_id}/stage_requests"
        )

    def get_activity_marks(self, module_id: int, activity_id: int) -> List:
        """
        Get the marks for a given activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :return:                        a list of objects representing the sessions of the activity
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/marks_list",
        )

    def add_activity(self, module_id: int, activity_info):
        """
        Add an activity to a given module

        :param module_id:               the module ID
        :param activity_info:           a dictionary containing the activity metadata

        :return:                        a dictionary representing the newly-created activity
        """
        return self._perform_request(
            method="POST",
            url=f"{MODULES_API}/{module_id}/activities",
            json=activity_info
        )

    def get_activity_files_list(self, module_id: int, activity_id: int) -> List:
        """
        Get a list of all the files in a given activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :return:                        a list of objects, each containing metadata about a file
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/files"
        )

    def get_activity_stage_files_list(self, module_id: int, activity_id: int, stage: str) -> List:
        """
        Get a list of all the files in a given stage of an activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param stage:                   the name of the stage

        :return:                        a list of objects, each containing metadata about a file
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/stage/{stage}/files"
        )

    def download_file_from_activity(self, module_id: int, activity_id: int, path: str) -> bytes:
        """
        Download a file from the activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param path:                    the path to the file to download

        :return:                        the requested file contents
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/download/{path}",
            raw=True
        ).content

    def delete_file_from_activity(self, module_id: int, activity_id: int, path: str):
        """
        Delete a file from the activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param path:                    the path to the file to delete

        :return:                        a string containing the word "Deleted"
        """
        return self._perform_request(
            method="DELETE",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/{path}",
        )

    def get_groups_for_activity(self, module_id: int, activity_id: int) -> List:
        """
        Get a list of the registered groups for a given activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :return:                        a list of objects, each containing information about a group
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/groups"
        )

    def get_unregistered_students_for_activity(self, module_id: int, activity_id: int) -> List:
        """
        Get a list of the unregistered students for a given activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :return:                        a list of objects, each containing information about an unregistered student
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/unregistered"
        )

    def get_group_by_id(self, module_id: int, activity_id: int, group_id: int):
        """
        Get a group's information given its ID

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param group_id:                the group ID

        :return:                        an dictionary describing the group
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/groups/{group_id}"
        )

    def get_group_marks(self, module_id: int, activity_id: int, group_id: int):
        """
        Get a group's marks given its ID

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param group_id:                the group ID

        :return:
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/checklist/group/{group_id}"
        )

    def update_marks(self, module_id: int, activity_id: int, group_id: int, data):
        """
        Update a group's marks

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param group_id:                the group ID
        :param data:                    the data to apply

        :return:
        """
        return self._perform_request(
            method="POST",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/checklist/group/{group_id}",
            json=data
        )

    def get_checklist_from_activity(self, module_id: int, activity_id: int):
        """
        Get the checklist for a given activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :return:                        a dictionary describing the checklist
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/checklist"
        )

    def add_checklist_to_activity(self, module_id: int, activity_id: int, data: dict):
        """
        Add a checklist to the given activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :param data:                    a dictionary describing the checklist
        """
        return self._perform_request(
            method="POST",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/checklist",
            json=data
        )

    def request_moulinette(self, module_id: int, activity_id: int, stage_name: str, dry_run: bool = False):
        """
        Request a moulinette on a given stage for every registered group

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param stage_name:              the name of the stage
        :param dry_run:                 whether the results should be private or sent to the student

        :return:                        a dictionary containing information about the moulinette jobs
        """
        return self._perform_request(
            method="POST",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/stages/{stage_name}/moulinette",
            json={"dry_run": dry_run}
        )

    def request_moulinette_for_group(
            self,
            module_id: int,
            activity_id: int,
            stage_name: str,
            group_id: int,
            dry_run: bool = False
    ):
        """
        Request a moulinette on a given stage of the activity, for a given group

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param stage_name:              the name of the stage
        :param group_id:                the ID of the group
        :param dry_run:                 whether the results should be private or sent to the student

        :return:                        a dictionary containing information about the moulinette jobs
        """
        return self._perform_request(
            method="POST",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/stages/{stage_name}/moulinette",
            json={"dry_run": dry_run, "group_id": group_id}
        )

    def get_circles(self, module_id: int, activity_id: int):
        """
        Retrieve circles information for the activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID

        :return:                        a list containing the names of the circles
        """
        return self._perform_request(
            method="GET",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/conversations/circles"
        )

    def add_conversation_for_activity(self, module_id: int, activity_id: int, data):
        """
        Add a new conversation for the given activity

        :param module_id:               the module ID
        :param activity_id:             the activity ID
        :param data:                    the data to add
        """

        return self._perform_request(
            method="POST",
            url=f"{MODULES_API}/{module_id}/activities/{activity_id}/conversations",
            json=data
        )

    def get_todo_by_id(self, ticket_id: int):
        """
        Get information about a ticket given its ID

        :param ticket_id:               the ticket ID

        :return:                        a dictionary containing the ticket information
        """
        return self._perform_request(
            method="GET",
            url=f"{TICKETS_API}/todos/{ticket_id}.json"
        )["data"]

    def update_todo(self, ticket_id: int, todo):
        """
        Update an existing ticket

        :param ticket_id:               the ticket ID
        :param todo:                    a dictionary containing the information to set for the ticket

        :return:                        a dictionary containing the ticket information after the update
        """
        return self._perform_request(
            method="PUT",
            url=f"{TICKETS_API}/todos/{ticket_id}.json",
            json=todo
        )["data"]

    def create_todo(self, todo):
        """
        Create a new ticket

        :param todo:                    a dictionary containing the information for the ticket to be created

        :return:                        a dictionary containing the newly-created ticket information
        """
        return self._perform_request(
            method="POST",
            url=f"{TICKETS_API}/todos.json",
            json=todo
        )["data"]

    def get_todos(self, filters: Dict = None, size: int = None):
        url = f"{TICKETS_API}/search.json?from=0"
        if filters is not None:
            filters = "".join(f"+{key}:{value}" for key, value in filters.items())
            url += f"&q={filters}"
        if size is not None:
            url += f"&size={size}"
        return self._perform_request(
            method="GET",
            url=url
        )
