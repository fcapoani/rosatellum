# Rosatellum

Divisione dei seggi nei collegi plurinominali della Camera come previsto dalla legge Rosato

Input: file csv che riporti almeno le seguenti colonne:

"CIRCOSCRIZIONE", "COLLEGIOPLURINOMINALE", "LISTA", "COALIZIONE", "VOTI_LISTA", "TIPO"

Ogni riga conterrà il risultato di una lista nel collegio indicato in "COLLEGIOPLURINOMINALE". Il codice raggruppa automaticamente più righe afferenti alla stessa lista nello stesso collegio (ad esempio se si prendono i dati da Eligendo dove sono ulteriorimente divisi per comune)

La colonna "TIPO" deve assumere il valore 1 se la lista (art. 83 della legge elettorale) è rappresentante di minoranze linguistiche e ha eletto almeno un quarto dei candidati nei collegi della regione o provincia autonoma in cui si presenta (in pratica: serve per escludere l'SVP dalle soglie di sbarramento)

Resta non ancora implementato il meccanismo di ripartizione dei voti dati al solo candidato uninominale tra le liste della coalizione (il file di esempio incluso è basato sui dati delle politiche 2018 piuttosto arbitrariamente ri-ripartiti nei nuovi collegi), e alcuni meccanismi di gestione delle situazioni di parità.

Sono inoltre presenti due file con il numero di seggi proporzionali assegnati alle circoscrizioni e ai collegi (nei due presenti, sono usate le suddivisioni per le elezioni 2022 post riduzione del numero dei parlamentari e basate sul censimento 2011, e pubblicate in Gazzetta ufficiale)
