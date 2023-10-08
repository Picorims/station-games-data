# station-games-data
Prepare data for the station-games repository: https://github.com/Picorims/station-games

## Environement setup

see requirements.txt for environment dependencies. Developed with Python 3.11.

## Licenses
### Program

Copyright (C) 2023  Picorims - licensed under the GNU AGPL-3.0-or-later

```
    This program processes open data from IDFM to prepare it for usage
    in picorims/station-games repository.
    Copyright (C) 2023  Picorims<picorims.contact@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

### Data

Stations data (`stops_data.json`) is licensed under the ODbL
and is a combination of the following sources:

- "Référentiel des arrêts : Arrêts", PRIM, snapshot from October 7th 2023, licensed under the Licence Ouverte v2.0 (Etalab)
    - **link:** https://prim.iledefrance-mobilites.fr/fr/donnees-statiques/arrets
    - **licence:** https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf
- "Référentiel des lignes de transport en commun d'île-de-France - lignes actives et prochainement actives", PRIM, snapshot from October 7th 2023, licensed under the ODbL (French version)
    - **link:** https://prim.iledefrance-mobilites.fr/fr/donnees-statiques/referentiel-des-lignes
    - **licence:** http://vvlibri.org/fr/licence/odbl-10/legalcode/unofficial
- "Arrêts et lignes associées", PRIM, snapshot from October 7th 2023, licensed under the ODbL (French version)
    - **link:** https://prim.iledefrance-mobilites.fr/fr/donnees-statiques/arrets-lignes
    - **licence:** http://vvlibri.org/fr/licence/odbl-10/legalcode/unofficial

You can find the derived data and its processing code in this repository.

