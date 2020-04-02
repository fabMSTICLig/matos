import ApiService from '@/common/api.service'
import { DataHelper } from '../common/helpers'

import {
  GET_FAMILY,
  FETCH_FAMILIES,
  UPDATE_FAMILY,
  CREATE_FAMILY
} from './actions.type'

import { SET_FAMILIES, SET_FAMILY } from './mutations.type'

export const state = {
  families: []
}
const getters = {
  families (state) {
    return state.families
  }
}

export const actions = {
  [FETCH_FAMILIES] (context, force = false) {
    // eslint-disable-next-line eqeqeq
    if (context.state.families.length == 0 || force) {
      return ApiService.get('api/families')
        .then(({ data }) => {
          context.commit(SET_FAMILIES, data)
          return data
        })
    } else {
      return Promise.resolve(context.state.families)
    }
  },
  [GET_FAMILY] (context, index) {
    return ApiService.get('api/families', index).then(({ data }) => {
      context.commit(SET_FAMILY, data)
      return data
    })
  },
  [UPDATE_FAMILY] (context, { id, data }) {
    return ApiService.update('api/equipment/', id, data).then(({ data }) => {
      context.commit(SET_FAMILY, data)
      return data
    })
  },
  [CREATE_FAMILY] (context, { data }) {
    return ApiService.post('api/equipments', data).then(({ data }) => {
      context.commit(SET_FAMILY, data)
      return data
    })
  }

}

/* eslint no-param-reassign: ['error', { 'props': false }] */
export const mutations = {
  [SET_FAMILIES] (state, families) {
    state.families = families
  },
  [SET_FAMILY] (state, family) {
    if ('id' in family) {
      DataHelper.updateById(state.families, family)
    }
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
