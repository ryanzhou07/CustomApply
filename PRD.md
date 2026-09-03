# Lean PRD: CustomApply MVP (V1)

## 1. Product Vision
CustomApply is a browser side-panel companion that helps users complete job applications faster while staying authentic to their own experience and voice.

## 2. Why This Product
- Existing simplify-style experiences often gate stronger automation features behind premium tiers.
- This product is being built to provide a practical local-first alternative users can use without mandatory paid upgrades.
- The focus is to remake a reliable local version centered on user-owned data and grounded response generation.

## 3. V1 Scope (Must Have)
- ATS support: **Workday** and **Greenhouse** only.
- Local **Profile** for reusable application data.
- Local **Story Bank** for user-authored examples and resume-backed content.
- Local **Tracker** for application progress and records.
- Autofill and open-ended response support inside the browser flow.

## 4. Success Criteria
- Autofill completes at least **75%** of fillable application fields on supported platforms.
- The assistant produces strong, usable open-ended responses with minimal editing.

## 5. AI Grounding Rules
- Generated responses must use only:
  - user-provided story content
  - user resume content
- No invented claims or unsupported details.
- Every generated response must include citations to source story/resume content used.

## 6. Data & Storage Requirements
- Store all application-related data locally by default.
- Encrypt stored login details/credentials.
- No additional encryption requirement for other local data in V1.

## 7. Tracker Schema Requirements
Each tracked application entry must include:
- Company name
- Role/title
- Date applied
- Story-filled entries used in the submitted application

## 8. Out of Scope for V1
- ATS platforms beyond Workday and Greenhouse
- Non-local-first expansion features unless explicitly prioritized later
