<!--
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault

-->
<template>
  <div class="row">
    <!--
            Premier bloc latéral : Choix Type Statistique
      -->
    <div class="col-xl-3">
      <form class="form">
        <lateral-type-stat
          @type-stat="(recupStat) => (statInput = recupStat)"
          @not-change="searchChange()"
        />
        <!--
        Second bloc latéral : Tri
      -->
        <lateral-type-tri
          @type-tri="(recupTri) => (triInput = recupTri)"
          @not-change="searchChange()"
        />
        <!--
        Cinquième bloc latéral : Filtrage par type d'affiliation
            Optionnel
      -->
        <lateral-filter-aff
          :tri-value="triInput"
          @filter-aff="(recupFA) => (filAffInput = recupFA)"
          @not-change="searchChange()"
        />
        <!--
        Sixième bloc latéral : Filtrage sur fréquence
            Optionnel
      -->
        <lateral-filter-freq
          :stat-value="statInput"
          :tri-value="triInput"
          @filter-freq="(recupFF) => (filFreqInput = recupFF)"
          @not-change="searchChange()"
        />
        <!--
        Troisième bloc latéral : Plage d'analyse
      -->
        <lateral-plage-date
          :start-date-default="startDate"
          :end-date-default="endDate"
          @plage-start-date="(recupSD) => (startDate = recupSD)"
          @plage-end-date="(recupED) => (endDate = recupED)"
          @not-change="searchChange()"
        />
        <!--
        Quatrième bloc latéral : Type de traitement de la plage d'analyse
      -->
        <lateral-type-trait-date
          @type-trait-date="(recupTD) => (clotLoanInput = recupTD)"
          @show-help="showHelp = !showHelp"
          @not-change="searchChange()"
        />

        <!--
        Bouton de calcul statistique (=> provoque un appel API, en utilisant les données du formulaire)
      -->
        <button
          v-if="statInput != '' && triInput != -1 && !notChange"
          class="btn btn-primary d-flex m-auto"
          @click="searchStat()"
        >
          Calculer les Statistiques
        </button>
        <button v-else class="btn btn-primary d-flex m-auto" disabled>
          Calculer les Statistiques
        </button>
      </form>
    </div>
    <!--
            Bloc principal
      -->
    <div class="col">
      <div v-if="!showHelp && !showWait" class="card mt-2">
        <div class="card-header">
          <div class="row justify-content-between">
            <div class="col-auto">
              <h3>{{ currentEntity.name }}: Statistiques</h3>
            </div>
            <div class="col-auto btn-group">
              <div class="dropdwn">
                <button
                  id="dropDL"
                  class="btn btn-outline-secondary dropdown-toggle"
                  :disable="data == undefined"
                  @click="showDL = !showDL"
                >
                  <svg class="svg-icon" viewBox="0 0 20 20">
                    <path
                      fill="white"
                      d="M15.608,6.262h-2.338v0.935h2.338c0.516,0,0.934,0.418,0.934,0.935v8.879c0,0.517-0.418,0.935-0.934,0.935H4.392c-0.516,0-0.935-0.418-0.935-0.935V8.131c0-0.516,0.419-0.935,0.935-0.935h2.336V6.262H4.392c-1.032,0-1.869,0.837-1.869,1.869v8.879c0,1.031,0.837,1.869,1.869,1.869h11.216c1.031,0,1.869-0.838,1.869-1.869V8.131C17.478,7.099,16.64,6.262,15.608,6.262z M9.513,11.973c0.017,0.082,0.047,0.162,0.109,0.226c0.104,0.106,0.243,0.143,0.378,0.126c0.135,0.017,0.274-0.02,0.377-0.126c0.064-0.065,0.097-0.147,0.115-0.231l1.708-1.751c0.178-0.183,0.178-0.479,0-0.662c-0.178-0.182-0.467-0.182-0.645,0l-1.101,1.129V1.588c0-0.258-0.204-0.467-0.456-0.467c-0.252,0-0.456,0.209-0.456,0.467v9.094L8.443,9.553c-0.178-0.182-0.467-0.182-0.645,0c-0.178,0.184-0.178,0.479,0,0.662L9.513,11.973z"
                    ></path>
                  </svg>
                  Télécharger
                </button>
                <ul class="dropdown-menu" :class="{ show: showDL }">
                  <li>
                    <button
                      class="dropdown-item"
                      @click="downloadActualData(0)"
                    >
                      en .pdf
                    </button>
                  </li>
                  <li>
                    <button
                      class="dropdown-item"
                      @click="downloadActualData(1)"
                    >
                      en .csv
                    </button>
                  </li>
                  <li>
                    <button
                      class="dropdown-item"
                      @click="downloadActualData(2)"
                    >
                      en .json
                    </button>
                  </li>
                  <li>
                    <button
                      class="dropdown-item"
                      @click="downloadActualData(3)"
                    >
                      en .txt
                    </button>
                  </li>
                </ul>
              </div>
                <router-link
                  class="btn btn-outline-secondary float-end"
                  role="button"
                  :to="{ name: 'entityinfos' }"
                >
                  Retour
                </router-link>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <div class="input-group">
                <label class="input-group-text" for="typeselect"
                  >Ordre :
                </label>
                <select
                  v-model="sortInput"
                  class="form-select"
                  @change="searchStat()"
                >
                  <option
                    v-for="item in sortChoices"
                    :key="item.value"
                    :value="item.value"
                  >
                    {{ item.label }}
                  </option>
                </select>
              </div>
            </div>
            <div
              v-if="statInput == 'd_moy_emp' && columns != undefined"
              class="col-auto"
            >
              <small
                >*une durée d'emprunt égale à 0 signifie qu'il n'y a aucun
                emprunt</small
              >
            </div>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead v-if="loaded && columns != undefined">
                <tr>
                  <th v-for="title_col in columns" :key="title_col">
                    {{ title_col }}
                  </th>
                </tr>
              </thead>
              <tbody v-if="loaded && data != undefined">
                <tr v-for="statData in data" :key="statData[1]">
                  <td>
                    {{ statData[0][0] }}
                  </td>
                  <td v-if="statData[0].length > 1">
                    {{ statData[0][1] }}
                  </td>
                  <td v-if="statData[0].length > 2">
                    {{ statData[0][2] }}
                  </td>
                  <td v-if="statData[0].length > 3">
                    {{ statData[0][3] }}
                  </td>
                  <td v-if="statData[0].length > 4">
                    {{ statData[0][4] }}
                  </td>
                  <td>
                    {{ statData[1] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <pagination
            v-if="loaded"
            :total="totalCount"
            :per-page="perPage"
            :current-page="currentPage"
            @pagechanged="onPageChange"
          />
        </div>
      </div>
      <div
        v-if="showWait && !showHelp"
        class="h-100 d-flex justify-content-center align-items-center"
      >
        <p class="fw-semibold fs-2">
          Merci de patientez, les calculs sont en cours...
        </p>
      </div>
      <div v-if="showHelp" class="card mt-2">
        <div class="card-header">
          <div class="row justify-content-between">
            <div class="col-auto">
              <h3>Aide : Type de traitement</h3>
            </div>
          </div>
        </div>
        <div class="card-body">
          <img src="@/../public/Schéma_aide.png" class="img-fluid mb-3" />
          <button
            class="btn btn-primary d-flex m-auto"
            @click="showHelp = false"
          >
            J'ai Compris
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
// importations des éléments utilisés
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useEntitiesStore } from "@/stores/entities";
import { useStatsStore } from "@/stores/stats";
import Pagination from "@/components/nav/ListPagination.vue";

// importations des composants du panneau latéral
import lateralTypeStat from "@/components/stats_components/LateralTypeStat.vue";
import lateralTypeTri from "@/components/stats_components/LateralTypeTri.vue";
import lateralFilterFreq from "@/components/stats_components/LateralFilterFreq.vue";
import lateralFilterAff from "@/components/stats_components/LateralFilterAff.vue";
import lateralTypeTraitDate from "@/components/stats_components/LateralTypeTraitDate.vue";
import lateralPlageDate from "@/components/stats_components/LateralPlageDate.vue";

// Constantes et fonctions générales
const loaded = ref(false); // passe à true quand la page est chargée
const notChange = ref(true); // indique si il y a eu un changement dans les paramètres depuis le dernier calcul
const showHelp = ref(false); // indique la visibilité de la page d'aide
const columns = ref(); // contient les noms des colonnes du taleau des données
const showDL = ref(false); // indique la visibilité du menu déroulant de téléchargement
const showWait = ref(false); // indique la visibilité du message d'attente (quand on attend les données du serveur)

// fonction qui modifie la valeur de la variable notChange si celle-ci est True
// sinon ne fait rien
function searchChange() {
  if (notChange.value) {
    notChange.value = !notChange.value;
  }
}

const entitiesStore = useEntitiesStore();
const { currentEntity } = storeToRefs(entitiesStore);

// Constantes et fonctions, de gestion des Input
const sortChoices = {
  // dictionnaire contenant les valeurs de l'input d'ordre
  desc: { value: "", label: "Décroissant : + => -" },
  asc: { value: "Reverse", label: "Croissant : - => +" },
};
const sortInput = ref(""); // valeur de l'input de l'ordre par défaut "", correspond à l'ordre décroissant
const statInput = ref(''); // contient la valeur de la statistique souhaitée
const triInput = ref(-1); // contient la valeur du tri souhaité
const filFreqInput = ref("0"); // contient la valeur du filtre par fréquence
const filAffInput = ref(["0", "1", "2", "3", "4", "5", "Naff"]); // contient la ou les valeurs des filtres par affiliation
const clotLoanInput = ref("0"); // contient la valeur du type de traitement souhaité pour la plage de dates

// construction of defaults values for dates
const dDate = new Date();
let tempDate = dDate.getFullYear().toString() + "-"; // Year
let tempSDate = (dDate.getFullYear() - 3).toString();
if (dDate.getMonth() < 10) {
  tempDate = tempDate + "0" + (dDate.getMonth() + 1).toString() + "-"; // Month
} else {
  tempDate = tempDate + (dDate.getMonth() + 1).toString() + "-"; // Month
}
if (dDate.getDate() < 10) {
  tempDate = tempDate + "0" + dDate.getDate().toString(); // Day
} else {
  tempDate = tempDate + dDate.getDate().toString(); // Day
}
tempSDate = tempSDate + tempDate.slice(4);
const startDate = ref(tempSDate); // contient la date de début de la plage de dates => by default = day date - 3 years
const endDate = ref(tempDate); // contient la date de fin de la plage de dates => by default = day date

// Constantes et fonctions de gestion des pages
const totalCount = ref(0); // nombre total de pages, défini au moment de la récupération des données d'une statistique
const currentPage = ref(1); // page actuelle => débute à 1
const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST)); // nombre d'éléments maximum par page, initialisé en fonction de la variable d'environnement de Vite
const data = ref(); // correspond aux données réceptionnées pour une statistique

