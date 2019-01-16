# Lab 7 
## Sprawozdanie

### 1. Wygląd aplikacji

- Widok duży aplikacji
  - Rozwinięty pasek nawigacji
  - Link udostępnienia obok przycisku generacji

![Widok Duży](screenshots/app-view/large.PNG)

- Widok średni aplikacji
	- Rozwinięty pasek nawigacji
	- Link udostępnienia nad przyciskiem generacji

![Widok Średni](screenshots/app-view/medium.PNG)

- Widok mały aplikacji
	 Zwinięty pasek nawigacji do menu typu "dropdown"
	 - Link udostępnienia nad przyciskiem generacji

![Widok Mały](screenshots/app-view/small.PNG)

### 2. Kompilacja SCSS

Większość arkuszy CSS jest generowana z __Bootstrapa__ za pomocą skróconego arkusza głównego SCSS. 

```scss
@import "functions";
@import "variables";
@import "mixins";
@import "root";
@import "reboot";
@import "type";
@import "images";
@import "grid";
@import "tables";
@import "forms";
@import "buttons";
@import "transitions";
@import "dropdown";
@import "button-group";
@import "input-group";
@import "custom-forms";
@import "nav";
@import "navbar";
@import "card";
@import "breadcrumb";
@import "jumbotron";
@import "alert";
@import "media";
@import "list-group";
@import "modal";
@import "utilities";
```

Dzięki wyrzuceniu modułów jak np. `_badge.scss` udało się zmniejszyć pierwotny rozmiar pliku CSS z ~180KB do ~148KB. Własne pliki SCSS zostały zaś ograniczone do koniecznego minimum.

```scss
#body-container {
  max-width: 750px;
}

.upload-drop-zone {
  color: #ccc;
  border: 2px dashed #ccc;
  text-align: center;
}
.upload-drop-zone.drop {
  color: #222;
  border-color: #222;
}

.nav-logged-text {
  color: white;
  padding-right: 1em;
```


### 3. Audyt aplikacji

Pominąłem audyt dotyczący aplikacji progresywnych, gdyż niniejsza aplikacja opierająca się o pobieranie i wgrywanie plików z założenia nie będzie działać offline. 

![Audyt 1](screenshots/lighthouse/1.PNG)

Jak wynika z audytu, aplikacji brakuje tylko jednego punktu dla jednego parametru głównego do uzyskania wszędzie "zielonej oceny". Pierwsza metryka, dotycząca ogólnej prezencji posiada wysoką ocenę. Szczególnie ważny jest tu "Speed Index", z którego wynika, że strona ładuje się w krótkim czasie.

![Audyt 2](screenshots/lighthouse/2.PNG)

Problematyczny przycisk, to przycisk menu rozwijalnego. Druga, problematyczna część to tagi `<input>`, które tutaj w praktyce są outputem. Sprawdziłem jednak, że tagi `<output>` służą do wyświetlania tylko wyników operacji, dlatego ich nie użyłem.

![Audyt 3](screenshots/lighthouse/3.PNG)

Założyłem, że HTTP/2 nie jest częścią zadania. 

