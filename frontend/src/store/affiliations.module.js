import ApiService from '@/common/api.service'
import { DataHelper } from '../common/helpers'

import {
  UPDATE_AFFILIATION,
  CREATE_AFFILIATION,
  DELETE_AFFILIATION,
  FETCH_AFFILIATIONS
} from './actions.type'

import { SET_AFFILIATION, SET_AFFILIATIONS } from './mutations.type'

export const state = {
  affiliations: []
}
const getters = {

  affiliations (state) {
    return state.affiliations
  }
}

export const actions = {
  [FETCH_AFFILIATIONS] (context, force = false) {
    // eslint-disable-next-line eqeqeq
    if (context.state.affiliations.length == 0 || force) {
      return ApiService.query('affiliations', {})
        .then(({ data }) => {
          context.commit(SET_AFFILIATIONS, data)
          return data
        })
        .catch(error => {
          throw new Error(error)
        })
    } else {
      return Promise.resolve(context.state.affiliations)
    }
  },
  [UPDATE_AFFILIATION] (context, { id, data }) {
    return ApiService.update('affiliations', id, data).then(({ data }) => {
      context.commit(SET_AFFILIATION, data)
      return data
    })
  },
  [CREATE_AFFILIATION] (context, { data }) {
    return ApiService.post('affiliations', data).then(({ data }) => {
      context.commit(SET_AFFILIATION, data)
      return data
    })
  },
  [DELETE_AFFILIATION] (context) {
    context.commit(SET_AFFILIATION, {
      name: '',
      type: ''
    })
  }
}

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {

  [SET_AFFILIATION] (state, orga) {
    if ('id' in orga) {
      DataHelper.updateById(state.orgas, orga)
    }
  },
  [SET_AFFILIATIONS] (state, affiliations) {
    state.affiliations = affiliations
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
