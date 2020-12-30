<template>
  <div v-if="loaded">
    <div class="row">
      <div class="col">
        <div class="card">
          <div class="card-header">
            <h4 class="float-left">{{ title }}</h4>
            <div class="btn-group float-right" role="group">
              <router-link
                class="btn btn-primary"
                role="button"
                :to="{
                  name: 'entityloans',
                  params: { entityid: pending_loan.entity }
                }"
                v-if="updateMode && canManage"
                >Retour entité</router-link
              >
              <router-link
                class="btn btn-primary"
                role="button"
                :to="{
                  name: 'authloans'
                }"
                v-if="updateMode && !canManage"
                >Mes prêts</router-link
              >
            </div>
          </div>
          <div class="card-body">
            <ul class="text-danger" v-show="errors.length != 0">
              <li
                v-for="error in errors"
                :key="error"
                v-text="error"
                tabIndex="-1"
              ></li>
            </ul>
            <form class="form" @submit="submitLoan">
              <div class="form-row">
                <div class="col-12 col-md-5 col-lg-5">
                  <div class="form-group" v-if="canManage">
                    <label>Utilisateur :</label>
                    <input-datalist
                      v-model="pending_loan.user"
                      ressource="users"
                      :makeLabel="makeUserLabel"
                    ></input-datalist>
                  </div>
                  <div class="form-group">
                    <label>Entité :</label>
                    <input
                      type="text"
                      class="form-control"
                      :value="entityById(pending_loan.entity) | field('name')"
                      readonly
                    />
                  </div>
                  <div class="form-group">
                    <label>Status :</label>
                    <select class="form-control" v-model="pending_loan.status" :disabled="!canManage">
                      <option
                        v-for="(val, key) in status"
                        v-text="val"
                        :key="key"
                        :value="key"
                      ></option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Date sortie :</label>
                    <input
                      class="form-control"
                      type="date"
                      v-model="pending_loan.checkout_date"
                      required
                      :disabled="readOnly"
                    />
                  </div>
                  <div class="form-group">
                    <label>Date retour prévue:</label>
                    <input
                      class="form-control"
                      type="date"
                      v-model="pending_loan.due_date"
                      required
                      :disabled="readOnly"
                    />
                  </div>
                  <div class="form-group" v-if="canManage">
                    <label>Date retour:</label>
                    <input
                      class="form-control"
                      type="date"
                      v-model="pending_loan.return_date"
                    />
                  </div>

                  <div class="form-group">
                    <label>Commentaire :</label>
                    <textarea
                      class="form-control"
                      v-model="pending_loan.comments"
                      :disabled="readOnly"
                    ></textarea>
                  </div>
                </div>
                <div class="col-12 col-md-7">
                  <p class="text-danger" v-show="emptyLoan">
                    Votre prêt doit contenir au moins un matériel. Pour un
                    materiel spécifique veuillez choisir une instance
                  </p>

                  <div class="table-responsive-md">
                    <table class="table">
                      <thead>
                        <tr class="d-flex">
                          <th class="col-8">Matériels</th>
                          <th class="col-3">Quantité</th>
                          <th class="col-1"></th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          class="d-flex"
                          v-for="item in pending_loan.generic_materials"
                          :key="'g' + item.material"
                        >
                          <td class="col-8 disabled">
                            {{ gmById(item.material) | field("name") }}
                          </td>
                          <td class="col-3 disabled">
                            <input
                              type="number"
                              min="1"
                              max="10000"
                              class="number-input form-control form-control"
                              v-model="item.quantity"
                              :disabled="readOnly"
                              v-on:change="checkQuantities()"
                            />
                          </td>

                          <td class="col-1 disabled">
                            <button
                              v-if="!readOnly"
                              class="btn btn-danger"
                              type="button"
                              @click="removeMaterial(gmById(item.material))"
                              style="margin-left: -10px;"
                            >
                              X
                            </button>
                          </td>
                        </tr>
                        <tr
                          class="d-flex"
                          v-show="maxQuantities.length"
                          v-for="material_loan in maxQuantities"
                          :key="material_loan.id"
                        >
                          <td class="col-7" v-if="material_loan.quantity > 0">
                            <span class="text-danger"
                              >Quantité disponible dépassée : {{ material_loan.quantity }}
                            </span>
                          </td>
                          <td class="col-7" v-if="material_loan.quantity == 0">
                            <span class="text-danger"
                              >Matériel indisponible
                            </span>
                          </td>
                          <td class="col-5">
                            <span class="text-danger float-right">{{
                              material_loan.name
                            }}</span>
                          </td>
                        </tr>
                        <tr
                          class="d-flex"
                          v-show="disabled.length"
                          v-for="material in disabled"
                          :key="material.id"
                        >
                          <td class="col-6">
                            <span class="text-danger"
                              >Matériel indisponible :
                            </span>
                          </td>
                          <td class="col-6">
                            <span class="text-danger float-right">{{
                              material.name
                            }}</span>
                          </td>
                        </tr>
                        <tr
                          class="d-flex"
                          v-for="item in pending_loan.models"
                          :key="'s' + item"
                        >
                          <td class="col-11" colspan="2">
                            {{ smById(item) | field("name") }}
                            <div>
                              <h6>Instances</h6>
                              <DynList
                                v-if="item in specificinstances"
                                :ressource="specificinstances[item]"
                                v-model="pending_loan.specific_materials"
                                :readonly="readOnly"
                              ></DynList>
                            </div>
                          </td>

                          <td>
                            <button
                              v-if="!readOnly"
                              class="btn btn-danger"
                              type="button"
                              @click="removeMaterial(smById(item))"
                              style="margin-left: -10px;"
                            >
                              X
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div
                    class="form-group"
                    v-if="
                      updateMode &&
                        (pending_loan.child ||
                          pending_loan.parent ||
                          pending_loan.status == 3) &&
                        makeChild_btn
                    "
                  >
                    <label>Historique :</label>
                    <div class>
                      <div role="group" class="btn-group">
                        <button
                          v-if="updateMode && pending_loan.parent"
                          class="btn btn-info"
                          type="button"
                          @click="goTo(pending_loan.parent)"
                        >
                          Précédent
                        </button>
                        <button
                          v-if="
                            updateMode &&
                              canManage &&
                              !pending_loan.child &&
                              pending_loan.status == 3
                          "
                          class="btn btn-info"
                          type="button"
                          @click="makeChild"
                        >
                          Créer un successeur
                        </button>

                        <button
                          v-if="updateMode && pending_loan.child"
                          class="btn btn-info"
                          type="button"
                          @click="goTo(pending_loan.child)"
                        >
                          Suivant
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12">
                <div role="group" class="btn-group">
                  <button
                    class="btn btn-primary float-left"
                    type="submit"
                    v-if="!readOnly"
                  >
                    {{ updateMode ? "Modifier" : labelSubmit }}
                  </button>
                  <button
                    v-if="!updateMode"
                    class="btn btn-danger"
                    type="button"
                    @click="cleanMaterials"
                  >
                    Vider
                  </button>
                </div>
                <div role="group" class="btn-group float-right">
                  <button
                    v-if="updateMode"
                    class="btn btn-danger"
                    type="button"
                    @click="newLoan"
                  >
                    Nouveau prêt
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { mapGetters, mapMutations } from "vuex";
import DynList from "@/components/DynList";
import { showMsgOk } from "@/components/Modal";
import InputDatalist from "@/components/InputDatalist";
/*
  Composant permettant de gérer le prêt courant
*/
export default {
  name: "Loan",
  components: {
    DynList,
    InputDatalist
  },
  data() {
    return {
      specificinstances: {},
      loaded: false,
      errors: [],
      prevRoute: null,
      makeChild_btn: false,
      selected: [],
      maxQuantities: [],
      genericMaterialsLoan: [],
      disabled: [],
      idRoute: ""
    };
  },
  computed: {
    ...mapGetters({
      genericmaterials: "genericmaterials/list",
      gmById: "genericmaterials/byId",
      specificmaterials: "specificmaterials/list",
      smById: "specificmaterials/byId",
      entityById: "entities/byId",
      loanById: "loans/byId",
      pending_loan: "loans/pending_loan",
      status: "loans/status",
      authUser: "authUser",
      isAdmin: "isAdmin",
    }),
    loanMessageSent() {
      if (this.pending_loan.status == 2) return "La demande a été envoyée";
      if (this.pending_loan.status == 3) return "La demande a été acceptée";
      if (this.pending_loan.status == 4) return "La demande a été refusée";
      if (this.pending_loan.status == 1) return "La demande a été annulée";

      return "La demande a été envoyée";
    },
    labelSubmit() {
      if (this.canManage && !this.updateMode) {
        return "Créer";
      } else {
        return "Envoyer la demande";
      }
    },

    emptyLoan() {
      return (
        this.pending_loan.generic_materials.length == 0 &&
        this.pending_loan.specific_materials.length == 0
      );
    },

    emptyInstances() {
      return this.pending_loan.models.length
        ? this.pending_loan.specific_materials.length == 0
        : false;
    },
    canManage() {
      return (
        this.isAdmin ||
        this.authUser.entities.indexOf(this.pending_loan.entity) > -1
      );
    },
    updateMode() {
      return "id" in this.pending_loan;
    },
    readOnly() {
      return (
        !this.canManage &&
        (this.pending_loan.status != 2)
      );
    },
    title() {
      return this.readOnly
        ? "Consulter prêt"
        : this.updateMode
        ? "Modification prêt"
        : "Nouveau prêt";
    },
    checkDates() {
      /*
        Vérification des dates remplies pour la demande ou la modification 
      */
      return ((this.pending_loan.checkout_date !== null && this.pending_loan.checkout_date !=="") && (this.pending_loan.due_date !== null && this.pending_loan.due_date !== ""))
                        || ((this.pending_loan.checkout_date !==  null && this.pending_loan.checkout_date !== "") && (this.pending_loan.return_date !== null && this.pending_loan.return_date !== ""));
    }
  },
  watch: {
    /*
      Disponibilité d'un matériel spécifique si modification d'Instances
    */
    'pending_loan.specific_materials': {
      handler() {
        if(this.checkDates) {
          if(this.pending_loan.specific_materials.length) {
            this.getMaterialAvailability();
          }
        }
      },
      deep: true
    },
    /*
      Vérification de la disponibilité et quantité des matériels aux changements de dates
    */
    'pending_loan.checkout_date': {
      handler() {
        this.maxQuantities = [];
        if(this.checkDates) {
          if(this.pending_loan.specific_materials.length) {
            this.getMaterialAvailability();
          }
          this.checkQuantities();
        }
      },
      deep: true
    },
    'pending_loan.due_date': {
      handler() {
        this.maxQuantities = [];
        if(this.checkDates) {
          if(this.pending_loan.specific_materials.length) {
            this.getMaterialAvailability();
          }
          this.checkQuantities();
        }
      },
      deep: true

    },
    'pending_loan.return_date': {
      handler() {
        this.maxQuantities = [];
        if(this.checkDates) {
          if(this.pending_loan.specific_materials.length) {
            this.getMaterialAvailability();
          }
          this.checkQuantities();
        }
      }
    },
    pending_loan: {

      handler() {
          /*
            Changement du prêt courant pour un utilisateur
            Attribution des status en fonction de l'état du prêt
            Vérification des quantité de matériels disponible
          */
          if (!this.canManage) {
          
            this.status = {};
            var keys = [1, 2];
            var values = ["Annulé", "Demandé"];

            if (this.pending_loan.status == 2 || this.pending_loan.status == 1) {
              for (var i = 0; i < keys.length; i++) {
                this.status[keys[i]] = values[i];
              }
            }
            else if (this.pending_loan.status == 3) {
              this.status[3] = "Accepté";
            }
            else if (this.pending_loan.status == 4 ) {
              this.status[4] = "Refusé";
            }
          }
        this.checkQuantities();
        this.$store.commit("loans/savePending");
      },
      deep: true
    },
    "$route.params.loanid": {
      handler: function(loanid) {
        /*
          Synchronisation du prêt courant avec la dernière version
          Redirection vers le prêt
        */
        this.idRoute = loanid;
        this.loaded=false;
        if (loanid) {
          this.$store.dispatch("loans/list").then(loans => {
            let pending_loan = loans.find(loan => loan.id == loanid);
            if (pending_loan) {
              this.goTo(pending_loan.id);
            }
          });
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    ...mapMutations({
      removeMaterial: "loans/removeMaterial"
    }),

    initInstances(item) {
      return this.$store
        .dispatch("specificmaterials/instances/fetchList", {
          prefix: "specificmaterials/" + item + "/"
        })
        .then(data => {
          Vue.set(this.specificinstances, item, data);
        });
    },
    getMaterialAvailability() {
      /*
        Vérification de la disponibilité de chaque matériel spécifique inclut dans le prêt
      */
      this.disabled = [];
      for(let i=0; i<= this.pending_loan.specific_materials.length-1;i++) {
        let specificinstance_id = this.pending_loan.specific_materials[i];

        let instances = Object.keys(this.specificinstances).filter(instances => {
           return Object.values(this.specificinstances[instances]).find(object => object.id == specificinstance_id)
        });
        let model = instances[0];
        let item = { "specificinstance":specificinstance_id, "model":model };
        this.setMaterialAvailability(item)
      }
    },
    submitLoan(e) {
      e.preventDefault();
      this.checkErrors();
      if (this.errors.length) {
        window.scrollTo(0, 0);
      }
      if (
        !this.emptyLoan &&
        !this.errors.length &&
        !this.emptyInstances &&
        !this.maxQuantities.length
      ) {
        if (this.pending_loan.return_date == "")
          this.pending_loan.return_date = null;

        if (this.updateMode) {
          this.$store
            .dispatch("loans/update", {
              data: this.pending_loan,
              id: this.pending_loan.id
            })
            .then(data => {
              if (this.pending_loan.status == 1) {
                showMsgOk("La demande de prêt a été supprimée");
                this.newLoan();
              } else {
                this.$store.commit("loans/setPending", data);
                showMsgOk("Le prêt a été modifié");
              }
              if (this.pending_loan.status == 3) {
                this.makeChild_btn = true;
              }
              this.errors = [];
            })
            .catch(e => {
              if ("non_field_errors" in e.response.data) {
                this.errors = e.response.data.non_field_errors;
                window.scrollTo(0, 0);
              }
              // eslint-disable-next-line
                console.log(e.response);
            });
        } else {
          if (this.pending_loan.user == null) {
            this.pending_loan.user = this.authUser.id;
          }
          if (this.pending_loan.status == null) {
            this.pending_loan.status = 2;
          }
          this.$store
            .dispatch("loans/create", { data: this.pending_loan })
            .then(data => {
              this.$store.commit("loans/setPending", data);
              showMsgOk(this.loanMessageSent);
              this.errors = [];
            })
            .catch(e => {
              if ("non_field_errors" in e.response.data) {
                this.errors = e.response.data.non_field_errors;
                window.scrollTo(0, 0);
              }
              this.errors = [];
              this.errors.push(
                e.response.data.non_field_errors
                  ? e.response.data.non_field_errors[0]
                  : e.response.data
              );
              console.log(this.errors);
              window.scrollTo(0, 0);
              // eslint-disable-next-line
              console.log(e.response);
            });
        }
      }
    },
    checkErrors() {
      this.errors = [];
      if (!this.pending_loan.user && this.canManage) {
        this.errors.push("Un utilisateur doit être assigné");
      }
      if (this.pending_loan.checkout_date > this.pending_loan.due_date) {
        this.errors.push(
          "la date de sortie doit être antérieure à celle du retour prévu"
        );
      }
      if (
        this.pending_loan.return_date &&
        this.pending_loan.checkout_date > this.pending_loan.return_date
      ) {
        this.errors.push(
          "la date de sortie doit être antérieure à celle du retour"
        );
      }
      if (this.emptyInstances) {
        this.errors.push(
          "Veuillez sélectionner une instance pour le matériel spécifique"
        );
      }
    },
    cleanMaterials() {
      this.$store.commit("loans/resetPending");
      this.$store.commit("loans/cleanMaterials");
      this.maxQuantities=[];
    },
    newLoan() {
      this.$store.commit("loans/resetPending");
      this.maxQuantities=[];

    },
    makeUserLabel(item) {
      return item.username;
    },
    goTo(id) {
      this.$store.dispatch("loans/fetchSingle", { id: id }).then(data => {
        this.$store.commit("loans/setPending", data);
        this.pending_loan.models.forEach(item => {
          this.initInstances(item);
        });
      });
    },
    makeChild() {
      this.$store
        .dispatch("loans/makeChild", { id: this.pending_loan.id })
        .then(data => {
          this.goTo(data.id);
        });
    },
    checkQuantities() {
      /*
        Passage des quantités maximales dans un tableau
        Vérification dépassement du stock et retrait du tableau sinon
      */
      for(let i=0; i<= this.pending_loan.generic_materials.length-1;i++) {
        let itemgeneric = this.pending_loan.generic_materials[i]
        let genericMaterial = this.genericmaterials.find( material => material.id == itemgeneric.material)

        /*
          Vérification sans le cas ou le stock est à zero
        */
        if(this.checkDates && genericMaterial.quantity !== 0) {

          this.setMaterialAvailability(itemgeneric);
        }
  
        if(parseInt(itemgeneric.quantity) <= genericMaterial.quantity) {
          let index = this.maxQuantities.indexOf(Object.values(this.maxQuantities).find( obj => obj.id == genericMaterial.id));
          if(index > -1) {
           this.maxQuantities.splice(index,1)
          }
        }

        if((parseInt(itemgeneric.quantity) > genericMaterial.quantity) && genericMaterial.quantity > 0 ) {
          let index = this.maxQuantities.indexOf(Object.values(this.maxQuantities).find( obj => obj.id == genericMaterial.id));
         
          if(index == -1) {
           this.maxQuantities.push(genericMaterial);
          }

        }
      }
    },
    setMaterialAvailability(item) {

      /*
        Passage de la disponibilité d'un matériel ou de la quantité disponible
      */

      // Affectation d'une variable id du prêt pour l'exclure de la recherche si prêt existant
     
      let id_loan=""
      
      if(this.pending_loan.id) {
        id_loan = this.pending_loan.id
      }

      if(item.quantity) {
        this.$store.dispatch("entities/genericMaterials/getMaterialAvailability", {
          id_entity: this.pending_loan.entity,
          id_mat: item.material,
          data: { "checkout_date": this.pending_loan.checkout_date,"due_date": this.pending_loan.due_date, "id_loan": id_loan }

        }).then(data => {
         
          let genericMaterial = this.genericmaterials.find( material => material.id == data.id_mat)
         
          if(genericMaterial) {

            if((parseInt(item.quantity) > data.quantity) && (genericMaterial.quantity > 0 )) {
              let material = {};
              material["name"] = genericMaterial.name;
              material["quantity"] = data.quantity;
              material["id"] = genericMaterial.id
              if(!this.maxQuantities.find(item => item.id == genericMaterial.id)){
                this.maxQuantities.push(material);
              }
            }
          }
        });
      } else {
        
        let specificinstance_id = item.specificinstance;
        let model = item.model
        
        this.$store.dispatch("entities/specificMaterials/getMaterialAvailability", {
          id_entity: this.pending_loan.entity,
          id_model: model,
          id_instance: specificinstance_id,
          data: { "checkout_date": this.pending_loan.checkout_date,"due_date": this.pending_loan.due_date, "id_loan": id_loan }

        }).then(data => {

            if(data == false) {
              let specificinstance = this.specificinstances[model].find( m => m.id == specificinstance_id )
              if(!this.disabled.find(item => item.id == specificinstance.id)) {
                this.disabled.push(specificinstance)
              }
            }

        });
      }
    }
  },
  beforeMount() {
    var pall = [];
    var self = this;
    pall.push(this.$store.dispatch("specificmaterials/fetchList"));
    pall.push(this.$store.dispatch("genericmaterials/fetchList"));
    pall.push(this.$store.dispatch("entities/fetchList"));
    pall.push(this.$store.dispatch("loans/fetchStatus"));
    this.pending_loan.models.forEach(item => {
      pall.push(this.initInstances(item));
    });
    Promise.all(pall).then(() => {
      if (!self.canManage) {
        self.status = {};
        var keys = [1, 2];
        var values = ["Annulé", "Demandé"];

        if(this.pending_loan.status == 2 && !this.pending_loan.id) {
          self.status[2] = "Demandé"
        }
        if ((this.pending_loan.status == 2 || this.pending_loan.status == 1) && this.pending_loan.id){
          for (var i = 0; i < keys.length; i++) {
            self.status[keys[i]] = values[i];
          }
        }
        else if (this.pending_loan.status == 3) {
          self.status[3] = "Accepté";
        }
        else if (this.pending_loan.status == 4 ) {
          self.status[4] = "Refusé";
        }
      }
      //début chargement
      this.loaded = true;

      if(this.checkDates) {
   
        for(let i=0; i<=this.pending_loan.generic_materials.length-1; i++) {
          let materialgeneric = this.pending_loan.generic_materials[i];
          this.setMaterialAvailability(materialgeneric);
        }

        for(let i=0; i<=this.pending_loan.specific_materials.length -1; i++) {
          let specificinstance_id = this.pending_loan.specific_materials[i];
          let instances = Object.keys(this.specificinstances).filter(instances => {
              return Object.values(this.specificinstances[instances]).find(object => object.id == specificinstance_id)
          });
          let model = instances[0]
          let item = {"specificinstance":specificinstance_id,"model":model};
          this.setMaterialAvailability(item);
        }
      }


    });

    if (this.pending_loan.id && this.pending_loan.status == 3) {
      this.$store
        .dispatch("loans/fetchSingle", { id: this.pending_loan.id })
        .then(data => {
          if (data.status !== 3) {
            this.makeChild_btn = false;
          } else {
            this.makeChild_btn = true;
          }
        });
    }
  }
};
</script>
