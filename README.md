# HAPIS Engine — Public Preview

Beta-tester guide for the **HAPIS Engine B2B API** — a precision RF engineering tool for
**High-Altitude Platform Systems (HAPS)** link-budget and coverage analysis, grounded in
ITU-R and 3GPP reference models.

> This repository contains **documentation and the issue tracker only — no engine source.**
> The product ships as a signed container image (below).

> **Status: preview / beta.** The engine carries the code label **v1.0.0** and is in active
> development; it is not yet publicly released. Endpoints and outputs may change between
> builds. Intended for **engineering evaluation and academic research** — not for
> operational or safety-critical use.

---

## What's in the preview

The preview ships as a single signed container image of the B2B API:

- **Propagation** — ITU-R P.525 (FSPL), P.676 (atmospheric gases), P.838 (rain),
  P.840 (cloud/fog), P.2108 (clutter)
- **Link budget** — RSSI, link margin, atmospheric losses, and coverage grids
- **Decision-grade reports** — circular RSSI / Link-Margin / SNR coverage maps and a
  Deployment Decision Summary, exported as PDF
- **NTN analysis** — 3GPP TR 38.811 / 38.821 / 38.822 (time-stepping, multi-beam,
  Doppler, handover, timing advance)

Bands of interest: **S (2 GHz), Ka (28 GHz), Q (38 GHz), V (47 GHz)**.

---

## Quick start

You need [Docker](https://docs.docker.com/get-docker/). The preview image is **public** —
no GitHub account or login required.

```bash
docker pull ghcr.io/hap-intel-systems/hapis-api:latest
docker run -p 8000:8000 ghcr.io/hap-intel-systems/hapis-api:latest
```

Then open:

- Interactive API docs — <http://localhost:8000/docs>
- Health check — <http://localhost:8000/health>

> The image is built for **linux/amd64**. On Apple Silicon it runs under Docker's built-in
> emulation (slower, but functional).

---

## Verify the image (optional, recommended)

Every image is signed keyless with [Sigstore `cosign`](https://docs.sigstore.dev/) and ships
with an SPDX SBOM. You can confirm it was built by our CI before running it:

```bash
# 1. Resolve the image digest
docker buildx imagetools inspect ghcr.io/hap-intel-systems/hapis-api:latest

# 2. Verify the signature against the digest from step 1
cosign verify ghcr.io/hap-intel-systems/hapis-api@<digest> \
    --certificate-identity-regexp 'https://github.com/HAP-Intel-Systems/.*' \
    --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

The SBOM attestation can be fetched separately with `cosign download attestation`.

---

## A first request

With the container running, the interactive docs at `/docs` let you try every endpoint in the
browser. Combined link-budget and coverage routes live under `/v1/link-budgets/*` (including
`/v1/link-budgets/report` and `/v1/link-budgets/constellation/report` for PDF reports).
Authentication uses an API key — see the in-container `/docs` for the current schema.

---

## Reporting issues & feedback

This is what the preview is for — please tell us what breaks or what's missing:

- **[Open an issue](../../issues/new/choose)** using the Bug report or Feedback template.
- Or email **<contact@hapintel.com>** for private, security, or commercial inquiries.

Please **do not** include API keys, tokens, or other secrets in issues.

---

## Links

- Website — <https://hapintel.com>
- Documentation — <https://hapintel.com/docs>
- Validation methodology white paper — <https://hapintel.com/papers/validation-methodology>

---

## Disclaimer

HAPIS Engine is an RF engineering and research tool. Results are model-based estimates for
planning and academic purposes and carry no warranty of fitness for any particular use. See
the [Terms of Service](https://hapintel.com/terms) for the full engineering disclaimer.

© 2026 HAP Intel Systems. The HAPIS Engine is proprietary software; this repository documents
a preview build provided for evaluation.
