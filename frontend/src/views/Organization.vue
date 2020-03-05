<template>
<div class="grid-2">
    <choice :items="entities" :title="listEntities"></choice>
  <div v-if="entity" class="align-form">
    <form  @submit="saveObject(entity)">
      <div class="form-group">
        <label>Nom </label>
        <input
          type="text"
          class="form-control"
          v-model="entity.name"
          placeholder="entity.name"
        />
        <label>Email </label
        ><input
          type="email"
          class="form-control"
          v-model="entity.contact"
          placeholder="entity.contact"
        />
        <label>Description </label
        ><textarea
          class="form-control"
          v-model="entity.description"
          placeholder="entity.description"
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary" @click.prevent="saveObject(entity)" >Submit</button>
    </form>
  </div>
</div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { mapGetters, mapState } from "vuex";
import choice from "@/components/choice"

export default {
  name: "Organization",

  data() {
    return {
      sorting: "1",
      listEntities: "Liste entités"
    };
  },

  props: {
    organization: {
      type: Number,
      default() {
        return "";
      }
    }
  },

  components: {
    choice
    // eslint-disable-next-line no-unused-expressions
  },

  methods: {
    saveObject(entity) {
      console.log('update entity')
      this.$store.dispatch("updateEntity",entity)
    }
  },
  created() {
    this.$store.dispatch("getOrganizations");
  },

  computed: {
    items() {
      return [
        this.entity.name,
        "Utilisateurs",
        "Prêts en cours",
        "Historique de prêts",
        "Matériels"
      ];
    },

    entities() {

      let entities = []
      for(let i=0; i<=this.organizations.length -1 ; i++) {
        entities[i] = { link: `/manage/entity/${this.organizations[i].id}`, name: this.organizations[i].name }
      }
      return entities
      
    },

    entity() {
      return (
        this.organizations.find(
          organization => organization.id == this.organization
        ) || {}
      );
    },

  
    ...mapState({
      equipment: state => state.equipment,
      organizations: state => state.organizations
      //orgatypes: state => state.organizationTypes
    }),
    sortKey: {
      get: function() {
        //this.$store.dispatch('getOrganizationTypes', this.sorting.split(' ')[0])
        return this.sorting.split(" ")[0]; // return the key part
      }
    },
    sortOrder: {
      get: function() {
        return this.sorting.split(" ")[1]; // return the order part
      }
    }
  },
  render(h) {
    return this.$route == "manage" ? h("organization") : h("home");
  }
};
</script>
