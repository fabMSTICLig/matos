<template>
    <div>
        <b-card
        :title="organization.name"
        tag="article"
        style="max-width: 20rem;"
        class="mb-2"
        v-show="organization"
        >
        <b-badge  variant="info" >Affiliations</b-badge>
        <b-list-group flush>
            <b-list-group-item v-for="item in organization.affiliations" :key="item.id">{{item.name}}</b-list-group-item>
        </b-list-group>
        <b-card-text>
            {{organization.description}}
        </b-card-text>

        <b-button href="#" @click="selectOrganization" variant="outline-primary">Select</b-button>
    </b-card>
    </div>
</template>

<script>
import { EditorMixin } from '@/common/mixins.js'
import { GET_ORGA, FETCH_ORGAS } from '@/store/actions.type'
export default {
  name: 'organization',
  mixins: [EditorMixin],
  data () {
    return {
      actions: {
        GET: GET_ORGA,
        FETCH: FETCH_ORGAS
      }
    }
  },
  props: {
    organization: {
      type: Object,
      default: null
    }
  },
  watchers: {
    organization (value) {
      console.log('update value')
      console.log(value)
    }
  },
  methods: {
    selectOrganization () {
      this.selectObject(this.organization)
    }
  }
}
</script>
<style scoped>
.container-md-8 {
  margin-top: 50px;
}
</style>
