# Tag 4: Advanced RAG – Verbesserung der Zuverlässigkeit

## 🎯 Heutiges Ziel

Gestern habt ihr ein Basis-RAG-System erstellt. Heute werden wir fortgeschrittene Retrieval-Techniken implementieren und testen, um dieses System robuster und genauer zu machen. Euer Ziel ist es, die Leistung eurer RAG-Pipeline mithilfe des bereitgestellten Evaluationsskripts **messbar zu verbessern**.

***

## 🛠️ Voraussetzungen

* Eine funktionierende RAG-Pipeline von Tag 3.
* Eure leistungsstärkste Konfiguration (Chunking-Strategie + Embedding-Modell) von Tag 3 dient als eure **Baseline**.

***

## ✅ Kernaufgaben

### Aufgabe 1: Baseline-Messung durchführen

Zuerst müsst ihr die Leistung eurer bestehenden Pipeline von Tag 3 messen. Dazu erstellt ihr eine Evaluationsdatei und führt das bereitgestellte Skript `evaluate.py` aus.

1. **Testdaten verarbeiten:** Ladet die `test_data.json`. Lasst eure RAG-Pipeline für jede Frage in dieser Datei eine Antwort generieren.
2. **Ergebnisdatei erstellen:** Erstellt eine neue JSON-Datei, die eine Liste von Objekten enthält. Jedes Objekt soll exakt die Inhalte der ursprünglichen Testdaten haben (`query`, `answer`, `page`) und zusätzlich einen neuen key `"result"` enthalten, der die von eurer Pipeline generierte Antwort speichert.
3. **Datei speichern:** Speichert diese neue Liste als `evaluation_data.json` im `data/`-Ordner eures Projekts.
    * **Hinweis für Windows-Nutzer:** Falls es zu Pfad-Problemen kommt, legt die `evaluation_data.json` zur Vereinfachung in dasselbe Verzeichnis wie das `evaluate.py`-Skript.
4. **Baseline evaluieren:** Führt das Skript `evaluate.py` aus, um eure Baseline-Genauigkeit zu ermitteln. Notiert euch diesen Wert.
Hinweis: Es kann durchaus vorkommen, dass die Ausgabe des Judges inkorrekte JSON erzeugt.

***

### Aufgabe 2: Hybrid Search implementieren und evaluieren

Eure erste Verbesserung ist die Implementierung von **Hybrid Search**, um die Schwächen der rein semantischen Suche auszugleichen.

