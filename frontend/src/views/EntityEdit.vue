<template>
  <div>
    <div class="card" v-if="object">
      <div class="card-header">
        <h3 class="float-left" v-text="cardName"></h3>
        <div v-if="!is_new" class="btn-group float-right" role="group">
          <router-link
            class="btn btn-primary"
            role="button"
            :to="{
              name: 'materialslist',
              params: { entityid: object.id },
            }"
            >Matériels</router-link
          >
          <router-link
            class="btn btn-primary"
            role="button"
            :to="{
              name: 'entityloans',
              params: { entityid: object.id },
            }"
            >Prêts</router-link
          >
        </div>
      </div>
      <div class="card-body">
        <form id="editor-form">
          <div class="form-row">
            <div class="col col-md-6 col-lg-6 col-xs-10 col-sm-12">
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
                  <label>Contact</label
                  ><input
                    class="form-control"
                    type="email"
                    v-model="object.contact"
                    required
                  />
                </div>
                <div class="form-group">
                  <label>Description</label>
                  <textarea
                    class="form-control"
                    v-model="object.description"
                  ></textarea>
                  <a href="#" @click.prevent="showMessage">Aide</a>
                </div>
              </fieldset>
            </div>

            <div class="md col-12 col-md-6 col-lg-6">
              <markdown
                :description="object.description"
                :showhelp="showHelp"
                @hideHelp="showHelp = false"
              ></markdown>
            </div>

            <div class="col col-12 col-md-6">
              <fieldset>
                <legend>Managers</legend>
                <div class="form-group">
                  <div :id="_uid">
                    <div class="input-group" style="height: 43px">
                      <multiselect
                        :value="managers"
                        :options="userslist"
                        :multiple="true"
                        track-by="id"
                        :custom-label="makeManagerLabel"
                        label="name"
                        hide-selected
                        placeholder="Rentrer au moins 3 lettres"
                        :reset-after="true"
                        @select="addManager"
                        @search-change="searchChange"
                        ><template slot="tag"><span></span></template>
                      </multiselect>
                    </div>
                  </div>
                  <ul class="list-group">
                    <li
                      class="
                        list-group-item
                        d-flex
                        justify-content-between
                        align-items-center
                      "
                      v-for="item in managers"
                      :key="item.id"
                    >
                      <span>
                        <strong>@{{ item.username }} :</strong>
                        {{ item.first_name }}
                        {{ item.last_name }}
                      </span>
                      <button
                        class="btn btn-danger"
                        type="button"
                        @click="removeManager(item)"
                      >
                        X
                      </button>
                    </li>
                  </ul>
                </div>
              </fieldset>
            </div>
            <div class="col col-12 col-md-6">
              <fieldset>
                <legend>Affiliations</legend>
                <div class="form-group">
                  <DynList
                    options="affiliations"
                    v-model="object.affiliations"
                  ></DynList>
                </div>
              </fieldset>
            </div>
          </div>
          <div class="btn-group" role="group">
            <button
              v-if="is_new"
              class="btn btn-primary"
              type="button"
              v-on:click="create"
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
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { EditMixin } from "@/common/mixins";
import DynList from "@/components/DynList";
import Markdown from "@/components/Markdown";
import Multiselect from "vue-multiselect";

/*
  Vue Edition d'une Entité
*/
export default {
  name: "EntityEdit",
  mixins: [EditMixin],
  components: {
    DynList,
    Markdown,
    Multiselect,
  },
  data() {
    return {
      ressource: "entities",
      new_label: "Nouvelle Entité",
      object_name: "Entité",
      showHelp: false,
      msg: "mise à jour",
      userslist: [],
    };
  },
  computed: {
    ...mapGetters({
      users: "users/list",
    }),
    managers() {
      return this.userslist.filter((el) =>
        this.object.managers.includes(el.id)
      );
    },
  },
  methods: {
    get_empty() {
      return {
        name: "",
        description: "",
        contact: "",
        affiliations: [],
        managers: [],
      };
    },
    searchUser(query) {
      this.$store
        .dispatch("users/fetchList", {
          params: { params: { search: query } },
        })
        .then((data) => {
          data.forEach((user) => {
            if (this.userslist.findIndex((u) => u.id == user.id) === -1) {
              this.userslist.push(user);
            }
          });
        });
    },
    addManager(item) {
      this.object.managers.push(item.id);
    },
    removeManager(item) {
      const index = this.object.managers.indexOf(item.id);
      if (index > -1) {
        this.object.managers.splice(index, 1);
      }
    },

    make_label() {
      return this.object.name;
    },
    makeManagerLabel(item) {
      return item.first_name + " " + item.last_name;
    },
    showMessage() {
      this.showHelp = true;
    },
    searchChange(query) {
      this.$store
        .dispatch("users/fetchList", {
          params: { params: { search: query } },
        })
        .then((data) => {
          data.forEach((user) => {
            const index = this.userslist.findIndex((u) => u.id == user.id);
            if (index == -1) {
              this.userslist.push(user);
            }
          });
        });
    },
  },
  beforeMount() {
    this.$store.dispatch("users/fetchList").then((data) => {
      data.forEach((user) => this.userslist.push(user));
    });
  },
};
</script>
