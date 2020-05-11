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
            <div class="col">
              <div class="form-group"><label>Name</label><input v-model="object.name" class="form-control"
                  type="text"></div>
              <div class="form-group"><label>Type</label>
                <select class="form-control">
                    <option v-for="(typename,type) in affiliation_types" value="type" v-text="typename" :key="type"></option>
                </select>
              </div>
            </div>
          </div>
          <div class="btn-group" role="group">
             <button v-if="is_new" class="btn btn-primary" type="button" v-on:click="create">Ajouter</button>
        
            <button v-if="!is_new" class="btn btn-primary" type="button" v-on:click="update">Modifier</button>
            <button v-if="!is_new" class="btn btn-danger" type="button">Supprimer</button>
          </div>
        </form>
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
import {PUSH_BREADCUMB, POP_BREADCUMB} from "@/store/actions.type";
export default {
    name: "AffiliaionEdit",
    components: {},
    data() {
        return {
            breadcumb: {},
            search_input: "",
            object: null,
        }
    },
    computed: {
        is_new(){
            return this.$route.path.indexOf('new')>-1;
        },
        cardName(){
            return this.is_new ? "Nouvelle Affiliation" : this.breadcumb.label;
        },
        ...mapGetters("affiliations", {
            affiliation_types: "types"
        }),
    },
    methods: {
        initObject(route){
            if (route.params.id == "new") {
                this.object = {
                    type: Object.keys(this.affiliation_types)[0],
                    name: ""
                }
                this.$store.dispatch(PUSH_BREADCUMB, {
                    label: 'Création',
                    url: route.path
                })
            } else if (parseInt(route.params.id, -1) != -1) {
                this.$store.dispatch('affiliations/fetchSingle', route.params.id).then((data) => {
                    this.object = Object.assign({}, data);
                    this.breadcumb = {
                        label: data.name,
                        url: route.path
                    };
                    this.$store.dispatch(PUSH_BREADCUMB, this.breadcumb)
                });
            }

        },
        update() {
            this.$store.dispatch('affiliations/update', {
                id: this.object.id,
                data: this.object
            }).then((data) => {
                this.object = Object.assign({}, data);
                console.log("affiliation" + ' updated');
                this.breadcumb.label = data.name;
                this.$bvModal.msgBoxOk("affiliation" + ' updated')
            })
        },
        create() {
            this.$store.dispatch('affiliations/create', this.object
                ).then((data) => {
                console.log("affiliation" + ' created');
                this.$bvModal.msgBoxOk("affiliation" + ' created')
                this.$router.push({ name: 'affiliation', params: { id: data.id } })
            });
        }
    },
    beforeMount() {
        this.$store.dispatch("affiliations/fetchTypes").then(() => {
            this.initObject(this.$route);
        });
    },
    beforeDestroy() {
        this.$store.dispatch(POP_BREADCUMB)
    },
    beforeRouteUpdate(to, from, next) {
        this.$store.dispatch(POP_BREADCUMB)
        this.initObject(to);
        next()
    }

};
</script>
