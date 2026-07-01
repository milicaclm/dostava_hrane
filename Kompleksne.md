Obrisi trenutnu analitiku i zatim napravi novu

1.Napiši Flux upit koji za svako vozilo računa ukupan broj zapisa gde je status 'accepted'. Upit mora da uključi filtriranje po merenju i polju, grupisanje po vehicle_id, agregaciju funkcijom count() i sortiranje rezultata od najvećeg ka najmanjem.

2.Napiši Flux upit koji za svakog korisnika (user_id) izračunava opseg kretanja (razliku između maksimalne i minimalne vrednosti) za polja latitude i longitude. Upit treba da koristi spread() i pivot() kako bi rezultati za obe koordinate bili prikazani u jednoj tabeli po korisniku.

3.Napiši složeni Flux upit koji pivotira delivery_status i distance po vremenu. Zatim, koristi elapsed() za izračunavanje trajanja svakog statusa. Nakon toga, obavezno primeni map() funkciju kako bi osigurao da je vrednost trajanja apsolutna (pozitivna). Nakon filtriranja distanci manjih ili jednakih nuli, kreiraj mapiranu kolonu efficiency kao odnos trajanja i distance. Na kraju, grupiši po user_id i delivery_status i izračunaj srednju vrednost (mean) efikasnosti.

4.Napiši Flux upit koji po user_id analizira zagušenje. Koristi map() da kreiraš binarne kolone (1 ili 0) za status 'canceled' i 'accepted'. Zatim, koristeći funkciju reduce(), izračunaj kumulativnu sumu oba statusa za svakog korisnika pojedinačno kako bi se dobio pregled odnosa otkazanih i prihvaćenih dostava.

5.Napiši Flux upit koji filtrira samo prihvaćene dostave ('accepted'). Koristi aggregateWindow sa intervalom od jednog sata (1h) i funkcijom count kako bi se dobila vremenska serija broja dostava po satima. Rezultat sortiraj hronološki.