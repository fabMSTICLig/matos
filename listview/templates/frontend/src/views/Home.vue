<template>
   <div class="home">
       <div class="d-flex flex-wrap">
            <organization v-bind:organization="1"></organization>
       </div>
        <hr />
        <h4 class="text-center font-weight-bold">Equipments liste</h4>
            <table class="table table-striped">
                <thead>
                <tr>
                    <th scope="col">Title</th>
                    <th scope="col">Quantité</th>
                    <th scope="col">Categorie</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="equipment in equipments"
                    v-bind:key="equipment.id"
                >
                    <td>{{equipment.title}}</td>
                    <td>{{equipment.quantity}}</td>
                    <td>{{equipment.family}}</td>

                    <td>
                        <button class="btn btn-danger" @click="deleteEquipment(equipment)"><b-icon-trash></b-icon-trash></button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
</template>

<script>
    import {mapGetters} from 'vuex'
    import Organization from './Organization.vue'
   
   export default {
        name:"Home",
             

        methods: {
            deleteEquipment(equipment) {

                this.$store.dispatch('deleteEquipment', equipment)
            }

        },
        
        mounted() {
           this.$store.dispatch('fetchEquipments')
        },

        components: {
            Organization
        },
        computed: {
            ...mapGetters([
                'equipments'
            ])
        }
    }

</script>