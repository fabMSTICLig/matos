<template>
   <div>
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
                        <button class="btn btn-danger" @click="deleteEquipment(equipment)"><i style="color:white" class="fa fa-trash"></i></button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
</template>

<script>
    import {mapGetters} from 'vuex'
   
   
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

        computed: {
            ...mapGetters([
                'equipments'
            ])
        }
    }

</script>