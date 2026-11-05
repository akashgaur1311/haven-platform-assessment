# Design Notes

## B0 — Terraform resource identity
Used for_each with landlord account IDs as stable keys instead of count indexes. Added moved blocks to preserve existing resource addresses and avoid unnecessary bucket replacement.

## B1 — S3 lifecycle cost
Glacier Flexible Retrieval has a 90-day minimum storage duration. Deleting objects early can cause additional charges. Archival must respect the application's deletion requirements.

## B2 — Access control
A ScreeningReport belongs to a Tenant, which belongs to a Property. Access is controlled by comparing the Property's landlord_account_id with the PropertyManager's landlord_account_id. Missing records fail closed.

## Cost tagging
The required billing tag is landlord_account_id because LandlordAccount is the billing unit.

The cost-tag check examines created and updated resources, reports missing billing tags, and uses deterministic output to maintain idempotency.