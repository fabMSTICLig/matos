<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <h3>Ajout massif matériel générique</h3>
        </div>
        <div class="card-body">
          <form id="editor-form">
            <div class="form-group">
              Format :
              <ul>
                <li>
                  Ordre des champs :
                  <ul>
                    <li>Nom</li>
                    <li>Quantité</li>
                    <li>Référence interne</li>
                    <li>Référence fabriquant</li>
                    <li>Description</li>
                    <li>Localisation</li>
                    <li>Tags</li>
                  </ul>
                </li>
                <li>Encodage : utf8</li>
                <li>Séparateur : tabulation</li>
                <li>Séparateur tags: ',' virgule</li>
              </ul>
            </div>
            <div class="form-group">
              Télécharger fichier exemple :
              <a href="static/example.csv">example.csv</a>
            </div>
            <div class="custom-file">
              <input
                type="file"
                @change="changeFile"
                accept=".csv"
                class="custom-file-input"
                id="customFile"
              />
              <label class="custom-file-label" for="customFile"
                >Choisissez un fichier</label
              >
            </div>
            <div>
              <span>Fichier : </span
              ><span class="mr-2" v-if="file" v-text="file.name"></span>
              <button
                v-if="file"
                class="btn btn-danger"
                type="button"
                @click="file = null"
              >
                X
              </button>
            </div>
            <div class="form-group">
              <label for="textinput">Entrée texte</label>
              <textarea
                v-model="textinput"
                class="form-control"
                id="textarea"
                rows="10"
                :disabled="file"
              ></textarea>
            </div>
            <button class="btn btn-primary" type="button" @click="send">
              Ajouter
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from "@/common/api.service";
import { showMsgOk } from "@/components/Modal";
/*
  Vue Edition Matériel Générique pour une Entité
*/

export default {
  name: "GenericMaterialBulk",
  data() {
    return {
      file: null,
      textinput:
        "name	quantity	ref_int	ref_fab	desc	loc	tags\narduino uno	10	fabardui	A000073	https://www.arduino.cc/	S03/A1/E3	arduino, elec"
    };
  },

  computed: {
    prefix() {
      return "entities/" + this.$route.params.entityid + "/";
    }
  },
  methods: {
    changeFile(f) {
      console.log(f);
      this.file = f.target.files[0];
    },
    send() {
      let data = null;
      let params = {};
      if (this.file) {
        data = new FormData();
        data.append("file", this.file);
        params = {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        };
      } else if (this.textinput) {
        data = new FormData();
        data.append("text", this.textinput);
      }
      console.log(this.textinput);
      console.log(data);
      if (data) {
        ApiService.post(
          "entities/" +
            this.$route.params.entityid +
            "/genericmaterials/bulk_add",
          data,
          params
        )
          .then(() => {
            this.$router.push({
              name: "materialslist",
              params: this.$route.params
            });
          })
          .catch(e => {
            if (e.response) {
              console.log(e.response.data.detail);
              showMsgOk(e.response.data.detail);
            } else console.log(e);
          });
      }
    }
  }
};
</script>
