<template>
    <div>
        <b-card
        :title="entity.name"
        tag="article"
        style="max-width: 20rem;"
        class="mb-2"
        v-show="entity"
        >
        <b-badge  variant="info" >Affiliations</b-badge>
        <b-list-group flush>
            <b-list-group-item v-for="item in entity.affiliations" :key="item.id">{{item.name}}</b-list-group-item>
        </b-list-group>
        <b-card-text>
            {{entity.description}}
        </b-card-text>

        <b-button href="#" @click="selectEntity" variant="outline-primary">Select</b-button>
    </b-card>
    </div>
</template>

<script>
import { EditorMixin } from '@/common/mixins.js'
import { GET_ENTITY, FETCH_ENTITIES } from '@/store/actions.type'
export default {
  name: 'entity',
  mixins: [EditorMixin],
  data () {
    return {
      actions: {
        GET: GET_ENTITY,
        FETCH: FETCH_ENTITIES
      }
    }
  },
  props: {
    entity: {
      type: Object,
      default: null
    }
  },
  watchers: {
    entity (value) {
      console.log('update value')
      console.log(value)
    }
  },
  methods: {
    selectEntity () {
      this.selectObject(this.entity)
    }
  }
}
</script>
<style scoped>
.container-md-8 {
  margin-top: 50px;
}
</style>
