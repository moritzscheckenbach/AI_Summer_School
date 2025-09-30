# Lösungsdokument - Labor Tag 2

Hier sind die detaillierten Lösungswege für die anspruchsvollen Beispielaufgaben.

---

### Aufgabe A: Das Porträt

**Problem:**
Ein Mann schaut auf ein Porträt. Jemand fragt ihn, wessen Porträt er betrachtet. Er antwortet: "Brüder und Schwestern habe ich keine, aber der Vater dieses Mannes ist der Sohn meines Vaters." Wessen Porträt betrachtet der Mann?

**Lösung (mittels Chain-of-Thought):**

1. **Analyse der Prämisse 1:** "Brüder und Schwestern habe ich keine." Dies bedeutet, der Sprecher ist ein Einzelkind.
2. **Analyse der Prämisse 2:** "...der Vater dieses Mannes [im Porträt] ist der Sohn meines Vaters."
3. **Auflösen der inneren Beziehung:** Wer ist "der Sohn meines Vaters"? Da der Sprecher ein Einzelkind ist, kann "der Sohn meines Vaters" nur er selbst sein.
4. **Substitution:** Wir ersetzen den Teil "der Sohn meines Vaters" durch "ich". Der Satz lautet nun: "Der Vater dieses Mannes [im Porträt] bin ich."
5. **Finale Schlussfolgerung:** Wenn der Sprecher der Vater des Mannes auf dem Porträt ist, dann betrachtet er das Porträt seines Sohnes.

**Antwort:** Er betrachtet das Porträt **seines Sohnes**.

---

### Aufgabe B: Die Bälle im Korb

**Problem:**
Du hast eine Kiste mit drei Bällen: einem roten, einem grünen und einem blauen, in dieser Reihenfolge von links nach rechts. Du führst fünf Aktionen aus. Was ist der Endzustand?

**Lösung (mittels Chain-of-Thought):**
Wir verfolgen den Zustand der Bälle Schritt für Schritt.

- **Start:** `[rot, grün, blau]`
- **Nach Schritt 1 (rot und blau tauschen):** `[blau, grün, rot]`
- **Nach Schritt 2 (Ball in der Mitte nach rechts):** Der Ball in der Mitte ist `grün`. `[blau, rot, grün]`
- **Nach Schritt 3 (links und rechts tauschen):** `[grün, rot, blau]`
- **Nach Schritt 4 (Ball links gelb färben):** Der Ball links ist `grün`. `[gelb, rot, blau]`
- **Nach Schritt 5 (lila Ball in die Mitte):** Die Reihe hat jetzt 3 Bälle. Die Mitte ist Position 2. Der neue Ball wird dort eingefügt. `[gelb, lila, rot, blau]`

**Antwort:** Der Ball ganz links ist **gelb**. Es sind jetzt insgesamt **vier** Bälle in der Kiste.

---

### Aufgabe C: Früchte im Korb

**Problem:**
In einem Korb sind dreimal so viele Äpfel wie Birnen. Es sind halb so viele Birnen wie Pfirsiche. Es gibt 24 Pfirsiche. Wenn 1/3 der Äpfel, die Hälfte der Birnen und 1/4 der Pfirsiche grün sind, wie viele Früchte im Korb sind *nicht* grün?

**Lösung (mittels Chain-of-Thought):**

1. **Anzahl Pfirsiche:** 24
2. **Anzahl Birnen:** Die Hälfte von 24 = 12 Birnen.
3. **Anzahl Äpfel:** Dreimal so viele wie Birnen = 3 * 12 = 36 Äpfel.
4. **Gesamtzahl der Früchte:** 24 (Pfirsiche) + 12 (Birnen) + 36 (Äpfel) = 72 Früchte.
5. **Anzahl grüne Äpfel:** 1/3 von 36 = 12.
6. **Anzahl grüne Birnen:** 1/2 von 12 = 6.
7. **Anzahl grüne Pfirsiche:** 1/4 von 24 = 6.
8. **Gesamtzahl grüner Früchte:** 12 + 6 + 6 = 24 grüne Früchte.
9. **Anzahl nicht-grüner Früchte:** Gesamtzahl - grüne Früchte = 72 - 24 = 48.

