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