# Contributing Guide

## Commit Message Convention

Use this format:

<type>(phaseX/<scope>): <short summary>

### Types
- feat: new feature
- fix: bug fix
- docs: documentation changes
- config: configuration changes
- sec: security improvements/hardening
- test: add/update tests
- refactor: restructure without behavior change
- chore: housekeeping (deps, cleanup, repo setup)

### Examples
- chore(phase0): initialize project structure
- feat(phase0/auth): add login endpoint + event logging
- fix(phase1/docker): resolve container startup issue
- sec(phase2/rbac): add least-privilege service accounts
- feat(phase3/tf): provision network + kubernetes cluster
- feat(phase4/alerts): alert on brute-force attempts

## Branching Strategy

Work in branches per phase:
- phase0-security-app
- phase1-dockerize
- phase2-k8s-deploy
- phase3-terraform
- phase4-secops-observability
