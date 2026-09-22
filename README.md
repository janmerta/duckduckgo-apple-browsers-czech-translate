# Český překlad DuckDuckGo pro macOS

Tento repozitář uchovává české lokalizační soubory aplikace DuckDuckGo pro macOS.

## Překlad

Aktuální české soubory jsou ve složce [`translations/cs.lproj`](translations/cs.lproj):

- `Localizable.strings`
- `Localizable.stringsdict`
- `InfoPlist.strings`
- `DeveloperID.strings`

Nové překlady zachycené sledováním vývoje jsou oddělené podle zdrojového bundle katalogu ve složce [`translations/updates`](translations/updates). Díky tomu lze změny později bezpečně sloučit do odpovídajících `.xcstrings` souborů bez záměny hlavní aplikace a balíčku SyncUI.

## Sledování nových textů

Workflow `Watch DuckDuckGo localization strings` sleduje lokalizační klíče v oficiálním
repozitáři [`duckduckgo/apple-browsers`](https://github.com/duckduckgo/apple-browsers).
Spouští se každý den a lze jej spustit také ručně v záložce **Actions**.

Při prvním běhu vytvoří výchozí snapshot. Při dalších změnách založí issue s přehledem
přidaných a odstraněných klíčů a snapshot automaticky aktualizuje. Workflow používá pouze
standardní `GITHUB_TOKEN`; není potřeba ukládat vlastní přístupový token.

Původní repozitář `duckduckgo/macos-browser` byl archivován a vývoj byl přesunut do
`duckduckgo/apple-browsers`, proto se změny sledují tam.

## Hotový lokalizační balíček

GitHub po každé změně překladů automaticky sestaví ZIP. Nejnovější balíček je
vždy ke stažení v části [Releases](https://github.com/janmerta/duckduckgo-apple-browsers-czech-translate/releases/tag/czech-latest)
jako `DuckDuckGo-cs-localization.zip`.

Archiv obsahuje dvě oddělené lokalizace:

- `main-app/cs.lproj` pro hlavní aplikaci DuckDuckGo,
- `SyncUI-macOS/cs.lproj` pro samostatný resource bundle SyncUI.

Balíček lze sestavit také ručně příkazem
`python3 scripts/build_localization_package.py`. Výsledek vznikne ve složce
`dist`.
