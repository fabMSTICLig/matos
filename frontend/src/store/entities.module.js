import ApiService from '@/common/api.service'
import { DataHelper } from '../common/helpers'
import Vue from 'vue'
import {
  FETCH_ENTITIES,
  UPDATE_ENTITY,
  GET_ENTITY,
  CREATE_ENTITY,
  RESET_ENTITY,
  DELETE_ENTITY
} from './actions.type'

import { SET_ENTITIES, SET_ENTITY, GET_ENTITY_STATE } from './mutations.type'

Vue.config.devtools = true

export const state = {
  entities: [],
  entity: ''
}
const getters = {
  entities (state) {
    return state.entities
  },

  entity (state) {
    return state.entity
  }
}

export const actions = {
  [FETCH_ENTITIES] (context, force = false) {
    // eslint-disable-next-line eqeqeq
    if (context.state.entities.length == 0 || force) {
      return ApiService.query('entities', {})
        .then(({ data }) => {
          context.commit(SET_ENTITIES, data)
          return data
        })
        .catch(error => {
          throw new Error(error)
        })
    } else {
      return Promise.resolve(context.state.entities)
    }
  },
  [GET_ENTITY] (context, id) {
    console.log(id)
    return ApiService.get('/entities', id).then(({ data }) => {
      context.commit(GET_ENTITY_STATE, data)
      return data
    })
  },
  [UPDATE_ENTITY] (context, { id, data }) {
    console.log('update orga')
    return ApiService.update('entities', id, data).then(({ data }) => {
      context.commit(SET_ENTITY, data)
      console.log(data)
      return data
    })
  },
  [DELETE_ENTITY] (context, { id }) {
    console.log('update orga')
    return ApiService.delete('entities', id).then(({ data }) => {
      context.commit(DELETE_ENTITY, data)
      console.log(data)
      return data
    })
  },

  [CREATE_ENTITY] (context, { data }) {
    return ApiService.post('entities/', data).then(({ data }) => {
      context.commit(SET_ENTITY, data)
      console.log(data)
      return data
    })
  },
  [RESET_ENTITY] (context) {
    context.commit(SET_ENTITY, {
      name: '',
      contact: '',
      orga_type: ''
    })
  }

}

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_ENTITIES] (state, entities) {
    state.entities = entities
  },
  [SET_ENTITY] (state, entity) {
    state.entity = entity
    if ('id' in entity) {
      DataHelper.updateById(state.entities, entity)
    }
  },
  [GET_ENTITY_STATE] (state, entity) {
    state.entity = entity
  },
  [DELETE_ENTITY] (state, entity) {
    console.log(entity)
    if ('id' in entity) {
      DataHelper.removeById(state.entities, entity)
    }
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
