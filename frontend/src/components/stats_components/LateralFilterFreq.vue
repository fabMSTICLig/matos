<template>
    <!--
        Sixième bloc latéral : Filtrage sur fréquence
            Optionnel
    -->
    <div v-if="(statValue == 'freq_emp' & triValue != 1)" class="card m-2">
        <div class="card-header" @click="show = !show">
            <h4>Choix du Filtrage sur fréquence</h4>
            <p v-if="!show" class="dropdown-toggle"> <small> Dépliez Moi en cliquant ! </small> </p>
            <p v-else class="dropdown-toggle"> <small> Repliez Moi en cliquant ! </small> </p>
        </div>
        <div class="card-body" v-if="show">
            <div class="form-check mb-1" @change="$emit('filterFreq',filFreqInput)">
                <input
                    type="radio"
                    :id="'filFreqInput0'"
                    class="form-check-input"
                    v-model="filFreqInput"
                    :value="0"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'filFreqInput0'"
                    >
                    Aucun Filtrage
                </label>
            </div>
            <div class="form-check mb-1" @change="$emit('filterFreq',filFreqInput)">
                <input
                    type="radio"
                    :id="'filFreqInput1'"
                    class="form-check-input"
                    v-model="filFreqInput"
                    :value="1"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'filFreqInput1'"
                    >
                    Empruntés uniquement
                </label>
            </div>
            <div class="form-check mb-1" @change="$emit('filterFreq',filFreqInput)">
                <input
                    type="radio"
                    :id="'filFreqInput2'"
                    class="form-check-input"
                    v-model="filFreqInput"
                    :value="2"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'filFreqInput2'"
                    >
                    Jamais empruntés uniquement
                </label>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

    export default {
        props: ['statValue','triValue'],
        emits: ['notChange','filterFreq'],
        data() {
            return {
                show: false,
                filFreqInput: ref("0"),
            }
        }
    }
</script>