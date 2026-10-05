# Publication review

The project is functional; legal content is a draft. Do not set publication_ready until these items are resolved and draft-only sentences are rewritten.

- [ ] Confirm public brand, legal operator, contact email, effective date, and intended release markets.
- [ ] Select governing law and dispute terms with appropriate consumer-rights protections.
- [ ] Verify production SDK data categories and actual Firebase Analytics, Crashlytics, and Amplitude retention, deletion, and transfer arrangements.
- [ ] Verify the production Universal Input research fields, activation conditions, user disclosures/consent where required, user disable options, and accessible deletion procedure. Do not assume operator permission equals user consent.
- [ ] Verify analytical/recovery retention against the deployed research configuration, including queues and recovery copies.
- [ ] Verify cloud backup release support, contents, retention, deletion, and provider permissions. Current TrackLogs code includes iCloud and Google Drive backup, despite the earlier project overview.
- [ ] Confirm age/audience rules, support retention, and applicable legal processing grounds.
- [ ] Remove or replace every draft-only commitment and placeholder in content and configuration.
- [ ] Confirm product/store URLs and public product description.
- [ ] Verify local preview and production readiness build; enable Pages only after explicit GitHub publication authorization.

Implementation evidence used: TrackLogs docs/environments.md, docs/research/operations.md, openspec/specs/cloud-backup/spec.md, cloud-backup-experience/spec.md, universal-input-platform-models/spec.md, and current settings code (2026-10-05). Repository documentation is not proof of live provider settings.
