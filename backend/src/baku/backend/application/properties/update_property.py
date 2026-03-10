"""Use case: UpdateProperty — update editable fields of a property — F-0003 US3.

Raises:
    PropertyNotFound — property_id does not exist or is soft-deleted.
    PropertyValidationError — name is blank if provided.
    PropertyDerivedFieldNotEditable — attempt to set a derived field directly.
"""

from __future__ import annotations

import logging

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.application.properties.contracts import (
    PropertyResult,
    UpdatePropertyCommand,
)
from baku.backend.application.properties.create_property import _to_result
from baku.backend.domain.properties.errors import (
    PropertyNotFound,
    PropertyValidationError,
)
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)

logger = logging.getLogger(__name__)


def update_property(
    cmd: UpdatePropertyCommand,
    property_repo: PropertyRepository,
    ownership_repo: OwnershipRepository,
    uow: PropertyUnitOfWorkPort,
) -> PropertyResult:
    property_ = property_repo.find_by_id(cmd.property_id)
    if property_ is None:
        raise PropertyNotFound()

    if cmd.name is not None:
        if not cmd.name.strip():
            raise PropertyValidationError("name must not be blank.")
        property_.name = cmd.name

    if cmd.type is not None:
        property_.type = cmd.type
    if cmd.description is not None:
        property_.description = cmd.description
    if cmd.address is not None:
        property_.address = cmd.address
    if cmd.city is not None:
        property_.city = cmd.city
    if cmd.postal_code is not None:
        property_.postal_code = cmd.postal_code
    if cmd.province is not None:
        property_.province = cmd.province
    if cmd.country is not None:
        property_.country = cmd.country
    if cmd.cadastral_reference is not None:
        property_.cadastral_reference = cmd.cadastral_reference
    if cmd.cadastral_value is not None:
        property_.cadastral_value = cmd.cadastral_value
    if cmd.cadastral_land_value is not None:
        property_.cadastral_land_value = cmd.cadastral_land_value
    if cmd.cadastral_value_revised is not None:
        property_.cadastral_value_revised = cmd.cadastral_value_revised
    if cmd.acquisition_date is not None:
        property_.acquisition_date = cmd.acquisition_date
    if cmd.acquisition_type is not None:
        property_.acquisition_type = cmd.acquisition_type
    if cmd.transfer_date is not None:
        property_.transfer_date = cmd.transfer_date
    if cmd.transfer_type is not None:
        property_.transfer_type = cmd.transfer_type
    if cmd.fiscal_nature is not None:
        property_.fiscal_nature = cmd.fiscal_nature
    if cmd.fiscal_situation is not None:
        property_.fiscal_situation = cmd.fiscal_situation

    now = utcnow()
    property_.updated_at = now
    property_.updated_by = cmd.updated_by

    # Re-validate derived field invariant after potential cadastral updates
    try:
        property_.__post_init__()
    except ValueError as exc:
        raise PropertyValidationError(str(exc)) from exc

    property_repo.save(property_)
    uow.commit()

    logger.info(
        "update_property_completed",
        extra={
            "operation": "update_property",
            "property_id": property_.property_id,
        },
    )

    ownerships = ownership_repo.list_active_by_property(property_.property_id)
    return _to_result(property_, ownerships)
