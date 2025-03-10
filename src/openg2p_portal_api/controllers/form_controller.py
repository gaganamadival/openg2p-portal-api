# from typing import Annotated

from openg2p_fastapi_common.controller import BaseController

from ..config import Settings
from ..models.form import ProgramForm, ProgramRegistrantInfo
from ..services.form_service import FormService

_config = Settings.get_config()


class FormController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._form_service = FormService.get_component()

        self.router.add_api_route(
            "/form/{programid}",
            self.get_program_form,
            responses={200: {"model": ProgramForm}},
            methods=["GET"],
        )

        self.router.add_api_route(
            "/form/{programid}",
            self.create_new_form_draft,
            responses={200: {"model": ProgramForm}},
            methods=["POST"],
        )

        self.router.add_api_route(
            "/form/{programid}",
            self.update_form_draft,
            responses={200: {"model": ProgramForm}},
            methods=["PUT"],
        )

        self.router.add_api_route(
            "/form/{programid}/submit",
            self.submit_form,
            responses={200: {"model": ProgramForm}},
            methods=["POST"],
        )

    @property
    def form_service(self):
        if not self._form_service:
            self._form_service = FormService.get_component()
        return self._form_service

    async def get_program_form(self, programid: int):
        return await self.form_service.get_program_form(programid)

    async def update_form_draft(
        self, programid: int, programreginfo: ProgramRegistrantInfo
    ):
        registrant_id = 42

        return await self.form_service.create_form_draft(
            programid, programreginfo, registrant_id
        )

    async def create_new_form_draft(
        self, programid: int, programreginfo: ProgramRegistrantInfo
    ):
        registrant_id = 42

        return await self.form_service.create_form_draft(
            programid, programreginfo, registrant_id
        )

    async def submit_form(self, programid: int, programreginfo: ProgramRegistrantInfo):
        registrant_id = 42

        return await self.form_service.submit_application_form(
            programid, programreginfo, registrant_id
        )
