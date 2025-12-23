<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None renamed, but principles added/updated based on user input
Added sections: Technology Stack, Constraints, Success Criteria sections
Removed sections: None
Templates requiring updates:
- ✅ plan-template.md - updated Constitution Check section to reflect new principles
- ✅ spec-template.md - no changes needed
- ✅ tasks-template.md - no changes needed
Follow-up TODOs: None
-->

# Todo Application Constitution

## Core Principles

### Spec-First Workflow (NON-NEGOTIABLE)
No manual coding—Claude Code generates all implementations. Clear, documented code following project conventions. Every feature must have a validated spec before implementation begins.
<!-- Rationale: Ensures predictable, reproducible development outcomes and maintains quality standards -->

### Incremental Complexity
Development follows structured progression: console → web → chatbot → Kubernetes → cloud. Each phase builds on the previous with clear deliverables and validation checkpoints.
<!-- Rationale: Reduces risk and enables iterative value delivery -->

### Clean Code Standards
Clean, well-documented Python (backend) and TypeScript (frontend). No hardcoded secrets—all environment variables. User data isolation at database and API levels. Comprehensive error handling and validation.
<!-- Rationale: Maintains maintainability, security, and scalability across the codebase -->

### Technology Stack Adherence
Strict adherence to defined technology stack per phase: Phase I: Python 3.13+, Claude Code, Spec-Kit Plus; Phase II: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth; Phase III: OpenAI Agents SDK, MCP SDK, OpenAI ChatKit; Phase IV: Docker, Kubernetes, Minikube, Helm Charts; Phase V: Kafka, Dapr, Azure/GCP/Oracle Cloud.
<!-- Rationale: Ensures consistency, reduces cognitive load, and enables effective team collaboration -->

### Code Traceability
Every code file must reference Task IDs in comments. All implementations must be linked to specs via Task IDs. Reproducible setup with complete README instructions.
<!-- Rationale: Enables auditability, debugging, and maintenance of the development process -->

### Open Source Transparency
All code in public GitHub repository. No feature without a validated spec. Every implementation linked to spec via Task IDs. Working demos showing all features. Clean, deployable code in GitHub. Specs organized in `/specs` folder with CLAUDE.md guidance.
<!-- Rationale: Promotes accountability, collaboration, and quality assurance -->

## Technology Stack

### Phase I: Foundation
Python 3.13+, Claude Code, Spec-Kit Plus

### Phase II: Web Application
Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth

### Phase III: AI Integration
OpenAI Agents SDK, MCP SDK, OpenAI ChatKit

### Phase IV: Containerization
Docker, Kubernetes, Minikube, Helm Charts

### Phase V: Cloud Deployment
Kafka, Dapr, Azure/GCP/Oracle Cloud

## Development Constraints

- All code must be in public GitHub repository
- No feature development without validated spec
- Every code file must reference Task IDs in comments
- Reproducible setup with complete README instructions
- No deviations from specified tech stack
- No hardcoded secrets—all environment variables
- User data isolation at database and API levels

## Development Workflow

- Spec-first workflow using Spec-Kit Plus
- No manual coding—Claude Code generates all implementations
- Clear, documented code following project conventions
- Incremental complexity: console → web → chatbot → Kubernetes → cloud
- Every implementation linked to spec via Task IDs
- Specs organized in `/specs` folder with CLAUDE.md guidance

## Success Criteria

- All 5 phases completed on schedule
- Every implementation linked to spec via Task IDs
- Working demos showing all features
- Clean, deployable code in GitHub
- Specs organized in `/specs` folder with CLAUDE.md guidance

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and migration plan. All PRs/reviews must verify compliance. Complexity must be justified. Use CLAUDE.md for runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2025-12-21 | **Last Amended**: 2025-12-21