V Assetsih se nahaja vsa potrebna koda za unity projekt. V njem so vse naše skripte, naš celoten svet v katerem se vozi avtomobil.
Za delovanje potreben Unity verzija 2020.2.1f


V controleNode se nahaja vsa potrebna koda za kontrolno vozlišče.
Za delovanje je potrebno:
- python 3.8.x
- QtCreator ter Qt python assets
Python knjižnice:
- AirSim
- PyQt5
- Pyserial
- Numpy
- Opencv-python
- Numba
- Traceback
- Os
- Pprint
- Pyaudio
- Wave
- Struct

Podatki o ploščici vsebuje .c kodo, ki se lahko nadaljno ureja za razne popravke ter nadgradnje.
Na ploščico pa lahko kar naložimo compiled.hex, ki je že zgenerirana koda.
Za delovanje potrebujemo:
- STM32F411 ploščico (modra)
- STM32CubeIDE (za urejanje kode)
- STM32 ST-LINK Utility (za nalaganje .hex dokumenta)
- USB kabel, ki ima na enem koncu mini B (obvezno podatkovni)
- USB kabel, ki ima na enem koncu micro USB (obvezno podatkovni)