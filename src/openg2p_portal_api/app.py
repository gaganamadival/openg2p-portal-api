# ruff: noqa: E402
import asyncio

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer

from .controllers.discovery_controller import DiscoveryController
from .controllers.form_controller import FormController
from .controllers.program_controller import ProgramController
from .models.orm.program_registrant_info_orm import ProgramRegistrantInfoDraftORM
from .services.form_service import FormService
from .services.membership_service import MembershipService
from .services.program_service import ProgramService


class Initializer(Initializer):
    def initialize(self, **kwargs):
        super().initialize()
        # Initialize all Services, Controllers, any utils here.
        MembershipService()
        FormService()
        ProgramService()
        DiscoveryController().post_init()
        ProgramController().post_init()
        FormController().post_init()

    def migrate_database(self, args):
        super().migrate_database(args)

        async def migrate():
            await ProgramRegistrantInfoDraftORM.create_migrate()

        asyncio.run(migrate())
