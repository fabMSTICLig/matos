<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object">
        <div class="card-header">
          <h3 v-text="cardName"></h3>
        </div>
        <div class="card-body">
          <ul class="text-danger" v-show="emptyInstances">
            <li> Pour valider la création d'un matériel spécifique, veuillez ajouter des instances</li>
          </ul>
          <div class="form-row">
            <div class="col col-6 col-md-12 col-sm-12 col-lg-4">
              <form id="editor-form">
                <fieldset>
                  <legend>Informations</legend>
                  <div class="form-group">
                    <label>Nom</label
                    ><input
                      class="form-control"
                      type="text"
                      v-model="object.name"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label>Description</label
                    ><textarea
                      class="form-control"
                      v-model="object.description"
                    />
                    <a href="#" @click.prevent="showMessage">Aide</a>
                  </div>
                  <div class="form-group">
                    <label>Référence interne</label
                    ><input
                      class="form-control"
                      type="text"
                      v-model="object.ref_int"
                    />
                  </div>
                  <div class="form-group">
                    <label>Référence fabriquant</label
                    ><input
                      class="form-control"
                      type="text"
                      v-model="object.ref_man"
                    />
                  </div>
                  <div class="form-group">
                    <label>Localisation</label
                    ><input
                      class="form-control"
                      type="text"
                      v-model="object.localisation"
                    />
                  </div>
                  <div class="form-group">
                    <label>Tags</label>
                    <TagsInput
                      fieldName="tags"
                      :object="object"
                      ressource="tags"
                    />
                  </div>
                </fieldset>
              </form>
              <div class="btn-group" role="group">
                <button
                  v-if="is_new"
                  class="btn btn-primary"
                  type="button"
                  v-on:click="validateForm"
                >
                  Ajouter
                </button>
                <button
                  v-if="!is_new"
                  class="btn btn-primary"
                  type="button"
                  v-on:click="update(msg)"
                >
                  Modifier
                </button>
                <button
                  v-if="!is_new"
                  class="btn btn-danger"
                  type="button"
                  v-on:click="destroy"
                >
                  Supprimer
                </button>
              </div>
            </div>
            <div class="col-lg-8 col-md-12">
              <div class="row">
                <div class="col col-md-12 col-sm-12 col-lg-5">
                    <fieldset>
                      <legend>Instances</legend>
                      <form @submit="addObject" id="editor-instances">
                        <div class="input-group">
                          <div class="input-group-prepend">
                            <span class="input-group-text">Ajouter</span>
                          </div>
                          <input v-model="new_object_name" class="form-control" required />
                          <div class="input-group-append">
                            <button class="btn btn-primary" type="submit">
                              Valider
                            </button>
                          </div>
                        </div>
                      </form>
                      <ul class="list-group">
                        <li
                          class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                          v-for="item in objects_paginated"
                          :key="item.id"
                          v-on:click="selectObject(item)"
                          :class="{
                            active:
                              selected_object && item.id == selected_object.id
                          }"
                        >
                          <span>
                            {{ item.name }}
                          </span>
                          <button
                            class="btn btn-danger"
                            type="button"
                            @click="removeObject(item)"
                          >
                            X
                          </button>
                        </li>
                      </ul>
                      <pagination
                        :total-pages="pages_count"
                        :total="objects_list.length"
                        :per-page="per_page"
                        :current-page="current_page"
                        @pagechanged="onPageChange"
                      />
                    </fieldset>
                </div>
                <div class="col col-md-12 col-lg-5">
                    <div v-if="!is_new && selected_object">
                      <form @submit="updateInstance">
                        <fieldset>
                          <legend>Instance</legend>
                          <div class="form-group">
                            <label>Nom</label
                            ><input
                              class="form-control"
                              type="text"
                              v-model="selected_object.name"
                              required
                            />
                          </div>
                          <div class="form-group">
                            <label>Numéro série</label
                            ><input
                              class="form-control"
                              type="text"
                              v-model="selected_object.serial_num"
                            />
                          </div>
                          <div class="form-group">
                            <label>Description</label>
                            <textarea
                              class="form-control"
                              v-model="selected_object.description"
                            ></textarea>
                          </div>
                        </fieldset>
                        <div class="btn-group" role="group">
                          <button class="btn btn-primary" type="submit">
                            Modifier
                          </button>
                        </div>
                      </form>
                    </div>
                </div>
              </div>
              <div class="row mt-4">
                <div class="col col-lg-12 col-md-12">
                  <markdown
                    :description="object.description"
                    :showhelp="showHelp"
                    @hideHelp="showHelp = false"
                    v-if="object.description"
                  ></markdown>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { EditMixin } from "@/common/mixins";
