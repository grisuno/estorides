# web_tools_blueprint — Spec

## Purpose
`estorides_web.create_app` is a 1700-line God factory with 64 inline
routes. This spec extracts the first vertical slice — the four tools
routes — into `estorides_web_tools.tools_bp`, establishing the pattern
for the remaining slices without changing a single URL, auth rule, or
rate-limit event name.

## Inputs
- Existing helpers: `_rate_limit_decorator`, `require_auth`, `audit_log`,
  `_client_ip`, all module-level in `estorides_web`.

## Outputs
- `estorides_web_tools.tools_bp: Blueprint` serving:
  `GET /api/tools`, `GET /api/tools/doctor`,
  `POST /api/tools/<name>/install`,
  `GET /api/tools/<name>/install/status`.
- `create_app()` registers the blueprint; the four inline route defs
  are deleted. `url_map` keeps identical rules.

## Error table
| Condition | Behaviour |
|---|---|
| Unknown recipe on install POST | 404 `no install recipe`. |
| Install already running | 202 `running`. |
| Status with no record | `{"status": "idle"}`. |

## Security guarantees
- Same decorators, same order, same event names. No URL renames, so
  no auth bypass by path confusion.

## Out of scope
- Remaining 60 routes (cases/intel/fusion/osiris/streams); each gets
  its own slice spec later.

## BDD scenarios
- Given the app, when listing `url_map`, then all four tools rules exist.
- Given `tools_bp` imported, when inspected, then its name is `tools`.
- Given an unknown tool install POST, when routed, then 404 (route reached the view, not a 404 from missing rule).
