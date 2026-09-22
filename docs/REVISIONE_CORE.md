# Revisione del nucleo di traduzione

## Perimetro e rami

- `main`: traduzione di WF net safe e sound in specifiche DECLARE
  sull'alfabeto delle **transizioni**, identificato dagli ID PNML.
- `dev`, creato dal commit `f7c6bca`: conserva lo stato sperimentale precedente
  alla pulizia. Contiene integralmente tutti i file di sviluppo rimossi da main.
  Il branch è locale; questa operazione non pubblica modifiche sul remoto.
- Prima della pulizia, `main` è stato aggiornato in fast-forward al riferimento
  locale `origin/main` (`fb7f882`), preservando i tre aggiornamenti di
  documentazione e immagini già disponibili.

Per lavorare sugli esperimenti: `git switch dev`. Per tornare al nucleo stabile:
`git switch main`. Il ramo dev è uno snapshot dei prototipi, non una versione
corretta o aggiornata della CLI stabile.

## Algoritmo preservato

La versione preesistente `dec_translator_nolables.py` implementava già le tre
regole sugli ID. Il traduttore unico `src/declare_translator/dec_translator.py`
consolida quella logica:

1. `Atmost1(postset(source))`;
2. `End(preset(sink))`;
3. `AlternatePrecedence(preset(p), postset(p))` per ogni posto interno.

I raggruppamenti branched restano intatti. Non sono state aggiunte chiusure,
proiezioni, riduzioni o regole di sintesi. Le liste dei parametri sono ordinate
per produrre output ripetibile. `tasks` contiene tutti gli ID di transizione;
i nomi non influenzano i vincoli. Il JSON mantiene `name`, `tasks`, `constraints`.
Il mapping delle etichette non fa parte della specifica stabile.

Questo è il perimetro dell'algoritmo del paper: l'alfabeto è T. La revisione
precedente delle silent e delle etichette riguardava le estensioni sperimentali,
non confuta l'encoding di base sulle transizioni.

Riferimento: [paper, definizione 13 e algoritmo 1](https://arxiv.org/html/2504.05114v2).

## Codice separato da main

I seguenti file/cartelle sono conservati nel branch dev:

- `main_dev.py`, `labeling.py`, `src/alignment.py`, `conformance/`;
- i due traduttori silent, `dec_translator_output.py`,
  `dec_translator_nolables.py`, `src/declare_translator/alternative_versions/`;
- `src/input/`, `src/output/`, con esempi e output sperimentali;
- `src/test-runner.py`, `src/runTests.sh` (benchmark con import/percorso obsoleti);
- i tre exporter in `src/utils/`, duplicati o con percorsi assoluti.

Sono stati confrontati i blob dei 60 file rimossi con il contenuto di dev prima
della rimozione: nessuno conteneva modifiche locali da perdere.
La CLI stabile ha solo `declare-synth` ed `export-wn`, senza dipendenza da
PM4Py o dal conformance checker. Il vecchio ambiente completo è conservato in
`evaluation/environment.yml`; quello alla radice serve il solo nucleo.

I materiali sperimentali del paper in `evaluation/` sono preservati. Gli 11
file `.DS_Store`/`.pyc` sono stati rimossi dall'indice, mantenendo le copie locali.
Dati ignorati e schizzi locali non sono stati cancellati né inclusi nei commit.

## Parser e interfaccia

Le modifiche al parser proteggono l'ingresso dell'algoritmo, senza modificarne
le regole. Sono supportati PNML con/senza namespace e posti/transizioni senza
nome. Gli ID sono preservati. Le marcature mancanti si ricavano da source e sink.

Si rifiutano esplicitamente ID duplicati, archi pendenti/non bipartiti,
archi duplicati o non unitari, riferimenti PNML non supportati, più reti nello
stesso documento, strutture non WF e marcature incompatibili con source/sink.

Il parser verifica la struttura; **non certifica safety e soundness**. Anche la
funzione Python `translate_to_DEC` assume un dizionario di rete valido, safe e
sound: chiamandola direttamente si è responsabili di queste precondizioni.

L'uso degli ID cambia intenzionalmente i simboli rispetto alla vecchia CLI che
usava i nomi. I log di attività richiedono un mapping/realizzazione separato,
da sviluppare su dev; non vanno confrontati direttamente con questa specifica.

## Verifiche eseguite

La suite passa sia nell’ambiente Conda esistente sia in una `.venv` pulita
con Python 3.13 e le dipendenze di `requirements.txt`; `pip check` non rileva
incompatibilità. È aggiunta una CI per Python 3.11, 3.12 e 3.13, che verrà
eseguita al push (non ancora eseguita sul servizio remoto).

- 15 test unittest, compresi parser, CLI JSON/CSV/export, errori d'ingresso,
  invarianza ai nomi/metadati e non mutazione dell'input.
- Confronto esaustivo dei linguaggi tramite prodotto finito su sette reti
  sintetiche: singola transizione, sequenza con etichette duplicate, XOR, AND,
  loop, self-loop, alternative sui posti iniziale/finale.
- Stesso confronto sui cinque modelli PNML già presenti nella raccolta di
  bisimulazione. I file con nomi che menzionano silent sono verificati trattando
  ogni transizione come simbolo esplicito, senza nasconderla.
- Un test muta deliberatamente la specifica, rimuovendo un vincolo, e verifica
  che l'oracolo trovi una traccia distinguente.
- Confronto con la versione ID originale su 23 modelli validi: tasks e vincoli
  coincidono, normalizzando soltanto l'ordine degli insiemi e ignorando il mapping
  di metadati della vecchia variante. Il campione include i cinque modelli di
  bisimulazione, i dodici real-world e sei modelli di benchmark generati.

Il confronto finito comprende tutte le lunghezze di traccia dei modelli testati,
ma non sostituisce la dimostrazione generale del paper. L'oracolo è test-only e
non usa il vecchio conformance checker basato su etichette.

## Problemi residui nei materiali di ricerca

Nel campione di 27 PNML, quattro file generati hanno ID duplicati:

| File sotto `evaluation/performance/` | Primo ID duplicato rilevato |
| --- | --- |
| `formula_size/expanded_pnml/out-complete/548.pnml` | `ueooi` |
| `formula_size/expanded_pnml/out-complete/773.pnml` | `efybh` |
| `formula_size/expanded_pnml/out-complete/999.pnml` | `efybh` |
| `set_cardinality/expanded_pnml/out-complete/548.pnml` | `amglm` |

Questi input ora falliscono esplicitamente; non sono stati rinominati o
rigenerati, perché ciò altererebbe i materiali sperimentali. I generatori e gli
script storici con percorsi assoluti richiedono una revisione separata prima di
ripetere gli esperimenti pubblicati. I risultati storici non sono stati
ricalcolati. L'integrazione esterna con MINERful non è stata eseguita in questa
revisione.
