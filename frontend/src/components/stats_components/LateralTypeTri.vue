<template>
    <!--
        Second bloc latéral : Tri
    -->
    <div class="card m-2">
        <div class="card-header" @click="show = !show">
            <h4>Choix du Tri</h4>
            <p v-if="!show" class="dropdown-toggle"> <small> Dépliez Moi en cliquant ! </small> </p>
            <p v-else class="dropdown-toggle"> <small> Repliez Moi en cliquant ! </small> </p>
        </div>
        <div v-if="show" class="row">
            <div class="col-sm-6">
                <div class="card-body">
                    <div class="form-check mb-1" @change="$emit('typeTri',triInput)">
                        <input
                            :id="'triInput0'"
                            v-model="triInput"
                            type="radio"
                            class="form-check-input"
                            :value="0"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'triInput0'"
                            >
                            Affiliation
                        </label>
                    </div>
                    <div class="form-check mb-1" @change="$emit('typeTri',triInput)">
                        <input
                            :id="'triInput2'"
                            v-model="triInput"
                            type="radio"
                            class="form-check-input"
                            :value="2"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'triInput2'"
                            >
                            Objet
                        </label>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <div class="card-body">
                    <div class="form-check mb-1" @change="$emit('typeTri',triInput)">
                        <input
                            :id="'triInput1'"
                            v-model="triInput"
                            type="radio"
                            class="form-check-input"
                            :value="1"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'triInput1'"
                            >
                            Utilisateur
                        </label>
                    </div>
                    <div class="form-check mb-1" @change="$emit('typeTri',triInput)">
                        <input
                            :id="'triInput3'"
                            v-model="triInput"
                            type="radio"
                            class="form-check-input"
                            :value="3"
                            @click="$emit('notChange')"
                        />
                        <label
                            class="form-check-label"
                            :for="'triInput3'"
                            >
                            Tag
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
        emits: ['notChange','typeTri'],
        data() {
            return {
                show: true,
                triInput: ref()
            }
        }
    }
</script>