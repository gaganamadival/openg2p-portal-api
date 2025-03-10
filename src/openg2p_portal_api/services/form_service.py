from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.service import BaseService
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..models.form import ProgramForm
from ..models.orm.program_orm import ProgramORM
from ..models.orm.program_registrant_info_orm import (
    ProgramRegistrantInfoDraftORM,
    ProgramRegistrantInfoORM,
)
from .membership_service import MembershipService


class FormService(BaseService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.membership_service = MembershipService.get_component()

    async def get_program_form(self, program_id: int):
        response_dict = {}

        res = await ProgramORM.get_program_form(program_id)
        if res:
            form = res.form
            if form:
                response_dict = {
                    "id": form.id,
                    "program_id": res.id,
                    "schema": form.schema,
                    "submission_data": None,
                    "program_name": res.name,
                    "program_description": res.description,
                }
            else:
                response_dict = {
                    "id": None,
                    "program_id": res.id,
                    "schema": None,
                    "submission_data": None,
                    "program_name": res.name,
                    "program_description": res.description,
                }
            return ProgramForm(**response_dict)
        else:
            # TODO: Add error handling
            pass

    async def create_form_draft(self, program_id: int, form_data, registrant_id: int):
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            check_if_draft_already_present = (
                await ProgramRegistrantInfoDraftORM.get_draft_reg_info_by_id(
                    program_id, registrant_id
                )
            )

            if check_if_draft_already_present is None:
                program_registrant_info = ProgramRegistrantInfoDraftORM(
                    program_id=program_id,
                    program_registrant_info=form_data.program_registrant_info,
                    registrant_id=registrant_id,
                )

                try:
                    session.add(program_registrant_info)

                    await session.commit()
                except IntegrityError:
                    return "Error: In creating the draft"

            else:
                check_if_draft_already_present.program_registrant_info = (
                    form_data.program_registrant_info
                )
                try:
                    await session.commit()
                except IntegrityError:
                    return "Error: In updating the draft."

        return "Successfully submitted the draft!!"

    async def submit_application_form(
        self, program_id: int, form_data, registrant_id: int
    ):
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            program_membership_id = await self.membership_service.check_and_create_mem(
                program_id, registrant_id
            )
            get_draft_reg_info = (
                await ProgramRegistrantInfoDraftORM.get_draft_reg_info_by_id(
                    program_id, registrant_id
                )
            )
            program_registrant_info = ProgramRegistrantInfoORM(
                program_id=program_id,
                program_membership_id=program_membership_id,
                program_registrant_info=form_data.program_registrant_info,
                state="active",
                registrant_id=registrant_id,
            )

            try:
                if get_draft_reg_info:
                    session.add(program_registrant_info)
                    await session.delete(get_draft_reg_info)
                else:
                    session.add(program_registrant_info)

                await session.commit()
            except IntegrityError:
                return "Error: Duplicate entry or integrity violation"

        return "Successfully applied into the program!!"
