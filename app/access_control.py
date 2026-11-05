from app.models import PropertyManager, ScreeningReport, Property, Tenant

def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:

    tenant = next(
        (t for t in tenants if t.id == report.tenant_id),
        None
    )

    if tenant is None:
        return False

    property_record = next(
        (p for p in properties if p.id == tenant.property_id),
        None
    )

    if property_record is None:
        return False

    return actor.landlord_account_id == property_record.landlord_account_id