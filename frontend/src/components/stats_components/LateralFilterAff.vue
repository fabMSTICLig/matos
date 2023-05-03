<template>
    <!--
        Cinquième bloc latéral : Filtrage par type d'affiliation
            Optionnel
    -->
    <div v-if="triValue == 0" class="card m-2">
        <div class="card-header" @click="show = !show">
            <h4>Choix du Filtrage par type d'affiliation</h4>
            <p v-if="!show" class="dropdown-toggle"> <small> Dépliez Moi en cliquant ! </small> </p>
            <p v-else class="dropdown-toggle"> <small> Repliez Moi en cliquant ! </small> </p>
        </div>
        <div v-if="show" class="row">
            <div class="col-sm-6">
                <div class="card-body">
                    <div class="form-check" @change="$emit('filterAff',filAffInput)">
                        <input
                            type="checkbox"
                            :id="'filAffInput0'"
                            class="form-check-input"
                            v-model="filAffInput"
                            :value="0"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'filAffInput0'"
                            >
                            Laboratoire
                        </label>
                    </div>
                    <div class="form-check" @change="$emit('filterAff',filAffInput)">
                        <input
                            type="checkbox"
                            :id="'filAffInput2'"
                            class="form-check-input"
                            v-model="filAffInput"
                            :value="2"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'filAffInput2'"
                            >
                            Plateforme
                        </label>
                    </div>
                    <div class="form-check" @change="$emit('filterAff',filAffInput)">
                        <input
                            type="checkbox"
                            :id="'filAffInput4'"
                            class="form-check-input"
                            v-model="filAffInput"
                            :value="4"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'filAffInput4'"
                            >
                            Recherche
                        </label>
                    </div>
                    <div class="form-check" @change="$emit('filterAff',filAffInput)">
                        <input
                            type="checkbox"
                            :id="'filAffInput6'"
                            class="form-check-input"
                            v-model="filAffInput"
                            :value="'Naff'"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'filAffInput6'"
                            >
                            Sans Affiliation
                        </label>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <div class="card-body">
                    <div class="form-check" @change="$emit('filterAff',filAffInput)">
                        <input
                            type="checkbox"
                            :id="'filAffInput1'"
                            class="form-check-input"
                            v-model="filAffInput"
                            :value="1"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'filAffInput1'"
                            >
                            Ecole
                        </label>
                    </div>
                    <div class="form-check" @change="$emit('filterAff',filAffInput)">
                        <input
                            type="checkbox"
                            :id="'filAffInput3'"
                            class="form-check-input"
                            v-model="filAffInput"
                            :value="3"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'filAffInput3'"
                            >
                            Service
                        </label>
                    </div>
                    <div class="form-check" @change="$emit('filterAff',filAffInput)">
                        <input
                            type="checkbox"
                            :id="'filAffInput5'"
                            class="form-check-input"
                            v-model="filAffInput"
                            :value="5"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'filAffInput5'"
                            >
                            Composante Universitaire
                        </label>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

    export default {
        props: ['triValue'],
        emits: ['notChange','filterAff'],
        data() {
            return {
                show: false,
                filAffInput: ref(["0","1","2","3","4","5","Naff"])
            }
        }
    }
</script>