// fonction à appeler au changement de page,
// modifie la valeur de la page actuelle et demande les données de la page au serveur
function onPageChange(page) {
  currentPage.value = page;
  searchStat();
}

// Fonctions et constantes pour appels API et réception des données pour une page d'une certaine statistique
const statStore = useStatsStore(); // store qui contient les méthodes d'appel à l'API
async function searchStat() {
  notChange.value = true; // on passe la variable à True
  showWait.value = true; // on montre le message d'attente en attendant de recevoir les données
  updateColumns(); // on met à jour les noms des colonnes du tableau

  let tempStr = ""; // string temporaire pour construire la chaine qui contient les filtres pour le tri par affiliation
  for (let i = 0; i < filAffInput.value.length; i++) {
    if (i == filAffInput.value.length - 1) {
      tempStr += filAffInput.value[i];
    } else {
      tempStr += filAffInput.value[i] + ",";
    }
  }

  // objet contenant les paramètres de la requête pour l'API
  let params = {
    tri: triInput.value,
    entity_selected: currentEntity.value.id,
    start_d: startDate.value,
    end_d: endDate.value,
    filters_aff: tempStr,
    filter_freq: filFreqInput.value,
    reverse_order: sortInput.value,
    offset: (currentPage.value - 1) * 10,
    limit: perPage.value,
    clotured: clotLoanInput.value,
  };
  data.value = await statStore.getDataPage(statInput.value, params); // attente puis assignation du résultat à la variable data
  totalCount.value = data?.value.pop(); // si data existe, prend le dernier élément (qui correspond au nombre de pages total) puis l'assigne à totalCount
  showWait.value = false; // on masque le message d'attente car tout a été réceptionné
}
/* 
  appel API pour recevoir les données du fichier téléchargeable souhaité
    parameter 'dl' contain a string with the format of document,
    formats supports :
        "pdf" | "txt" | "csv" | "json"
  */