import { showMsgOk } from "@/components/Modal";
import Pagination from "@/components/Pagination";
import TagsInput from "@/components/TagsInput";
import Markdown from "@/components/Markdown";

export default {
  name: "SpecificMaterialEdit",
  mixins: [EditMixin],
  components: {
    TagsInput,
    Pagination,
    Markdown
  },
  data() {
    return {
      ressource: "entities/specificMaterials",
      new_label: "Nouveau Matériel Spécifique",
      object_name: "Matériel",
      selected_object: null,
      current_page: 1,
      new_object_name: "",
      showHelp: false,
      msg: "mis à jour",
      errors: [],
      emptyInstances: null
    };
  },
  computed: {
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    },
    objects_list() {
      return this.$store.getters["entities/specificMaterials/instances/list"];
    },
    instancePrefix() {
      return (
        "entities/" +
        this.$route.params.entityid +
        "/specificmaterials/" +
        this.$route.params.matid +
        "/"
      );
    },
    objects_paginated() {
      return this.objects_list.slice(
        (this.current_page - 1) * process.env.VUE_APP_MAXLIST,
        this.current_page * process.env.VUE_APP_MAXLIST
      );
    },
    pages_count() {
      return Math.ceil(this.objects_list.length / process.env.VUE_APP_MAXLIST);
    },
    per_page() {
      return parseInt(process.env.VUE_APP_MAXLIST);
    }
  },
  methods: {
    get_empty() {
      return {
        name: "",
        ref_int: null,
        ref_man: null,
        localisation: null,
        description: "",
        entity: this.$route.params.entityid,
        tags: []
      };
    },
    validateForm() {
      this.create();
      this.emptyInstances = true;
      console.log(this.emptyInstances);
    },
    make_label() {
      return this.object.name;
    },
    initComponent() {
      if (this.is_new) {
        return Promise.resolve();
      } else {
        return this.$store
          .dispatch("entities/specificMaterials/instances/fetchList", {
            prefix: this.instancePrefix
          })
          .then(() => {
            if (this.objects_list.length > 0) {
              this.selectObject(this.objects_list[0]);
            }
          });
      }
    },
    onPageChange(page) {
      this.current_page = page;
    },
    removeObject(item) {
      this.$store
        .dispatch("entities/specificMaterials/instances/destroy", {
          id: item.id,
          prefix: this.instancePrefix
        })
        .then(() => {
          if (this.selected_object && this.selected_object.id == item.id)
            this.selected_object = null;
        });
    },
    addObject(e) {
      e.preventDefault();
      //if (document.querySelector("#editor-instances").checkValidity())
      if (this.new_object_name != "") {
        this.$store
          .dispatch("entities/specificMaterials/instances/create", {
            data: {
              name: this.new_object_name,
              model: this.object.id,
              serial_num: null
            },
            prefix: this.instancePrefix
          })
          .then(data => {
            this.new_object_name = "";
            this.selectObject(data);
          });
      }
    },
    selectObject(item) {
      this.selected_object = Object.assign({}, item);
    },
    updateInstance(e) {
      e.preventDefault();
      this.$store
        .dispatch("entities/specificMaterials/instances/update", {
          data: this.selected_object,
          id: this.selected_object.id,
          prefix: this.instancePrefix
        })
        .then(data => {
          this.selectObject(data);
          showMsgOk("Instance mise à jour");
        });
    },
    showMessage() {
      this.showHelp = true;
    }
  }
};
</script>
