<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object && loaded">
        <div class="card-header">
          <h3 class="float-left" v-text="object.name"></h3>
          <div role="group" class="float-right">
            <div class="btn-group">
              <button
                class="btn btn-primary"
                type="button"
                @click="addMaterial(object)"
              >
                Ajouter
              </button>
              <router-link
                v-if="isManager"
                class="btn btn-primary"
                role="button"
                :to="editRoute"
                >Modifier</router-link
              >
              <div
                :class="show ? 'dropdown show' : 'dropdown'"
                @focusout="hide"
                style="margin-right: 10px;"
                v-if="isManager && filtered_entities.length"
                ref="dropcopy"
              >
                <div
                  class="btn btn-primary dropdown-toggle"
                  id="dropdownMenuButton"
                  @click="toggle"
                >
                  Copier
                </div>
                <div
                  :class="show ? 'dropdown-menu show' : 'dropdown-menu'"
                  :id="'tooltip' + _uid"
                  aria-labelledby="dropdownMenuButton"
                >
                  <button
                    class="dropdown-item"
                    v-for="item in filtered_entities"
                    :key="item.id"
                    @click="copyMaterial(item)"
                    type="button"
                  >
                    {{ item.name }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col col-12 col-md-6">
              <markdown
                :description="object.description"
                :displayed="displayed"
              ></markdown>
            </div>
          </div>
          <table class="table">
            <tr>
              <th scope="row">Ref interne</th>
              <td>{{ object.ref_int }}</td>
            </tr>
            <tr>
              <th scope="row">Ref fabricant</th>
              <td>{{ object.ref_man }}</td>
            </tr>
          </table>

          <p>
            <span><strong>Tags :&nbsp;</strong></span>
            <DisplayIdList fieldName="tags" :object="object" ressource="tags" />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Markdown from "@/components/Markdown";
import DisplayIdList from "@/components/DisplayIdList";
import { mapGetters, mapMutations } from "vuex";
import { showMsgOk } from "@/components/Modal";

/*
    Router vue matériel spécifique / générique
*/
export default {
  name: "MaterialInfos",
  components: {
    Markdown,
    DisplayIdList
  },

  data() {
    return {
      object: null,
      ressource: "",
      object_name: "Matériel",
      displayed: true,
      show: false,
      prefix: "",
      loaded: false
    };
  },
  computed: {
    ...mapGetters({
      tags: "tags/list",
      entityById: "entities/byId",
      entities: "entities/list"
    }),
    ...mapGetters(["authUser"]),
    isManager() {
      return this.authUser.entities.length || this.authUser.is_staff;
    },
    editRoute() {
      var name = "specificmaterial";
      if ("quantity" in this.object) {
        name = "genericmaterial";
      }
      return {
        name: name,
        params: { matid: this.object.id, entityid: this.object.entity }
      };
    },

    filtered_entities() {
      if (this.entities.length) {
        let ret = this.authUser.entities.slice(); //simple copy
        ret.splice(ret.indexOf(this.object.entity), 1);
        return ret.map(id => {
          console.log(id);
          return this.entityById(id);
        });
      } else {
        return [];
      }
    }
  },
  methods: {
    ...mapMutations({
      addMaterial: "loans/addMaterial"
    }),
    toggle(e) {
      e.preventDefault();
      this.show = !this.show;
    },
    hide(e) {
      if (!this.$refs.dropcopy.contains(e.relatedTarget)) {
        this.show = false;
      }
    },
    copyMaterial(entity) {
      /*
        Copie du matériel dans une entité gérée
      */
      var ressource = "";
      if (this.ressource == "genericmaterials") {
        ressource = "genericmaterials";
      }
      if (this.ressource == "specificmaterials") {
        ressource = "specificmaterials";
      }
      var prefix = "entities/" + entity.id + "/";

      this.$store
        .dispatch(ressource + "/create", {
          data: this.object,
          prefix: prefix
        })
        .then(() => {
          showMsgOk("le matériel a été ajouté à l'entité");
        })
        .catch(error => {
          if (error.response.data.non_field_errors) {
            showMsgOk(
              "La copie a échouée, vous avez déjà un matériel avec ce nom."
            );
          }
        });
    }
  },
  beforeMount() {
    var pall = [];
    pall.push(this.$store.dispatch("tags/fetchList"));

    if (this.$route.name == "specificmaterialitem") {
      this.ressource = "specificmaterials";
    }
    if (this.$route.name == "genericmaterialitem") {
      this.ressource = "genericmaterials";
    }
    if (parseInt(this.$route.params[this.$route.meta.routeparam], -1) != -1) {
      pall.push(
        this.$store
          .dispatch(this.ressource + "/fetchSingle", {
            id: this.$route.params[this.$route.meta.routeparam]
          })
          .then(data => {
            this.object = Object.assign({}, data);
          })
      );
    }
    if (this.isManager) pall.push(this.$store.dispatch("entities/fetchList"));

    Promise.all(pall).then(() => {
      this.loaded = true;
    });
  }
};
</script>