async function downloadStat(dl) {
  let tempStr = ""; // string temporaire pour construire la chaine qui contient les filtres pour le tri par affiliation
  for (let i = 0; i < filAffInput.value.length; i++) {
    if (i == filAffInput.value.length - 1) {
      tempStr += filAffInput.value[i];
    } else {
      tempStr += filAffInput.value[i] + ",";
    }
  }

  // objet contenant les paramètres de la requête pour l'API
  let params = {
    tri: triInput.value,
    entity_selected: currentEntity.value.id,
    start_d: startDate.value,
    end_d: endDate.value,
    filters_aff: tempStr,
    filter_freq: filFreqInput.value,
    reverse_order: sortInput.value,
    clotured: clotLoanInput.value,
    download: dl,
  };
  let tempRet = await statStore.getDataPage(statInput.value, params); // attente et récupération des données à télécharger (le fichier)
  return tempRet;
}

/* 
  modifications des noms des colonnes du tableau de résultat
        (effectué dans une fonction pour que la modification ne soit pas 
        fait en temps réel mais seulement quand elle est souhaitée)
  */
function updateColumns() {
  columns.value = []; // réinitialisation du tableau des colonnes

  // ajout des noms de colonnes en fonction du tri sélectionné
  if (triInput.value == 0) {
    columns.value.push("Affiliation");
  } else if (triInput.value == 1) {
    columns.value.push("Prénom", "Nom", "Affiliations");
  } else if (triInput.value == 2) {
    columns.value.push(
      "Nom",
      "Référence Interne",
      "Référence Fabricant",
      "Nom Instance",
      "Numéro de série Instance"
    );
  } else {
    columns.value.push("Tag");
  }

  // ajout des noms de colonnes en fonction de la statistique sélectionnée
  if (statInput.value == "nb_emp") {
    columns.value.push("Nombre d emprunts");
  } else if (statInput.value == "d_moy_emp") {
    columns.value.push("Durée moyenne d emprunts (en jours)");
  } else {
    columns.value.push("Fréquence d emprunts");
  }
}

