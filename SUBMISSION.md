# Submission
DevOps Engineer Assignment

**Candidate name:** Veeraj Panchal
**Email:** panchalveeraj12@gmail.com
**Date submitted:** 2026-05-24
**Hours spent (approximate):** 8 hours

## Deliverables checklist
[x] Part A: Terraform code under /terraform applies cleanly on LocalStack
[x] Part A: terraform validate and terraform fmt -check both pass
[x] Part B: Janitor script runs in --dry-run mode and produces report.json
[ ] Part B: GitHub Actions workflow runs green on a fresh PR
[x] Part B: --delete mode respects Protected=true tag
[x] Part C: DESIGN.md is present and within 2 pages
[x] Walkthrough video link below is accessible (unlisted is fine)

## Walkthrough video
Link : https://drive.google.com/drive/u/0/folders/1Hho5pX1mfcTSMPFX9JEmVRN51uhrGWMg

## Sample report
In the root directory after running the script.

## Known limitations
* Cost projections utilize static regional tier constants hardcoded into a constants module rather than calling the live AWS Pricing API web vectors dynamically.
* The reporting execution engine iterates through configuration arrays sequentially rather than utilizing true concurrent multi-region worker pools.

## AI usage disclosure
* **Tools Used:** Gemini Pro for architectural documentation layouts and resolving provider state mismatch errors; GitHub Copilot for accelerating repeatable configuration boilerplate blocks.
* **AI Error Correction:** Initial AI outputs suggested a flat, monolithic infrastructure file configuration that violated the structural modularity constraints; flagged this error via local compilation checks and refactored the network tier into a separate module.
* **Manual Implementation:** Hand-authored the core conditional evaluation logic within the Python script to cross-reference multi-key tag values and inspect attachment state signatures to ensure strict behavioral alignment with the grading requirements.