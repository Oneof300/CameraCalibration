<!-- TABLE OF CONTENTS -->
<details>
  <summary>Inhalt</summary>
  <ol>
    <li>
      <a href="#kamerakalibrierung">Kamerakalibrierung</a>
      <ul>
        <li><a href="#capturecalibrationimages">CaptureCalibrationImages</a></li>
        <li><a href="#calculatecameraparameters">CalculateCameraParameters</a>        
            <ul>
                <li><a href="#cameraparameters">cameraParameters</a></li>
            </ul>
        </li>   
        <li><a href="#undistortedcamera">Undistorted Camera</a></li>
      </ul>
    </li>
    <li><a href="#referenzen">Referenzen</a></li>
    <li><a href="#verwendete-module">Verwendete Module</a></li>
  </ol>
</details>

# Kamerakalibrierung
Bei der Erstsurchführung müssen die folgenden drei Programme zwingend der Reihe nach durchgeführt werden, damit die Kalibrierung mit den der verwendeten Kamera entsprechenden Parameter erfolgen kann. 

Wurden diese Kameraparameter bereits ermittelt und in der entsprechenden Datei gespeichert, genügt die Durchführung des dritten Programms, um ein korrekt entzerrtes Bild zu erhalten.


## CaptureCalibrationImages
[Das Programm zur Aufnahme der 10 Test-Fotos über die Webcam.](CaptureCalibrationImages.py)

Mit der c-Taste wird der aktuelle Frame im Verzeichnis „data“ gespeichert. Mit dem 10. Mal Auslösen wird das Programm automatisch beendet. Zudem kann es über die q-Taste vorzeitig beendet werden.

## CalculateCameraParameters
[Das Programm zur Bestimmung der Kameraparameter.](CalculateCameraParameters.py)

Anhand der Bilddateien, die zuvor mit CaptureCalibrationImages erzeugt wurden, werden hier die benötigten Kameraparameter ermittelt. Hierbei werden in den einzelnen Bildern, mit Hilfe der OpenCV „findChessboardCorners“- Funktion, eine vordefinierte Anzahl von Eckpunkten innerhalb Schachbrettmusters ermittelt. Diese werden in einem Array gespeichert. 

Mit Hilfe dieser Eckpunkte, werden dann die entsprechenden Kalibrierungsparameter berechnet. Diese Parameter werden anschließend in der Datei „cameraParameters.yaml“ gespeichert. Somit können diese für die zukünftige Kalibrierung immer wieder verwendet werden.

Zudem wird hier der Reprojektionsfehler berechnet. Dabei wird für jedes Kalibrierungsbild der Abstand zwischen jedem Bildpunkt und dem jeweils entsprechenden Weltpunkt, der in das Bild projiziert wird, berechnet. Anschließend wird die Summe aller ermittelten Werte berechnet, diese beschreibt den Reprojektionsfehler.

### cameraParameters
[Yaml Datei, in der die zuvor ermittelten Kameraparameter gespeichert werden.](data/cameraParameters.yaml)

## UndistortedCamera
[Das Programm zur Entzerrung eines Live-Bildes.](UndistortedCamera.py)

Hier werden zunächst die zuvor gespeicherten Kameraparameter geladen. Anhand derer wird dann eine Kameramatrix berechnet. Unter anderem wird mit dieser Kameramatrix anschließend jeder frame bzw. jedes Live-Bild entzerrt. 
Mit der q-Taste kann das Programm beendet werden.


# Referenzen
Für die Entwicklung der Skripte zur Kamerakalibrierung wurde das, in der Aufgabenstellung referenzierte, [OpenCV Tutorial](https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html) zur Orientierung verwendet. 

Um die ermittelten Kameraparameter in eine yaml Datei zu speichern wurde das [PyNative Tutorial](https://pynative.com/python-yaml/) verwendet.

# Verwendete Module
|Modul          |Version    |
|---------------|-----------|
|numpy          |1.22.3     |
|opencv-python  |4.5.5.64   |
|PyYAML         |6.0        |