/*
  Fonction qui met en place le téléchargement des données actuelles puis provoque le téléchargement

  type = integer appartenant à [0,1,2,3]
  0 = pdf
  1 = csv
  2 = json
  3 = txt
  */
async function downloadActualData(type) {
  // si la variable data contient des données
  if (data.value != undefined) {
    // si le tri est par utilisateur, téléchargement impossible pour contrainte RGPD
    if (triInput.value == 1) {
      showDL.value = false;
      alert(
        "Contrainte RGPD\n => téléchargement des statistiques avec tri par utilisateur impossible"
      );
    } else {

      let triName = ['aff', '', 'mats', 'tags'];
      // sinon pour tout autre tri
      let date = ""; // construction de la chaine contenant les dates de la plage sélectionnée => sert pour le nom du fichier
      if (startDate.value != undefined && startDate.value != null) {
        date += "s" + startDate.value;
      }
      if (endDate.value != undefined && endDate.value != null) {
        date += "_e" + endDate.value;
      }
      // initialisation des variables
      let labelData = "";
      let a = document.createElement("a");
      let file = null;

      if (type == 0) {
        // in PDF
        // construction du nom du fichier
        labelData =
          "Statistiques_" +
          currentEntity.value.name +
          "_" +
          triName[triInput.value]+
          "_" +
          statInput.value +
          "_" +
          date +
          ".pdf";
        let pdfFile = await downloadStat("pdf"); // récupération du fichier à télécharger
        pdfFile = pdfFile.toString(); // conversion en chaine de caractères (pour téléchargement)
        file = new Blob([pdfFile], {
          // construction d'un blob avec le fichier pdf en string
          type: "application/pdf",
        });
      } else if (type == 1) {
        // in CSV
        // construction du nom du fichier
        labelData =
          "Statistiques_" +
          currentEntity.value.name +
          "_" +
          triName[triInput.value]+
          "_" +
          statInput.value +
          "_" +
          date +
          ".csv";
        // construction du début du fichier (pour les noms des colonnes)
        let csvfile = "";
        for (let c of columns.value) {
          csvfile += c + ",";
        }
        let tempFile = await downloadStat("csv"); // récupération du fichier à télécharger
        csvfile += "\n" + tempFile; // concaténation du fichier reçu et du début construit au préalable
        file = new Blob([csvfile], {
          // construction d'un blob avec le fichier csv
          type: "text/plain",
        });
      } else if (type == 2) {
        // in JSON
        // construction du nom du fichier
        labelData =
          "Statistiques_" +
          currentEntity.value.name +
          "_" +
          triName[triInput.value]+
          "_" +
          statInput.value +
          "_" +
          date +
          ".json";
        let jsonfile = await downloadStat("json"); // récupération du fichier à télécharger
        file = new Blob(
          [JSON.stringify({ order: columns.value, values: jsonfile }, null, 2)],
          {
            // construction d'un blob avec le fichier json et les colonnes
            type: "text/plain",
          }
        );
      } else {
        // in TXT
        // construction du nom du fichier
        labelData =
          "Statistiques_" +
          currentEntity.value.name +
          "_" +
          triName[triInput.value]+
          "_" +
          statInput.value +
          "_" +
          date +
          ".txt";
        // construction du début du fichier (pour les noms des colonnes)
        let txtfile = "|";
        for (let c of columns.value) {
          txtfile += c + "|";
        }
        let tempFile = await downloadStat("txt"); // récupération du fichier à télécharger
        txtfile += "\n" + tempFile; // concaténation du fichier reçu et du début construit au préalable
        file = new Blob([txtfile], {
          // construction d'un blob avec le fichier txt
          type: "text/plain",
        });
      }
      a.href = URL.createObjectURL(file); // assignation d'un lien vers un objet (le fichier/blob construit) au lien 'a' construit au préalable
      a.download = labelData; // définition du nom du fichier téléchargé en utilisant le lien
      a.click(); // clic sur le lien pour lancer le téléchargement

      showDL.value = false; // fermeture du menu déroulant de téléchargement
    }
  } else {
    // si data ne contient pas de données (normalement le bouton de téléchargement est désactivé dans ce cas)
    showDL.value = false; // on ferme le menu déroulant de téléchargement
    alert("Aucune donnée à télécharger"); // on informe l'utilisateur qu'il n'y a aucune donnée à télécharger
  }
}

loaded.value = true; // tout a été effectué donc la page a fini de charger
</script>
