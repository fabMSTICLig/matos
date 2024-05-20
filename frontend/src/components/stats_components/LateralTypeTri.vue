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