<template>
<div class="row">
  <div class="col-12">
    <div class="card" v-if="object">
      <div class="card-header">
        <h3 v-text="cardName"></h3>
      </div>
      <div class="card-body">
        <form>
          <div class="form-row">
            <div class="col col-12 col-md-6 col-xl-4">
              <fieldset>
              <legend>Informations</legend>
              <div class="form-group"><label>Username</label><input class="form-control" type="text" v-model="object.username"></div>
              <div class="form-group"><label>Prénom</label><input class="form-control" type="text" v-model="object.first_name"></div>
              <div class="form-group"><label>Nom</label><input class="form-control" type="text" v-model="object.last_name"></div>
              <div class="form-group"><label>Email</label><input class="form-control" type="email" v-model="object.email"></div>
              <div class="form-group"><label>RGPD accept date</label><input class="form-control" type="date"
                  readonly v-model="object.rgpd_accept"></div>
              </fieldset>
            </div>
            <div class="col col-12 col-md-6 col-xl-4">
              <fieldset>
              <legend>Affiliations</legend>
              <div class="form-group">
                <DynList ressource="affiliations" v-model="object.affiliations" ></DynList> 
              </div>
              </fieldset>
            </div>
            <div class="col col-12 col-md-6 col-xl-4">
              <fieldset>
              <legend>Entités</legend>
              <div class="form-group">
                <div class="input-group">
                  <div class="input-group-prepend"><span class="input-group-text">Ajouter</span></div><input class="form-control"
                    type="text">
                  <div class="input-group-append"><button class="btn btn-primary" type="button">Ajouter</button></div>
                </div>
                <ul class="list-group">
                  <li class="list-group-item"><span class="float-left">FabMSTIC</span><button class="btn btn-danger float-right"
                      type="button"><i class="fa fa-remove"></i></button></li>
                  <li class="list-group-item"><span>List Group Item 2</span><button class="btn btn-danger float-right"
                      type="button"><i class="fa fa-remove"></i></button></li>
                  <li class="list-group-item"><span>List Group Item 3</span><button class="btn btn-danger float-right"
                      type="button"><i class="fa fa-remove"></i></button></li>
                </ul>
              </div>
              </fieldset>
            </div>
          </div>
          <div class="btn-group" role="group">
            <button v-if="is_new" class="btn btn-primary" type="button" v-on:click="create">Ajouter</button> 
            <button v-if="!is_new" class="btn btn-primary" type="button" v-on:click="update">Modifier</button>
            <button v-if="!is_new" class="btn btn-danger" type="button" v-on:click="destroy">Supprimer</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { EditMixin } from "@/common/mixins";
import DynList from "@/components/DynList";
export default {
  name: "UserEdit",
  mixins: [EditMixin],
    components: {
      DynList,
    },
  data() {
    return {
      ressource: "users",
      new_label: "Nouvel Utilisateur",
      object_name: "User",
    }
  },
  computed: {
  },
  methods: {
    get_empty(){
        return {
          username: "",
          first_name: "",
          last_name: "",
          email: "",
          affiliations: [],
        }

    },
    make_label(){
        return this.object.username;
    },
  },
};
</script>
