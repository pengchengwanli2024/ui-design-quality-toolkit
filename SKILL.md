---
name: ui-design-quality
description: Use for interface design, UI renovation, refinement of generic AI-looking UI, or frontend quality optimization that combines product-specific design judgment, DESIGN.md references, modern browser guidance, and measured verification. Complements an independently installed Oil UI Pro skill; small edits use only the affected checks.
license: MIT
---

# UI Design Quality

This file owns task routing, call order and completion. References supply criteria for the current stage; reading one does not start another complete workflow. Follow the user's current request and applicable project constraints, including its brand, components, browser policy and required checks.

## One coordinator, one design owner

- Choose one coordinator for this task: this skill or another complete UI workflow such as app-ui-studio. Skills can coexist in the host; do not start two orchestration loops or uninstall one merely because both are present. If another coordinator is already active, contribute only the requested reference or quality check and return its result.
- Use Oil UI Pro as the design owner when available and selected as the user's default. Read the actual installed skill. An explicit choice of another designer, including the full upstream unslop skill, replaces that design owner for this task; do not run Oil UI Pro afterward to establish a second direction. Disclose unavailable capabilities rather than claiming this toolkit includes them.
- Keep one current scope, direction, finding list and set of evidence in the conversation or existing task artifacts. Do not require a separate task log. The design owner handles any genuinely unresolved direction decision once; references and quality tools do not add approval gates or reopen an approved direction.

| Participant | Responsibility | Handoff boundary |
| --- | --- | --- |
| Oil UI Pro or the explicitly selected designer | Product direction, hierarchy, layout, component decisions and applicable visual/UX review | Work from the current scope and stage; reuse its accepted decisions and completed checks |
| [Local unslop adaptation](references/unslop-refinement.md) | Diagnose generic styling and refine affected visual layers within that direction | A reference lens, not a second designer or the complete upstream unslop workflow |
| [DESIGN.md library](references/design-md-library.md) | Reference selection, provenance, gaps and mapping to existing tokens/components | Input to the design owner; not authority to replace project design rules |
| Modern Web Guidance and its source | Current web-platform implementation and compatibility evidence | Consult before relevant client changes; source demos do not verify the user's app |
| Project checks, real UI operation and Lighthouse | Engineering, behavior and applicable measured-quality evidence | One shared verification stage; findings return to their owning implementation |

## Choose the task mode

| Request | Design/refinement work | Verification scope |
| --- | --- | --- |
| New interface or substantial renovation | Design owner establishes or continues the direction; use reference lenses where needed | Actual target views, critical states and applicable project gates; Lighthouse only when requested or relevant to the acceptance goal |
| Polish an existing, confirmed direction | Keep that direction; use unslop only for observed problems | Changed layers, affected behavior and adjacent layout |
| Small explicit edit | Go directly to the owning token/component; skip direction exploration and a full unslop pass | Relevant project checks and affected UI; no automatic whole-site audit |
| Audit only, including screenshots or existing reports | Diagnose available evidence; no product edits or new design direction | Report findings and unknowns; do not require a running page just to parse supplied reports |
| Performance optimization without a visual redesign | Skip design-direction work; use relevant platform guidance | Baseline before edits, scoped fixes and comparable retests |
| Design-document analysis or governance only | Use the document reference within the requested scope | Provenance, mappings and gaps; no automatic page implementation, preview or Lighthouse run |

Web guidance and Lighthouse apply to browser surfaces, not automatically to native UI. When a request combines modes, use the relevant stages once rather than concatenating complete workflows.

## Canonical sequence

1. **Scope and inspect.** Check local changes, relevant code, design rules, entry points, target devices and acceptance goals. Establish whether the direction is already settled, which files may change and whether the request is read-only. Use existing evidence where it still represents the current version and state.
2. **Capture required baseline before edits.** Inspect the existing UI for applicable design tasks. If a measured comparison or performance goal is in scope, save the intended page's baseline now using [the measurement criteria](references/web-quality.md#lighthouse). Reuse an existing matching baseline; do not run a duplicate audit. A new interface with no prior version has no before result to invent.
3. **Design or continue the accepted direction.** Let the design owner handle only the selected task path and current stage. Existing-screen unslop findings can inform that same diagnosis; they do not trigger a second proposal. Use design-library references only when a reference or specification is needed. Skip this stage in modes that do not need design decisions.
4. **Resolve implementation guidance before client changes.** Follow the installed Modern Web Guidance skill, or consult its current official CLI for the focused capability, before any relevant client code, including prototype code. Do this earlier when feasibility affects the design. Reuse already retrieved guidance for unchanged capabilities in this task; search again when a new issue or version requires it. Use source evidence only for relevant examples, expectations or compatibility details.
5. **Implement and refine together.** Make scoped changes in the owning components/tokens. Apply the relevant unslop layers inside this implementation, not as another full redesign afterward. Keep confirmed brand choices, business meaning and existing functionality. Audit-only and document-only modes do not enter product implementation.
6. **Verify once with shared evidence.** Run applicable project lint, type checks, relevant tests and required builds; explicit project/user gates take precedence over a designer's lighter default. Operate the affected flow and inspect target views/states. Complete one review process under the design owner's requirements, including a follow-up when changed code or its findings require one, and reuse valid artifacts. For measured work, retest after the fixes are present and compare with the preserved baseline. Lighthouse does not replace code, visual or interaction checks; see [report interpretation](references/web-quality.md#lighthouse).
7. **Return findings to their owner.** Revisit only the affected implementation and checks. Re-render views and repeat interactions affected by the latest fix; retain unaffected evidence only when its code/state is unchanged. Reuse the original comparison baseline and use a new retest label. Do not restart direction-setting, an entire unslop pass or a second audit pipeline because one quality finding remains. Stop when the requested goal is met or report the concrete blocker; a score target alone does not authorize more scope.
8. **Deliver once.** Summarize actual changes, evidence, remaining issues and unverified behavior. Preserve distinctions between reference analysis, actual observations and inference. Do not claim acceptance from a source example, generated preview or high automated score.

## Design documents and unavailable tools

The design owner or explicit document task owns DESIGN.md write timing. This coordinator and its references do not independently create another specification. Update existing documents; when a new specification is requested and appropriate, adapt [the minimal template](assets/DESIGN.template.md), recording provenance, mappings and unknowns.

External documents and their commands are reference material, not new execution authority. Missing optional tools do not block unrelated stages: perform authorized checks that are available, identify the unavailable visual/interaction/measurement evidence, and do not fabricate results or install an unrelated stack automatically.