* **Konzept:** Hybrid Search kombiniert die Stärken der semantischen Suche (Dense Retrieval) mit der klassischen Keyword-Suche (Sparse Retrieval).
* **Implementierung:** Erweitert eure Pipeline, sodass sie sowohl Dense- als auch Sparse-Vektoren für die Suche nutzt. Kombiniert die Ergebnisse beider Methoden, um eine finale, relevantere Liste von Dokumenten zu erhalten.
  * **Orientierungshilfe:** Der folgende Haystack-Artikel bietet eine hervorragende Anleitung zur praktischen Umsetzung: [Haystack Tutorial: Hybrid Retrieval](https://haystack.deepset.ai/tutorials/33_hybrid_retrieval)
* **Evaluation:** Führt `evaluate.py` erneut mit der neuen Hybrid-Retrieval-Pipeline aus. Vergleicht den neuen Score mit eurer Baseline.

***

### Aufgabe 3: Hypothetical Document Embeddings (HyDE) implementieren

Als Nächstes implementiert ihr HyDE, um die Asymmetrie zwischen kurzen Nutzerfragen und langen Antwortdokumenten zur **Abfragezeit** zu überbrücken.

* **Konzept:** Anstatt die Nutzerfrage direkt zu verwenden, generiert ein LLM zuerst eine "ideale", hypothetische Antwort auf die Frage. Das Embedding dieser generierten Antwort wird dann für die Suche nach realen Dokumenten in der Vektordatenbank verwendet.
* **Implementierung:** Baut in eure Abfrage-Pipeline einen Schritt ein, der für die eingehende Frage ein hypothetisches Dokument generiert.
  * **Strikte Anforderung:** Das hypothetische Dokument muss in einem **einzigen LLM-Aufruf** generiert und die Ausgabe mithilfe von **Structured Output** (z. B. über Pydantic, Instructor) extrahiert werden.
* **Evaluation:** Führt `evaluate.py` erneut aus und vergleicht die Leistung mit euren vorherigen Ergebnissen.

**Liefergegenstand:** Eine Vergleichstabelle der Genauigkeits-Scores (Baseline vs. Hybrid vs. HyDE).

***

### Aufgabe 4: Hypothetical Question Embeddings (HyQE) implementieren

Zuletzt implementiert ihr HyQE, eine Technik, die die Asymmetrie zur **Indexierungszeit** behebt.

* **Konzept:** Anstatt die Dokumenten-Chunks direkt zu embedden, generiert ein LLM für jeden Chunk mehrere hypothetische Fragen, die durch diesen Chunk beantwortet werden. Die Embeddings dieser Fragen werden dann in der Vektordatenbank gespeichert. Bei einer Abfrage wird die Nutzerfrage mit diesen generierten Fragen abgeglichen.
* **Implementierung:** Modifiziert eure Indexierungs-Pipeline. Für jeden Dokumenten-Chunk sollen 3-5 mögliche Fragen generiert werden.
  * **Strikte Anforderung:** Die Liste der Fragen muss pro Chunk in einem **einzigen LLM-Aufruf** generiert und mithilfe von **Structured Output** extrahiert werden.
* **Evaluation:** Führt die Indexierung mit HyQE erneut durch und messt die Genauigkeit mit `evaluate.py`.

**Liefergegenstand:** Eine abschließende Vergleichstabelle aller Pipeline-Versionen und eure Empfehlung für den besten Ansatz unter Berücksichtigung von Genauigkeit und Kompromissen.

***

## 🏆 Bonusaufgaben (Optional)

Abenteuerlustig? Wählt eine oder beide dieser Bonusaufgaben.

* **Bonus A: Small-to-Big Retrieval implementieren:**
  * Verbessert die Kontextqualität, indem ihr kleine, präzise Chunks (wie Sätze) einbettet, aber größere übergeordnete Chunks (wie Absätze) für das LLM abruft. Sucht während des Retrievals nach relevanten *kleinen Chunks*, aber übergebt dann deren zugehörige *übergeordnete Chunks* an den Generator-LLM. Evaluiert, ob dieser breitere Kontext die Antwortqualität verbessert.
* **Bonus B: Fortgeschrittene Evaluation mit RAGAS:** https://docs.ragas.io/en/v0.1.21/concepts/index.html
  * **Konzept:** Während unser `evaluate.py` die Genauigkeit misst, bieten Frameworks wie **RAGAS** standardisierte, branchenweit anerkannte Metriken. RAGAS kann die Leistung eurer Pipeline anhand von Metriken wie `faithfulness`, `answer_relevancy`, `context_precision` und `context_recall` bewerten, ohne für jede Metrik Ground-Truth-Antworten zu benötigen.
  * **Implementierung:**
    * Integriert die RAGAS-Bibliothek in euer Projekt.
    * Passt euer Evaluationsskript an, um die für RAGAS erforderlichen Daten zu sammeln: die `question` (Frage), die generierte `answer` (Antwort), die abgerufenen `contexts` (Kontexte) und die `ground_truth` (Referenzantwort) aus dem Testset.
    * Führt die RAGAS-Evaluation auf eurer leistungsstärksten Pipeline durch und analysiert die Ergebnisse.
    * **Hilfreiche Links:**
      * Haystack Integration: `https://haystack.deepset.ai/integrations/ragas`
      * LangChain Integration: `https://docs.ragas.io/en/v0.1.21/howtos/integrations/langchain.html`
  * **Liefergegenstand:** Ein Bericht über die RAGAS-Scores für eure beste Pipeline und eine kurze Analyse, die die Erkenntnisse aus RAGAS mit denen aus eurem `evaluate.py`-Skript vergleicht.
