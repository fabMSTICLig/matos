<template>
    <!--
        Quatrième bloc latéral : Type de traitement de la plage d'analyse
    -->
    <div class="card m-2">
        <div class="card-header" @click="show = !show">
            <h4 class="d-inline">Choix du Type de traitement de la plage d'analyse</h4> 
            <button
                class="btn btn-outline-info"
                type="button"
                @click.stop="$emit('showHelp')"
            >
            <span class="badge rounded-pill">i</span>
            </button>
            <p v-if="!show" class="dropdown-toggle"> <small> Dépliez Moi en cliquant ! </small> </p>
            <p v-else class="dropdown-toggle"> <small> Repliez Moi en cliquant ! </small> </p>
        </div>
        <div v-if="show" class="card-body">
            <div class="form-check mb-2" @change="$emit('typeTraitDate',clotLoanInput)">
                <input
                    :id="'clotLoanInput0'"
                    v-model="clotLoanInput"
                    type="radio"
                    class="form-check-input"
                    :value="0"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'clotLoanInput0'"
                    >
                    Afficher prêts dont date de retour <small>(rendu/fin)</small> comprise dans la plage définie
                </label>
            </div>
            <div class="form-check mb-2" @change="$emit('typeTraitDate',clotLoanInput)">
                <input
                    :id="'clotLoanInput1'"
                    v-model="clotLoanInput"
                    type="radio"
                    class="form-check-input"
                    :value="1"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'clotLoanInput1'"
                    >
                    Afficher prêts dont date de sortie <small>(début)</small> comprise dans la plage définie
                </label>
            </div>
            <div class="form-check" @change="$emit('typeTraitDate',clotLoanInput)">
                <input
                    :id="'clotLoanInput2'"
                    v-model="clotLoanInput"
                    type="radio"
                    class="form-check-input"
                    :value="2"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'clotLoanInput2'"
                    >
                    Afficher prêts dont dates de début ET de fin comprises dans la plage définie
                </label>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

    export default {
        emits: ['notChange','typeTraitDate','showHelp'],
        data() {
            return {
                show: false,
                clotLoanInput: ref("0")
            }
        }
    }
</script>