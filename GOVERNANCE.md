# Governance

## Was der Hub verspricht — und was nicht

| Zusage | Wie gesichert |
|---|---|
| Ein Paket stammt aus diesem Repo | Sigstore-Signatur, Identität `publish.yml@refs/heads/main`, Aussteller GitHub Actions; der Client prüft genau diese Identität |
| Das installierte Paket ist das signierte | Hash im `ruttla-hub.lock`; jede Abweichung bricht den Scan ab (Exit 3) |
| Eine Version ändert sich nie | `ruttla hub build --previous` lehnt geänderten Inhalt unter bekannter Version ab |
| Eine Regel ist geprüft | Konformitäts-Kit + Falsch-Positiv-Lauf in der CI vor dem Signieren |
| Es wird kein Code installiert | Pakete sind JSON mit Regeltexten; Ruttla-Python-Plugins sind über den Hub nicht installierbar |

**Nicht** versprochen: dass eine Regel fachlich recht hat. Das entscheidet das
Review. Und das Lockfile schützt nicht vor einem böswilligen Prüfziel — wer
das Repo schreibt, schreibt auch das Lockfile; die Bauform begrenzt den
Schaden (nur Daten, linearzeitige Muster, nur zusätzliche Befunde).

## Review

- Jeder PR braucht eine grüne `check`-Ausführung und ein Review durch den
  Maintainer. Merge auf `main` veröffentlicht.
- Beleg (`evidence`) muss den Fehler tatsächlich zeigen, nicht nur das Thema.
- Keine Dublette eines offiziellen Ruttla-Checks; ist eine Regel allgemein
  genug, gehört sie nach Ruttla selbst.
- Korpus-Änderungen (`corpus.toml`) sind eigene PRs mit Begründung.

## Meldungen

Issue-Vorlagen: *Neue Regel*, *Falsch-positiv*, *Falsch-negativ*. Ein
bestätigter Falsch-positiv-Fall wird zur `pass`-Fixture, ein Falsch-negativ-Fall
zur `fail`-Fixture — nie nur zur Musteränderung.
