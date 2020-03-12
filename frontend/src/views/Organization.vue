<template>
<div class="grid-2">
  <choice :items="entities" :title="listEntities"></choice>
  <div v-show="!isEmpty" class="align-form">
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
import { FETCH_ORGAS, UPDATE_ORGA } from "@/store/actions.type"

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
        return 0;
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
      this.$store.dispatch(UPDATE_ORGA, { id: entity.id, data: entity }).then((entity) => {
            console.log('organisation mise a jour')
          });
    }
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

    isEmpty() {
      console.log(Object.keys(this.entity).length === 0)
      return Object.keys(this.entity).length === 0
    },

    entities() {
      let entities = []
      for(let i=0; i<=this.orgas.length -1 ; i++) {
        entities[i] = { link: `/manage/entity/${this.orgas[i].id}`, name: this.orgas[i].name }
      }
      return entities      
    },

    entity() {
      console.log(this.organization)
      return this.orgas.find( orga => orga.id == this.$route.params.id) || {}
      
    },

    ...mapGetters(['orgas']),

    ...mapState({
      equipment: state => state.equipment,
      organizations: state => state.orgas
    }),
    sortKey: {
      get: function() {
        return this.sorting.split(" ")[0]; // return the key part
      }
    },
    sortOrder: {
      get: function() {
        return this.sorting.split(" ")[1]; // return the order part
      }
    }
  },

  beforeMount () {
    this.$store.dispatch(FETCH_ORGAS)
  },

  render(h) {
    return this.$route == "manage" ? h("organization") : h("home");
  }
};
</script>
