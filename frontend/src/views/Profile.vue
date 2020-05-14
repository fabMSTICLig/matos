<template>
  <div class="card">
    <div class="card-header">
      <h3>Votre profile</h3>
    </div>
    <div class="card-body">
      <form>
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
          />
        </div>
        <div class="form-group">
          <label>Nom</label
          ><input
            class="form-control"
            type="text"
            v-model="authUser.last_name"
          />
        </div>
        <div class="form-group">
          <label>Email</label
          ><input class="form-control" type="email" v-model="authUser.email" />
        </div>
        <div class="form-group">
          <label>Affiliations</label>
          <DynList
            ressource="affiliations"
            v-model="authUser.affiliations"
          ></DynList>
        </div>
        <div class="btn-group" role="group">
          <button class="btn btn-primary" type="button" v-on:click="update">
            Modifier
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import DynList from "@/components/DynList";
import { UPDATE_AUTHUSER } from "@/store/actions.type";
import { mapGetters } from "vuex";
export default {
  name: "Profile",
  components: {
    DynList
  },
  data() {
    return {};
  },
  computed: {
    ...mapGetters(["authUser"])
  },
  methods: {
    update() {
      this.$store.dispatch(UPDATE_AUTHUSER, this.authUser).then(() => {
        console.log("Profile updated");
        this.$bvModal.msgBoxOk("Profile updated");
        this.$store.dispatch("affiliations/fetchList");
      });
    }
  }
};
</script>
