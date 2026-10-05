# ruttla-hub

Regelpakete für [Ruttla](https://github.com/hehljo/Ruttla) — geprüft, signiert,
reine Daten. Ein Paket installiert keinen Code: seine Regeln laufen in der
linearzeitigen Ruttla-Engine, und ein Scan bleibt offline.

```bash
ruttla hub search git
ruttla hub add gitgates      # prüft Signatur + Hash, schreibt ruttla-hub.lock
ruttla .                     # lädt die Paketregeln offline, nur bei passendem Hash
ruttla hub sync              # stellt nach einem Checkout den Stand des Lockfiles her
```

`hub add` und `hub sync` brauchen `sigstore` (`pip install 'ruttla[hub]'`
oder `python -m pip install 'sigstore>=4.5,<5'` in Ruttlas venv). Ohne bricht
der Befehl ab — ungeprüft wird nichts installiert.

## Aufnahme

Ein Paket ist ein Verzeichnis `packages/<name>/`:

```text
packages/<name>/package.toml
packages/<name>/rules/<plattform>/hub.<name>.<regel>.toml
```

`package.toml` trägt `format = "ruttla-hub-package/0"`, `name`, `version`,
`description`, `evidence` (https-URLs auf den belegten Fehlerfall) und
`license`. Das Regelformat ist `ruttla-rule/0`
([RULE_FORMAT.md](https://github.com/hehljo/Ruttla/blob/main/docs/RULE_FORMAT.md)).

Lokal genau so prüfen wie die CI:

```bash
python scripts/fetch_corpus.py corpus.toml /tmp/korpus > /tmp/korpus.args
ruttla hub check packages/<name> $(cat /tmp/korpus.args)
```

Angenommen wird nur, was alle drei Schritte besteht — jeder läuft, auch wenn
ein anderer ablehnt:

| Schritt | Lehnt ab |
|---|---|
| `format` | fehlender Beleg, ID außerhalb von `hub.<name>.`, Pfad ≠ `<plattform>/<id>.toml`, unbekannte Felder |
| `kit` | alles, was `ruttla rule test` ablehnt: Schema, Fixtures, Wirksamkeit, Laufzeitbudget |
| `falsch-positiv` | jeder Befund im gepinnten Gesund-Korpus (`corpus.toml`, Schwelle 0). Eine Regel, die dort keine Datei prüft, ist *nicht gemessen* und wird nicht angenommen |

Eine veröffentlichte Version ist unveränderlich: dieselbe Version mit anderem
Inhalt bricht den Build ab. Jede Änderung braucht eine neue Version.

Siehe [GOVERNANCE.md](GOVERNANCE.md) für Review und Vertrauensgrenzen.
