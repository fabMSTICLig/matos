<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object && filter_entities && loaded">
        <div class="card-header">
          <h3 class="float-left" v-text="object.name"></h3>
          <div role="group" class="float-right">
            <div class="input-group">
              <button
                class="btn btn-primary input-group-append"
                type="button"
                @click="addMaterial(object)"
              >
                Ajouter
              </button>
              <div
                :class="
                  show
                    ? 'dropdown show input-goup-append'
                    : 'dropdown input-group-append'
                "
                @focusout="hide"
                style="margin-right: 10px;"
                v-if="isManager && filter_entities.length"

              >

                <div
                  class="btn btn-primary dropdown-toggle"
                  id="dropdownMenuButton"
                  @click="toogle"
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
                    v-for="item in filter_entities"
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
      entities: [],
      show: false,
      prefix: "",
      loaded: false,
      filter_entities:[]
    };
  },
  computed: {
    ...mapGetters({
      tags: "tags/list",
      pending_loan: "loans/pending_loan"
    }),
    ...mapGetters(["authUser"]),
    materialTags() {
      return this.tags.filter(item => {
        return this.object["tags"].includes(item.id);
      });
    },
    isManager() {
      return this.authUser.entities.length || this.authUser.is_staff;
    }
  },
  methods: {
    ...mapMutations({
      addMaterial: "loans/addMaterial"
    }),
    make_label() {
      return this.object.name;
    },
    toogle(e) {
      e.preventDefault();
      this.show = !this.show;
    },
    hide(e) {
      if (!this.$el.contains(e.relatedTarget)) {
        this.show = false;
      }
    },
    get_entities() {
      var prefix = "";
      var filtered = "";
      let self = this;
      if (this.entities.length) {
          filtered = this.entities.filter(entity => {
          return this.authUser.entities.find(
            managed => managed == entity.id && managed != this.object.entity
          );

        });
        if (this.authUser.is_staff) {
          filtered = this.entities.filter(entity => {
            return entity.id != this.object.entity;
          });
        }

        if(filtered.length){

          filtered.forEach(entity => {
            if (this.ressource == "specificmaterials") {
              prefix = "entities/specificMaterials/instances";
            }
            if (this.ressource == "genericmaterials") {
              prefix = "entities/genericMaterials";
            }

            this.$store
              .dispatch(prefix + "/getMaterials", {
                id: entity.id
              })
              .then(materials => {
                let presentMaterial = materials.filter(material => {
                  return material.name == this.object.name;
                });

                if (!presentMaterial.length) {
                  self.filter_entities.push(entity);
                }
              });
          });
          self.loaded = true;
        }

      }
      self.loaded = true;

    },
    copyMaterial(entity) {
      var ressource = "";
      if (this.ressource == "genericmaterials") {
        ressource = "entities/genericMaterials";
      }
      if (this.ressource == "specificmaterials") {
        ressource = "entities/specificMaterials";
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
          // eslint-disable-next-line
          console.log(JSON.stringify(error));
        });
    }
  },
  beforeMount() {

    var pall = [];
    pall.push(this.$store.dispatch("specificmaterials/fetchList"));
    pall.push(this.$store.dispatch("tags/fetchList"));


    if (this.$route.name == "specificmaterialitem") {
      this.ressource = "specificmaterials";
    }
    if (this.$route.name == "genericmaterialitem") {
      this.ressource = "genericmaterials";
    }
    if (parseInt(this.$route.params[this.$route.meta.routeparam], -1) != -1) {
      pall.push(this.$store
        .dispatch(this.ressource + "/fetchSingle", {
          id: this.$route.params[this.$route.meta.routeparam]
        })
        .then(data => {
          this.object = Object.assign({}, data);
        }));
    }
    pall.push(this.$store.dispatch("entities/fetchList").then(data => {
      this.entities = data;
    }));

    Promise.all(pall).then(() => {
      this.get_entities()
    })
  }
};
</script>
