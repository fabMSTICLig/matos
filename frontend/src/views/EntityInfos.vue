<template>
  <div class="row">
    <div class="col-12">
      <div class="card" v-if="object">
        <div class="card-header">
          <h3 class="float-left">
            {{ object | field("name") }}
          </h3>
          <router-link
            class="btn btn-primary float-right"
            role="button"
            :to="{
              name: 'entityedit',
              params: { entityid: object.id }
            }"
            v-if="isManager"
            >Modifier</router-link
          >
        </div>
        <div class="card-body">
          <fieldset>
            <legend>Informations</legend>
            <p class="card-text">
              <span
                ><strong>{{ object.description }}</strong></span
              >
            </p>
            <p class="card-text">
              <span><strong>Contact :&nbsp;</strong></span
              ><a :href="'mailto:' + object.contact">{{ object.contact }}</a>
            </p>
            <h4>Affiliations :&nbsp;</h4>
            <DisplayIdList
              fieldName="affiliations"
              :object="object"
              ressource="affiliations"
            />
          </fieldset>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import DisplayIdList from "@/components/DisplayIdList";

export default {
  name: "Entity",
  data() {
    return {
      object: null,
      ressource: "entities"
    };
  },
  components: {
    DisplayIdList
  },
  computed: {
    ...mapGetters(["authUser"]),
    isManager() {
      return (
        (this.object && this.authUser.entities.indexOf(this.object.id) > -1) ||
        this.authUser.is_staff
      );
    }
  },
  methods: {},
  beforeMount() {
    if (
      this.$route.params[this.$route.meta.routeparam] != "new" &&
      parseInt(this.$route.params[this.$route.meta.routeparam], -1) != -1
    ) {
      this.$store
        .dispatch(this.ressource + "/fetchSingle", {
          id: this.$route.params[this.$route.meta.routeparam]
        })
        .then(data => {
          this.object = Object.assign({}, data);
        });
    }
  }
};
</script>
