<template>
  <div class="card">
    <div class="card-header">
      <h3>Votre profile</h3>
    </div>
    <div class="card-body">
      <form id="editor-form" class="form">
        <p
          v-if="
            !$store.getters.authUser.first_name ||
              !$store.getters.authUser.last_name ||
              !$store.getters.authUser.email
          "
          class="text-danger"
        >
          Pour utiliser ce site vous devez renseigner vos prenom, nom et email.
        </p>
        <div class="form-group">
          <label>Username</label
          ><input
            class="form-control"
            type="text"
            v-model="authUser.username"
            readonly
          />
        </div>
        <div class="form-group">
          <label>Prénom</label
          ><input
            class="form-control"
            type="text"
            v-model="authUser.first_name"
            required
          />
        </div>
        <div class="form-group">
          <label>Nom</label
          ><input
            class="form-control"
            type="text"
            v-model="authUser.last_name"
            required
          />
        </div>
        <div class="form-group">
          <label>Email</label
          ><input
            class="form-control"
            type="email"
            v-model="authUser.email"
            required
          />
        </div>
        <template v-if="!authUser.externe">
          <div class="text-success" v-show="goodpassword">
            Le mot de passe a été modifié
          </div>
          <div class="text-danger" v-show="goodpassword == false">
            Le mot de passe est incorrect
          </div>
          <div class="text-danger" v-show="!passvalid">
            L'ancien mot de passe est nécéssaire pour changer celui-ci
          </div>
          <div class="text-danger" v-show="!passvalid">
            Le nouveau mot de passe est nécéssaire
          </div>
          <div class="text-danger" v-show="!passvalid">
            Le nouveau mot de passe et la confirmation doivent être identiques
          </div>
          <div class="form-group">
            <label>Password</label>
            <input
              v-model="form.old_password"
              type="password"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label> New password</label>
            <input
              v-model="form.new_password"
              type="password"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label>Confirm new assword</label>
            <input
              v-model="form.new_password2"
              type="password"
              class="form-control"
            />
          </div>
        </template>
        <div class="form-group">
          <label>Affiliations</label>
          <DynList
            ressource="affiliations"
            v-model="authUser.affiliations"
          ></DynList>
        </div>
        <div class="btn-group" role="group">
          <button class="btn btn-primary" type="button" @click="update">
            Modifier
          </button>
        </div>
        <div class="btn btn-primary float-right" @click="personalData">
          Consulter mes données
        </div>
      </form>
    </div>
    <modal id="modal-rgpd" title="RGPD" hideFooter v-model="showRGPD">
      <h6>Conditions d'utilisation</h6>
      <p>
        Pour permettre le bon fonctionnment du site certaines de vos
        informations sont stockées.
      </p>
      <p>
        Nom d'utilisateur, Prénom, Nom, Email sont utilisés afin de vous
        contacter. Seul les managers des entités ont accés à ces informations.
      </p>
      <p>
        Ces informations ainsi que celles liées aux prêts seront stockées 3 ans
        après que vous ayez quitté l'université ou sur demande à l'adresse
        matos@univ-grenoble-alpes.fr
      </p>

      <h6>Accepter vous ces termes ?</h6>
      <div>
        <div class="btn-group" role="group" aria-label="RGPD Accept">
          <button type="button" class="btn btn-primary" @click="accept">
            Oui
          </button>
          <button
            type="button"
            class="btn btn-danger"
            @click="showRGPD = false"
          >
            Non
          </button>
        </div>
      </div>
    </modal>
  </div>
</template>
<script>
import DynList from "@/components/DynList";
import { showMsgOk, Modal } from "@/components/Modal";
import {
  UPDATE_AUTHUSER,
  UPDATE_PASSWORD,
  UPDATE_RGPD,
  USER_DATA
} from "@/store/actions.type";
import { mapGetters } from "vuex";
import { JSONRenderer } from "@/common/helpers";
/*
  Profile de l'utilisateur
*/

/*
  @TODO: synchoniser les affiliations suite à la validation RGPD
*/
export default {
  name: "Profile",
  components: {
    DynList,
    Modal
  },
  data() {
    return {
      goodpassword: null,
      showRGPD: false,
      form: {
        old_password: "",
        new_password: "",
        new_password2: ""
      }
    };
  },
  computed: {
    ...mapGetters(["authUser", "userData"]),
    passvalid() {
      if (
        this.form.old_password == "" &&
        this.form.new_password == "" &&
        this.form.new_password2 == ""
      )
        return true;
      if (
        (this.form.old_password != "" && this.form.new_password == "") ||
        (this.form.old_password == "" && this.form.new_password != "") ||
        (this.form.new_password == "" && this.form.new_password2 == "")
      )
        return false;
      if (this.form.new_password != this.form.new_password2) return false;
      return true;
    }
  },
  methods: {
    update() {
      this.goodpassword = null;
      if (
        document.querySelector("#editor-form").checkValidity() &&
        this.passvalid != false
      ) {
        if (this.form.old_password != "") {
          this.$store
            .dispatch(UPDATE_PASSWORD, this.form)
            .then(() => {
              this.goodpassword = true;
              this.updateUser();
              this.form.old_password = "";
              this.form.new_password = "";
              this.form.new_password2 = "";
            })
            .catch(e => {
              if (e.response.status == 400) {
                this.goodpassword = false;
                showMsgOk("Mot de passe incorrect");
              }
              // eslint-disable-next-line
              console.log(e.response);
            });
        } else {
          this.updateUser();
        }
      } else {
        document.querySelector("#editor-form").reportValidity();
      }
    },
    updateUser() {
      this.$store.dispatch(UPDATE_AUTHUSER, this.authUser).then(() => {
        // eslint-disable-next-line
        console.log("Profile updated");
        showMsgOk("Profile mis à jour");
      });
    },
    accept() {
      this.$store.dispatch(UPDATE_RGPD).then(() => {
        this.showRGPD = false;
      });
    },
    personalData() {
      /*
        retourne les données personnelles d'utilisation de la plateforme
      */
      return this.$store.dispatch(USER_DATA).then(() => {
        let dateObj = new Date();
        let month = dateObj.getMonth() + 1; //months from 1-12
        let day = dateObj.getUTCDate();
        let year = dateObj.getUTCFullYear();
        let labelData =
          this.authUser.username + "_" + day + month + year + ".json";
        JSONRenderer.download(this.userData, labelData, "text/plain");
        console.log(this.userData);
      });
    }
  },
  mounted() {
    if (!this.authUser.rgpd_accept) {
      this.showRGPD = true;
    }
  }
};
</script>
