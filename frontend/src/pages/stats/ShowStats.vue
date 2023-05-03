<template>
    <div class="row">
      <!--
            Premier bloc latéral : Choix Type Statistique
      -->
      <div class="col-xl-3">
        <form class="form">
          <lateral-type-stat @type-stat="(recupStat) => statInput = recupStat" @not-change="searchChange()"/>
      <!--
        Second bloc latéral : Tri
      -->
          <lateral-type-tri @type-tri="(recupTri) => triInput = recupTri" @not-change="searchChange()"/>
      <!--
        Cinquième bloc latéral : Filtrage par type d'affiliation
            Optionnel
      -->
          <lateral-filter-aff :tri-value="triInput" @filter-aff="(recupFA) => filAffInput = recupFA" @not-change="searchChange()"/>
      <!--
        Sixième bloc latéral : Filtrage sur fréquence
            Optionnel
      -->
          <lateral-filter-freq :stat-value="statInput" :tri-value="triInput" @filter-freq="(recupFF) => filFreqInput = recupFF" @not-change="searchChange()"/>
      <!--
        Troisième bloc latéral : Plage d'analyse
      -->
          <lateral-plage-date :start-date-default="startDate" :end-date-default="endDate" @plage-start-date="(recupSD) => startDate = recupSD" @plage-end-date="(recupED) => endDate = recupED" @not-change="searchChange()"/>
      <!--
        Quatrième bloc latéral : Type de traitement de la plage d'analyse
      -->
          <lateral-type-trait-date @type-trait-date="(recupTD) => clotLoanInput = recupTD" @show-help="showHelp = !showHelp" @not-change="searchChange()"/>

      <!--
        Bouton de calcul statistique (=> provoque un appel API, en utilisant les données du formulaire)
      -->
            <button v-if="((statInput != null && triInput != null) && (!notChange))" class="btn btn-primary d-flex m-auto" @click="searchStat()">
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
        <div v-if="!showHelp" class="card mt-2">
          <div class="card-header">
            <div class="row justify-content-between">
              <div class="col-auto">
                <h3> {{ currentEntity.name }}: Statistiques</h3>
              </div>
              <div class="col-auto btn-toolbar">
                <div class="dropdwn">
                  <button v-if="(data != undefined)" class="btn btn-outline-secondary dropdown-toggle" id="dropDL" @click="(showDL = !showDL)">
                    <img src="@/../public/download.png" width="24" height="24">
                    Télécharger
                  </button>
                  <button v-else class="btn btn-outline-secondary dropdown-toggle" id="dropDL" @click="(showDL = !showDL)" disabled>
                    <img src="@/../public/download.png" width="24" height="24">
                    Télécharger
                  </button>
                  <ul class="dropdown-menu" :class="{ show: showDL }">
                    <li> <button class="dropdown-item" @click="downloadActualData(0)"> en .pdf </button> </li>
                    <li> <button class="dropdown-item" @click="downloadActualData(1)"> en .csv </button> </li>
                    <li> <button class="dropdown-item" @click="downloadActualData(2)"> en .json </button> </li>
                    <li> <button class="dropdown-item" @click="downloadActualData(3)"> en .txt </button> </li>
                  </ul>
                </div>
                <div>
                  <router-link
                    v-if="!isAuthLoans"
                    class="btn btn-outline-secondary float-end"
                    role="button"
                    :to="{ name: 'entityinfos', }"
                  >
                    Retour
                  </router-link>
                </div>
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
                  <select v-model="sortInput" class="form-select" @change="searchStat()">
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
              <div class="col-auto" v-if="(statInput == 'd_moy_emp' && columns != undefined)">
                <small>*une durée d'emprunt égale à 0 signifie qu'il n'y a aucun emprunt</small>
              </div>
            </div>
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead v-if="(loaded && columns != undefined)">
                  <tr>
                    <th v-for="title_col in columns"> {{ title_col }} </th>
                  </tr>
                </thead>
                <tbody v-if="(loaded && data != undefined)">
                  <tr v-for="statData in data">
                    <td>
                        {{ statData[0][0] }}
                    </td>
                    <td v-if="(statData[0].length > 1)">
                        {{ statData[0][1] }}
                    </td>
                    <td v-if="(statData[0].length > 2)">
                        {{ statData[0][2] }}
                    </td>
                    <td v-if="(statData[0].length > 3)">
                        {{ statData[0][3] }}
                    </td>
                    <td v-if="(statData[0].length > 4)">
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
        <div v-if="showHelp" class="card mt-2">
          <div class="card-header">
            <div class="row justify-content-between">
              <div class="col-auto">
                <h3> Aide : Type de traitement</h3>
              </div>
            </div>
          </div>
          <div class="card-body">
            <img src="@/../public/Schéma_aide.png" class="img-fluid mb-3"/>
            <button class="btn btn-primary d-flex m-auto" @click="showHelp = false">
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
  import { useRoute } from "vue-router";
  import { storeToRefs } from "pinia";
  import { useEntitiesStore } from "@/stores/entities";
  import { useStatsStore } from "@/stores/stats"
  import Pagination from "@/components/nav/ListPagination.vue";

  // importations des composants du panneau latéral
  import lateralTypeStat from "@/components/stats_components/LateralTypeStat.vue"
  import lateralTypeTri from "@/components/stats_components/LateralTypeTri.vue"
  import lateralFilterFreq from "@/components/stats_components/LateralFilterFreq.vue"
  import lateralFilterAff from "@/components/stats_components/LateralFilterAff.vue"
  import lateralTypeTraitDate from "@/components/stats_components/LateralTypeTraitDate.vue"
  import lateralPlageDate from "@/components/stats_components/LateralPlageDate.vue"
  
  // Constantes et fonctions générales
  const loaded = ref(false)
  const route = useRoute();
  const notChange = ref(true)
  const showHelp = ref(false)
  const columns = ref()
  const showDL = ref(false)

  function searchChange() {
    if (notChange.value){
      notChange.value = !notChange.value
    }
  }
  
  const entitiesStore = useEntitiesStore();
  const { objects: entity, currentEntity } = storeToRefs(entitiesStore);

  // Constantes et fonctions, de gestion des Input
  const sortChoices = {
    desc: { value: "", label: "Décroissant : + => -" },
    asc: { value: "Reverse", label: "Croissant : - => +" },
  };
  const sortInput = ref("");
  const statInput = ref()
  const triInput = ref()
  const filFreqInput = ref("0")
  const filAffInput = ref(["0","1","2","3","4","5","Naff"])
  const clotLoanInput = ref("0")

  const dDate = new Date()
  let tempDate = dDate.getFullYear().toString() + '-' // Year
  let tempSDate = (dDate.getFullYear() - 3).toString()
  if (dDate.getMonth() < 10){
    tempDate = tempDate + '0' + (dDate.getMonth()+1).toString() + '-' // Month
  } else {
    tempDate = tempDate + (dDate.getMonth()+1).toString() + '-' // Month
  }
  if (dDate.getDate() < 10) {
    tempDate = tempDate + '0' + dDate.getDate().toString() // Day
  } else {
    tempDate = tempDate + dDate.getDate().toString() // Day
  }
  tempSDate = tempSDate + tempDate.slice(4)
  const startDate = ref(tempSDate)
  const endDate = ref(tempDate)

  // Constantes et fonctions de gestion des pages
  const totalCount = ref(0)
  const currentPage = ref(1);
  const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST));
  const data = ref()

  function onPageChange(page) {
    currentPage.value = page;
    searchStat()
  }

  // Fonctions et constantes pour appels API et réception des données
  const statStore = useStatsStore();
  async function searchStat() {
    notChange.value = true
    updateColumns()

    let tempStr = ""
    for (let i = 0; i < filAffInput.value.length; i++) {
      if (i == filAffInput.value.length - 1) {
        tempStr += filAffInput.value[i]
      } else {
        tempStr += filAffInput.value[i] + ","
      }
    }

    let params = {'tri':triInput.value,'entity_selected':currentEntity.value.id,'start_d':startDate.value,'end_d': endDate.value,'filters_aff':tempStr,'filter_freq':filFreqInput.value,'reverse_order':sortInput.value,'offset':(currentPage.value-1) * 10,'limit':perPage.value,'clotured':clotLoanInput.value}
    data.value = await statStore.getDataPage(statInput.value,params)
    totalCount.value = data.value.pop()
  }

  async function downloadStat(dl) {
    let tempStr = ""
    for (let i = 0; i < filAffInput.value.length; i++) {
      if (i == filAffInput.value.length - 1) {
        tempStr += filAffInput.value[i]
      } else {
        tempStr += filAffInput.value[i] + ","
      }
    }

    let params = {'tri':triInput.value,'entity_selected':currentEntity.value.id,'start_d':startDate.value,'end_d': endDate.value,'filters_aff':tempStr,'filter_freq':filFreqInput.value,'reverse_order':sortInput.value,'clotured':clotLoanInput.value,'download':dl}
    let tempRet = await statStore.getDataPage(statInput.value,params)
    return tempRet
  }

  function updateColumns() {
    columns.value = []

    if (triInput.value == 0) {
      columns.value.push("Affiliation")
    } else if (triInput.value == 1) {
      columns.value.push("Prénom","Nom","Affiliations")
    } else if (triInput.value == 2) {
      columns.value.push("Nom","Référence Interne","Référence Fabricant","Nom Instance","Numéro de série Instance")
    } else {
      columns.value.push("Tag")
    }

    if (statInput.value == "nb_emp"){
      columns.value.push("Nombre d emprunts")
    } else if (statInput.value == "d_moy_emp") {
      columns.value.push("Durée moyenne d emprunts (en jours)")
    } else {
      columns.value.push("Fréquence d emprunts")
    }
  }

  /*
  type = integer appartenant à [0,1,2,3]
  0 = pdf
  1 = csv
  2 = json
  3 = txt
  */
  async function downloadActualData(type) {
    if (data.value != undefined) {
      if (triInput.value == 1) {
        showDL.value = false
        alert("Contrainte RGPD\n => téléchargement des statistiques avec tri par utilisateur impossible")
      } else {
        let date = ""
        if (startDate.value != undefined && startDate.value != null) {
          date += "dDebut-" + startDate.value
        } else if (endDate.value != undefined && endDate.value != null) {
          date += "_dFin-" + endDate.value
        }
        let labelData = ""
        let a = document.createElement("a");
        let file = null

        // labelDate génération
        if (type == 0) {
          // in PDF
          labelData = "Statistiques_" + currentEntity.value.name + "_" + statInput.value + "_" + columns.value[columns.value.length-1] + "_" + date + ".pdf";
          let pdfFile = await downloadStat("pdf")
          pdfFile = pdfFile.toString()
          file = new Blob([pdfFile], {
            type: "application/pdf",
          });

        } else if (type == 1) {
          // in CSV
          labelData = "Statistiques_" + currentEntity.value.name + "_" + statInput.value + "_" + columns.value[columns.value.length-1] + "_" + date + ".csv";
          let csvfile = ""
          for (let c of columns.value) {
            csvfile += c + ","
          }
          let tempFile = await downloadStat("csv")
          csvfile += "\n" + tempFile
          file = new Blob([csvfile], {
            type: "text/plain",
          });
        } else if (type == 2) {
          // in JSON
          labelData = "Statistiques_" + currentEntity.value.name + "_" + statInput.value + "_" + columns.value[columns.value.length-1] + "_" + date + ".json";
          let jsonfile = await downloadStat("json")
          file = new Blob([JSON.stringify({order:columns.value,values:jsonfile},null,2)], {
            type: "text/plain",
          });
        } else {
          // in TXT
          labelData = "Statistiques_" + currentEntity.value.name + "_" + statInput.value + "_" + columns.value[columns.value.length-1] + "_" + date + ".txt";
          let txtfile = "|"
          for (let c of columns.value) {
            txtfile += c + "|"
          }
          let tempFile = await downloadStat("txt")
          txtfile += "\n" + tempFile
          file = new Blob([txtfile], {
            type: "text/plain",
          });
        }
        a.href = URL.createObjectURL(file);
        a.download = labelData;
        a.click();

        showDL.value = false
      }
    } else {
      showDL.value = false
      alert("Aucune donnée à télécharger")
    }
  }

  loaded.value = true
</script>