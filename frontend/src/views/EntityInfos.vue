<template>
  <div class="row" v-if="!isManager">
    <entity-edit v-if="isManager"></entity-edit>
    <div class="col-12">
      <div class="card" v-if="object">
        <div class="card-header">
          <h3 class="float-left">{{ entityById($route.params.entityid) | field("name") }}</h3>
        </div>
        <div class="card-body">
          <fieldset>
            <legend>Informations</legend>
            <p class="card-text">
              <span><strong>{{object.description}}</strong></span>
            </p>
            <p class="card-text">
              <span><strong>Contact :&nbsp;</strong></span
              ><a :href="'mailto:' + object.contact">{{
                object.contact
              }}</a>
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
import { EditMixin } from "@/common/mixins";
import DisplayIdList from "@/components/DisplayIdList";
import EntityEdit from "@/views/EntityEdit";

export default {
  name: "Entity",
  mixins: [EditMixin],
  data() {
    return {
      ressource: "entities",
      object_name: "Entité"
    }
  },
  components:{
    DisplayIdList,
    EntityEdit

  },
  computed: {
     ...mapGetters(["authUser"]),
   
    ...mapGetters({
      entityById: "entities/byId",
    }),
    isManager() {
      return (
        (this.selected_object &&
          this.authUser.entities.indexOf(this.selected_object.id) > -1) ||
        this.authUser.is_staff
      );
    }

  },
  methods: {}
};
</script>
