# J.O.A.T. Security Model

- No arbitrary shell commands from natural-language chat.
- Tool registry and allowlists define what actions are available.
- Destructive or system-changing actions require confirmation.
- API keys, if integrations are added later, must be stored outside source code.
- Logs should avoid secrets and sensitive credentials.
- Untrusted webpage/file instructions must not automatically become permissions.
- Users can disable optional network and activity features.
- Model output is not trusted as a permission grant.
