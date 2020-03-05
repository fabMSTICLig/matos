<template>
        <form action="" @submit="createEquipment(equipment)">
            <h4 class="text-center font-weight-bold">Post creation form</h4>
            <div class="form-group">
                <input type="text" placeholder="Post title" v-model="equipment.title" class="form-control">

            </div>
           
            <div class="form-group">
                <input type="text" v-model="equipment.sku" placeholder="Equipment stock" class="form-control">
            </div>
             <div class="form-group">
                <input type="text" v-model="equipment.barcode" placeholder="Equipment barcode" class="form-control">
            </div>
             <div class="form-group">
                <input type="text" v-model="equipment.refUsine" placeholder="ref fabricant" class="form-control">
            </div>
            <div class="form-group">
                <input type="text" v-model="equipment.description" placeholder="Description" class="form-control">
            </div>
             <div class="form-group">
                <input type="number" v-model="equipment.location" placeholder="Organisation" class="form-control">
            </div>
             <div class="form-group">
                <input type="number" v-model="equipment.family" placeholder="Categorie" class="form-control">
            </div>
            
            <div class="form-group">
                <button :disabled="!isValid" class="btn btn-block btn-primary" @click.prevent="createEquipment(equipment)">Submit
                </button>
            </div>
        </form>
    </template>

    <script>

        export default {
            name: "CreateEquipment",
            data() {
                return {
                    equipment: {
                        title: '',
                        quantity: ''
                    }
                }
            },
            
            methods: {
                createEquipment(equipment) {
                    this.$store.dispatch('createEquipment', equipment)
                }
            },
            computed: {
                isValid() {
                    return this.equipment.title !== '' && this.equipment.sku !== ''
                }
            }
        }
    </script>

    <style scoped>

    </style>