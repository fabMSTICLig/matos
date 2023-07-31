<template>
    <!--
        Premier bloc latéral : Choix Type Statistique
    -->
    <div class="card m-2">
        <div class="card-header" @click="show = !show">
            <h4>Choix Type Statistique</h4>
            <p v-if="!show" class="dropdown-toggle"> <small> Dépliez Moi en cliquant ! </small> </p>
            <p v-else class="dropdown-toggle"> <small> Repliez Moi en cliquant ! </small> </p>
        </div>
        <div v-if="show" class="card-body">
            <div class="form-check mb-1" @change="$emit('typeStat',statInput)">
                <input
                    :id="'statInput0'"
                    v-model="statInput"
                    type="radio"
                    class="form-check-input"
                    :value="'nb_emp'"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'statInput0'"
                    >
                    Nombre d'emprunts
                </label>
            </div>
            <div class="form-check mb-1" @change="$emit('typeStat',statInput)">
                <input
                    :id="'statInput1'"
                    v-model="statInput"
                    type="radio"
                    class="form-check-input"
                    :value="'d_moy_emp'"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'statInput1'"
                    >
                    Durée moyenne d'emprunt
                </label>
            </div>
            <div class="form-check mb-1" @change="$emit('typeStat',statInput)">
                <input
                    :id="'statInput2'"
                    v-model="statInput"
                    type="radio"
                    class="form-check-input"
                    :value="'freq_emp'"
                    @click="$emit('notChange')"
                />
                <label
                    class="form-check-label"
                    :for="'statInput2'"
                    >
                    Fréquence d'emprunts
                </label>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

    export default {
        emits: ['notChange','typeStat'],
        data() {
            return {
                show: true,
                statInput: ref()
            }
        }
    }
</script>