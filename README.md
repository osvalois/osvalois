# Oscar Valois

**Senior Generative AI Engineer — Agent Platforms, MCP & LLM Governance**
Querétaro, México · Remote (LATAM)

I build agent systems that run in production, and I measure whether they actually do
what their architecture claims.

---

### Focus

**Agent runtimes** — multi-agent orchestration with tool calling, structured outputs,
tool-failure handling, and human-in-the-loop approval bound to a plan hash and consumed once.

**Model Context Protocol** — building MCP servers and tools since 2025: an enterprise MCP
platform, an orchestration server, and agent integrations. Currently on protocol version
`2025-11-25`.

**Governance & traceability** — external policy decision point over Open Policy Agent,
runtime guardrails, execution provenance with HMAC-signed evidence anchored in a
transparency log, per-model token accounting and cost budgets.

**Retrieval** — RAG over vector stores, encrypted memory, per-subject erasure (GDPR Art. 17).

---

### Production track record

**Federal public-sector trade platform** — 17 microservices, ~200k LOC. Measured at
297/300 pods healthy, 199 concurrent PostgreSQL connections, all APIs and VIPs returning
HTTP 200.

**Financial services cloud platform** — 50+ Azure resources across 25 Terraform modules;
SQL Server, Redis at 99.9% SLA, PostgreSQL. Delivered on the committed go-live date.

**Logistics platform** — development to production in three months.

*Client names withheld. Supporting documentation available on request.*

---

### Measured, not asserted

I wrote the conformance instrument that audits my own architecture: **31 executable
invariants**, including a class not described in the prior fitness-function literature —
checks that *count authorities* rather than verify dependencies.

I ran it for two months across 78 components and published the result, **including the
negative one**: with the instrument live and the gate enforcing, four structural violations
did not move.

> *Measured Architectural Divergence: Executable Conformance in an Agent System* —
> technical report, instrument and dataset. **Coming 2026-09-15.**

---

### Stack

`TypeScript` `Rust` `Python` `Java` `Kotlin` · `PostgreSQL` `Qdrant` `Redis` ·
`Kubernetes` `Terraform` `Azure` `AWS` · `OPA` `MCP` `OpenTelemetry` `OAuth2/OIDC`

---

[LinkedIn](https://linkedin.com/in/oscar-valois-331892287) · osvaloismtz@gmail.com