**Antwort:** Es sind **48** Früchte nicht grün.

---

### Aufgabe D: Die Flugreise

**Problem:**
Ein Flugzeug startet am Dienstag um 22:00 Uhr in Tokio (UTC+9). Der Flug nach New York (UTC-4) dauert 13 Stunden. Wann landet es in New York (Wochentag und Uhrzeit)?

**Lösung (mittels Chain-of-Thought):**

1. **Startzeit in UTC umrechnen:** Tokio ist 9 Stunden vor UTC. Also 22:00 - 9 Stunden = 13:00 UTC am Dienstag.
2. **Ankunftszeit in UTC berechnen:** 13:00 UTC am Dienstag + 13 Stunden Flugzeit = 02:00 UTC am Mittwoch.
3. **Ankunftszeit in die lokale Zeitzone umrechnen:** New York ist 4 Stunden hinter UTC. Also 02:00 UTC - 4 Stunden = 22:00 Ortszeit.
4. **Wochentag bestimmen:** Da wir von 02:00 am Mittwoch zurückgerechnet haben und die Mitternachtsgrenze unterschritten haben, ist der Wochentag in New York noch Dienstag.

**Antwort:** Das Flugzeug landet am **Dienstag um 22:00 Uhr** Ortszeit in New York.

---

### Aufgabe E: Das Spiel mit den Münzen

**Problem:**
21 Münzen, 2 Spieler, 1-3 Münzen pro Zug. Wer die letzte nimmt, gewinnt. Spieler A startet. Was ist die Gewinnstrategie?

**Lösung (mittels Chain-of-Thought):**

1. **Ziel des Spiels analysieren:** Man gewinnt, wenn man den Gegner zwingt, eine Situation vorzufinden, aus der man im nächsten Zug sicher die letzte Münze nehmen kann.
2. **Rückwärts denken:** Um zu gewinnen, muss ich meinem Gegner einen Haufen von 1, 2 oder 3 Münzen überlassen.
3. **Die "Verliererposition" finden:** Wenn ich meinem Gegner einen Haufen von 4 Münzen überlasse, kann er nicht gewinnen. Nimmt er 1, lasse ich ihm 3; nimmt er 2, lasse ich ihm 2; nimmt er 3, lasse ich ihm 1. In jedem Fall kann ich im nächsten Zug den Rest nehmen. Eine Position von 4 Münzen ist also eine "Verliererposition" für den, der am Zug ist.
4. **Gewinnstrategie ableiten:** Die Strategie besteht darin, den Gegner immer auf einem Vielfachen von 4 zu lassen (4, 8, 12, 16, 20...). Dies sind die "Gewinnerpositionen", die man am Ende seines eigenen Zuges erreichen will.
5. **Den ersten Zug bestimmen:** Das Spiel startet mit 21 Münzen. Die nächstniedrigere "Gewinnerposition" ist 20. Um den Münzhaufen auf 20 zu reduzieren, muss Spieler A zu Beginn 21 - 20 = 1 Münze nehmen.
6. **Gesamte Strategie:** Spieler A nimmt 1 Münze. Danach, egal was Spieler B nimmt (x), Spieler A nimmt immer (4 - x) Münzen. (Nimmt B 1, nimmt A 3; nimmt B 2, nimmt A 2; nimmt B 3, nimmt A 1). Dadurch wird die Anzahl der Münzen nach jedem Zugpaar von A um 4 reduziert, und A wird garantiert die letzte Münze nehmen.

**Antwort:** Die Strategie ist, den Gegner immer auf eine Anzahl von Münzen zu bringen, die ein Vielfaches von 4 ist. Der erste Zug muss sein, **1 Münze** zu nehmen.
