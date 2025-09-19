# Kursmaterialien zu AICamp - I4

In diesem Repository finden Sie alle Codes, die im Rahmen des Moduls **I4** (AICamp) erstellt wurden. 

## Getting Started

Es gibt einige Möglichkeiten, dieses Repository zu verwenden - je nach Ihrem Komfortlevel:

1. **Als ZIP herunterladen**
   Falls Sie nicht firm in Git sind, ist das die einfachste Methode.
   - klicken Sie auf den grünen `<>Code`-Button rechts oben im Repository
   - wählen Sie 'Download ZIP' aus
   - extrahieren (unzippen) Sie den Folder auf ihrem PC
   - öffnen Sie den Folder in z.B. [VS Code](https://code.visualstudio.com/) oder einem anderen Editor Ihrer Wahl
     
2. **Über Git**
   Falls Sie sich bereits mit Git auskennen, können Sie das Repository auch einfach klonen:
   - git clone https://github.com/hannahwimmer/AICamp-I4.git
   - cd AICamp-I4
  
   Falls Sie sind *noch nicht* auskennen, es aber gerne versuchen würden, hier eine Variante, die VS Code als Editor verwendet:
   - installieren Sie [VS Code](https://code.visualstudio.com/)
   - installieren Sie [Python](https://www.python.org/downloads/) (klicken Sie "Add Python to PATH" während der Installation!)
   - erstellen Sie einen leeren Folder, z.B. direkt auf Ihrem Desktop
   - in VS Code, wählen Sie oben in der Leiste `File`>`Open Folder` und wählen Sie den erstellten leeren Folder aus
   - unter den Icons am linken Bildschirmrand in VS Code, wählen Sie den Tab `Source Control` aus (sieht aus wie drei Knoten eines Graphen)
   - wählen Sie `Initialize Repository` aus, dann klicken Sie auf die drei Punkte in der Zeile `CHANGES` und wählen sie 'Clone'
   - in der aufpoppenden Zeile, geben Sie die URL zu unserem GitHub-Repo ein (die finden Sie wieder in unserem Git Repo online unter dem grünen
     `<>Code`-Button - kopieren Sie einfach die Zeile mit `https://github....`) und drücken Enter
   - es öffnet sich der Explorer; hier suchen Sie wieder Ihren leeren Folder aus und wählen Sie ggf. "Open in New Window" aus
   Gratulation! Sie haben nun Ihr erstes Git Repo geklont in VS Code geöffnet!

3. Notebooks in Google Colab öffnen
   Wenn Sie sich keine Gedanken um Ihre Coding-Infrastruktur machen wollen, öffnen Sie das Repo am besten direkt in Google Colab:
   - gehen Sie zu [Google Colab](https://colab.google/)
   - klicken Sie auf `New Notebook`
   - geben Sie `pwd` ("print working directory") in die Code-Zeile ein und klicken Sie auf das Play Symbol, um herauszufinden, 
     in welchem Ordner Sie sich gerade befinden (sollte per Default `/content` sein)
   - in einer neuen Code-Zeile, geben Sie `!git clone https://github.com/hannahwimmer/AICamp-I4.git` (der Link zu unserem Github Repo) ein
     und klicken Sie auf das Play Symbol
   Wenn Sie nun auf das Ordner Symbol am linken Bildschirmrand gehen und den `content`-Ordner öffnen, sollten Sie dort jetzt einen Folder
   sehen, der "AICamp-I4" heißt.
   - Rechtsklicken Sie auf den Ordner und wählen Sie 'Öffnen' - dann wird alles strukturiert angezeigt
