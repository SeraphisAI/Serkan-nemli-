# Seraphis DNA (UCP-QH 1.0 Starter)

## 1) ASSUMPTIONS
See `docs/ASSUMPTIONS.md`.

## 2) ARCHITECTURE
Modular layout:
- `core/`: IoT ingest + summary
- `transport/`: FastAPI REST active, WS/MQTT stubs
- `quantum/`: local simulator + provider adapter interface
- `security/`: API key auth, PQC-ready interfaces
- `privacy/`: data classification + masking
- `policy/`: versioned policies + evaluator + audit events
- `telemetry/`: event model + optimization hints, default off
- `migrations/`: init and rollback scripts
- `update/`: check/apply endpoints with signature verification + rollback snapshot

## 3) CONTRACTS
OpenAPI 3.1 contract: `contracts/openapi.yaml`.

## 4) PROJECT TREE
See repository structure; top-level folders align with UCP-QH required modules.

## 5) CODE
Code is under `src/` with module boundaries above.

## 6) RUN & TEST
```bash
make install
make test
make dev
```
Or Docker:
```bash
docker compose up --build
```

## 7) MIGRATION PACK
- Apply: `make migrate`
- Rollback: `./migrations/rollback.sh`
- Strategy: each update stores prior VERSION in `migrations/rollback/`.

## 8) POLICY PACK
- Policy file: `policy/policies.json`
- Enforced actions: `ingest`, `update_apply`
- Audit events emitted as telemetry `policy` records.

## 9) TELEMETRY
- Event types: `request`, `response`, `error`, `latency`, `throughput`, `policy`, `anomaly`
- Default off (`SERAPHIS_TELEMETRY_ENABLED=false`)
- Improvement hints endpoint: `GET /telemetry/hints`

## 10) SECURITY & PRIVACY NOTES
- Secrets via env vars (`SERAPHIS_API_KEY`, `SERAPHIS_UPDATE_HMAC_KEY`)
- Update apply is HITL-compatible (`approver` field) + signature-verified + rollback-ready.
- Sensitive fields masked before telemetry logging.
