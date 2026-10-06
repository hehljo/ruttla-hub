# ruttla-hub

> English version: [README.md](README.md).

Regelpakete für [Ruttla](https://github.com/hehljo/Ruttla) — geprüft, signiert,
reine Daten. Ein Paket installiert keinen Code: seine Regeln laufen in der
linearzeitigen Ruttla-Engine, und ein Scan bleibt offline.

```bash
ruttla hub search git
ruttla hub add gitgates      # prüft Signatur + Hash, schreibt ruttla-hub.lock
ruttla .                     # lädt die Paketregeln offline, nur bei passendem Hash
ruttla hub sync              # stellt nach einem Checkout den Stand des Lockfiles her
```

Ein lokal verändertes Paket unter `.ruttla/hub/` überschreiben `add`, `sync`
und `remove` nie still: sie brechen ab und nennen es; `--force` sichert es
vorher nach `.ruttla/backup/`.

`hub add` und `hub sync` brauchen `sigstore` (`pip install 'ruttla[hub]'`
oder `python -m pip install 'sigstore>=4.5,<5'` in Ruttlas venv). Ohne bricht
der Befehl ab — ungeprüft wird nichts installiert.

## Eigene Regeln — erst im Projekt, dann für alle

1. Paket im eigenen Projekt anlegen: `.ruttla/packages/<name>/` in genau der
   Form unten. Jeder Scan dort lädt es sofort mit; kein `hub`-Befehl und kein
   `ruttla update` fasst es an.
2. `ruttla hub submit <name>` prüft Format und Konformitäts-Kit, gleicht die
   Version mit dem Index ab und zeigt, was eingereicht würde — gesendet wird
   nichts.
3. `ruttla hub submit <name> --yes` legt den PR an (braucht `git` und `gh`;
   ohne Schreibrecht über einen Fork).
4. Nach Review und Merge signiert die CI das Paket. Danach `ruttla hub add
   <name>` und die lokale Kopie löschen — sonst bricht der Scan ab, weil
   dasselbe Paket zweimal vorliegt.

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
