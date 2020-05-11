<template>
<div class="row">
  <div class="col-12 col-md-6">
    <div class="card">
      <div class="card-header"><input v-model="search_input" type="search" placeholder="Search"><router-link class="btn btn-primary float-right"
          role="button" :to="{name: 'affiliation', params: { id: 'new' }}" >Ajouter</router-link></div>
      <div class="card-body">
        <div class="table-responsive table-hover">
          <table class="table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Nom</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in affiliations_list" :key="item.id" v-on:click="selected_object=item">
                <td v-text="affiliation_types[item.type]"></td>
                <td v-text="item.name"></td>
              </tr>
            </tbody>
          </table>
        </div>
        <nav v-if="page_count>1"> 
          <ul class="pagination">
            <li class="page-item"><a class="page-link" href="#" aria-label="Previous"><span aria-hidden="true">«</span></a></li>
            <li class="page-item"><a class="page-link" href="#">1</a></li>
            <li class="page-item"><a class="page-link" href="#">2</a></li>
            <li class="page-item"><a class="page-link" href="#">3</a></li>
            <li class="page-item"><a class="page-link" href="#">4</a></li>
            <li class="page-item"><a class="page-link" href="#">5</a></li>
            <li class="page-item"><a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">»</span></a></li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
  <div class="col-12 col-md-6">
    <div class="card" v-if="selected_object" >
      <div class="card-header">
        <h3 class="float-left" v-text="selected_object.name"></h3>
        <div class="btn-group float-right" role="group"><router-link class="btn btn-primary" role="button" :to="{name: 'affiliation', params: { id: selected_object.id }}">Edit</router-link>
          <button
            class="btn btn-primary d-block d-md-none" type="button">Back</button>
        </div>
      </div>
      <div class="card-body">
        <p class="card-text">Type : {{affiliation_types[selected_object.type]}}</p>
      </div>
    </div>
  </div>
</div>
</template>

<script>
// @ is an alias to /src
import {
    mapGetters
} from "vuex";
export default {
    name: "AffiliaionList",
    components: {},
    data(){
        return{
            search_input:"",
            selected_object:null,
        } 
    },
    computed: {
        ...mapGetters('affiliations', {affiliations:'list', affiliation_types: 'types'}),
        affiliations_list() {
            return this.affiliations.filter(item => {
            return item.name.toLowerCase().indexOf(this.search_input.toLowerCase()) > -1;
            });
        },
        page_count(){
            return Math.floor(this.affiliations_list.length/10)+1;
        }
    },
    beforeMount() {
      this.$store.dispatch('affiliations/fetchTypes').then(()=>{
        this.$store.dispatch('affiliations/fetchList').then(()=>{
            if(this.affiliations.length>0)
            {   
               this.selected_object=this.affiliations[0];
            }
        });
      });
    }

};
</script>
