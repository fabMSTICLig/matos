
<template>
<div>
  <div class="row">
    <div class="col">
      <div class="card">
        <div class="card-header">
          <h4>Nouveau prêt</h4>
        </div>
        <div class="card-body">
          <form class="form">
            <div class="form-group"><label>Entité :</label><input type="text" class="form-control" :value="getEntityName(pending_loan.entity)"
                readonly /></div>
            <div class="form-group"><label>Status :</label>
                <select class="form-control" v-model="pending_loan.status">
                    <option v-for="(val,key) in status" v-text="val" :key="key" :value="key" ></option>
                </select>
            </div>
            <div class="form-group"><label>Date sortie :</label><input class="form-control" type="date" v-model="pending_loan.checkout_date"
              /></div>
            <div class="form-group"><label>Date retour :</label><input class="form-control" type="date" v-model="pending_loan.due_date"

              /></div>
            <div class="form-group"><label>Commentaire :</label><textarea class="form-control" v-model="pending_loan.comments"
></textarea></div>
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr class="d-flex">
                    <th class="col-7">Matériels</th>
                    <th class="col-4">Quantité</th>
                    <th class="col-1"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="d-flex" v-for="item in pending_loan.genericmaterials" :key="item.material" >
                    <td class="col-7">{{gmById(item.material).name}}</td>
                    <td class="col-4"><input type="number" class="form-control form-control" :value="item.quantity"
                      /></td>
                    <td class="col-1"><button class="btn btn-primary" type="button">X</button></td>
                  </tr>
                  <tr class="d-flex" v-for="item in pending_loan.models" :key="item">
                    <td class="col-7">{{smById(item).name}}</td>
                    <td class="col-4">
                      <div class="form-group">
                        <div class="input-group">
                          <div class="input-group-prepend"><span class="input-group-text">Instances</span></div><input
                            type="text" class="form-control" />
                          <div class="input-group-append"><button class="btn btn-primary" type="button">Ajouter</button></div>
                        </div>
                        <ul class="list-group">
                          <li class="list-group-item"><span class="float-left">LIG</span><button class="btn btn-danger float-right"
                              type="button"><i class="fa fa-remove"></i></button></li>
                        </ul>
                      </div>
                    </td>
                    <td class="col-1"><button class="btn btn-primary" type="button">X</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div role="group" class="btn-group"><button class="btn btn-primary" type="button">Envoyer</button>
              <button
                class="btn btn-danger" type="button">Vider</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
export default {
  name: "Loan",
  components: {
  },
  data() {
    return {
    };
  },
  computed: {
    ...mapGetters({
                    genericmaterials : "genericmaterials/list", 
                    gmById : "genericmaterials/byId", 
                    specificmaterials : "specificmaterials/list",
                    smById : "specificmaterials/byId",
                    entityById : "entities/byId",
                    authUser : "authUser", 
                    isAdmin : "isAdmin",
                    pending_loan : "loans/pending_loan",
                    status: "loans/status"}),
  },
  methods: {
    ...mapMutations({
      addMaterial: 'loans/addMaterial'
    }),
    getEntityName(id){
        if(id)
        {
          var entity = this.entityById(id)
          if(entity) return entity.name
        }
        else return ""
    },

  },
  beforeMount(){
   this.$store.dispatch("specificmaterials/fetchList")
   this.$store.dispatch("genericmaterials/fetchList")
   this.$store.dispatch("entities/fetchList")
   this.$store.dispatch("loans/fetchStatus")
  }
};
</script>
