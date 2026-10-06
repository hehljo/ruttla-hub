# ruttla-hub

Rule packages for [Ruttla](https://github.com/hehljo/Ruttla) — reviewed,
signed, pure data. A package installs no code: its rules run in Ruttla's
linear-time engine, and a scan stays offline.

> German version: [README.de.md](README.de.md).

```bash
ruttla hub search git
ruttla hub add gitgates      # verifies signature + hash, writes ruttla-hub.lock
ruttla .                     # loads the package rules offline, only on a matching hash
ruttla hub sync              # restores the lockfile state after a checkout
```

`add`, `sync` and `remove` never silently overwrite a locally modified
package under `.ruttla/hub/`: they abort and name it; `--force` backs it up to
`.ruttla/backup/` first.

`hub add` and `hub sync` need `sigstore` (`pip install 'ruttla[hub]'` or
`python -m pip install 'sigstore>=4.5,<5'` in Ruttla's venv). Without it the
command aborts — nothing is installed unverified.

## Your own rules — first in the project, then for everyone

1. Create the package in your own project: `.ruttla/packages/<name>/` in
   exactly the layout below. Every scan there loads it immediately; no `hub`
   command and no `ruttla update` touches it.
2. `ruttla hub submit <name>` checks the format and the conformance kit,
   compares the version with the index and shows what would be submitted —
   nothing is sent.
3. `ruttla hub submit <name> --yes` opens the PR (needs `git` and `gh`; via a
   fork without write access).
4. After review and merge, CI signs the package. Then run `ruttla hub add
   <name>` and delete the local copy — otherwise the scan aborts because the
   same package is present twice.

## Admission

A package is a directory `packages/<name>/`:

```text
packages/<name>/package.toml
packages/<name>/rules/<platform>/hub.<name>.<rule>.toml
```

`package.toml` carries `format = "ruttla-hub-package/0"`, `name`, `version`,
`description`, `evidence` (https URLs pointing to the documented failure) and
`license`. The rule format is `ruttla-rule/0`
([RULE_FORMAT.md](https://github.com/hehljo/Ruttla/blob/main/docs/RULE_FORMAT.md)).

Check locally exactly like CI does:

```bash
python scripts/fetch_corpus.py corpus.toml /tmp/corpus > /tmp/corpus.args
ruttla hub check packages/<name> $(cat /tmp/corpus.args)
```

Only what passes all three steps is accepted — each one runs, even when
another rejects:

| Step (as printed) | Rejects |
|---|---|
| `format` | missing evidence, ID outside `hub.<name>.`, path ≠ `<platform>/<id>.toml`, unknown fields |
| `kit` | everything `ruttla rule test` rejects: schema, fixtures, effectiveness, runtime budget |
| `falsch-positiv` | any finding in the pinned healthy corpus (`corpus.toml`, threshold 0). A rule that examines no file there is *not measured* and is not accepted |

A published version is immutable: the same version with different content
fails the build. Every change needs a new version.

See [GOVERNANCE.md](GOVERNANCE.md) for review and trust boundaries.
