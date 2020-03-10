import ApiService from "@/common/api.service"
import DataHelper from "@/common/helpers"

import {
  FETCH_ORGAS,
  UPDATE_ORGA,
  GET_ORGA,
  CREATE_ORGA,
  RESET_ORGA
} from './actions.type'

import { SET_ORGAS, SET_ORGA } from './mutations.type'

export const state = {
  orgas: [],
}
const getters = {
  orgas (state) {
    return state.orgas
  }
}

export const actions = {
  [FETCH_ORGAS] (context, force = false) {
    if (context.state.orgas.length == 0 || force) {
      return ApiService.query('gestion/organizations', {})
        .then(({ data }) => {
          context.commit(SET_ORGAS, data)
          return data
        })
        .catch(error => {
          throw new Error(error)
        })
    } else {
      return Promise.resolve(context.state.orgas)
    }
  },
  [GET_ORGA] (context, id) {
    return ApiService.get('organizations', id).then(({ data }) => {
      context.commit(SET_ORGA, data)
      return data
    })
  },
  [UPDATE_ORGA] (context, { id, data }) {
    return ApiService.update('organizations', id, data).then(({ data }) => {
      context.commit(SET_ORGA, data)
      return data
    })
  },
  [CREATE_ORGA] (context, { data }) {
    return ApiService.post('organizations', data).then(({ data }) => {
      context.commit(SET_ORGA, data)
      return data
    })
  },
  [RESET_ORGA] (context) {
    context.commit(SET_ORGA, {
      name: '',
      contact: '',
      orga_type: ''
    })
  }
}

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_ORGAS] (state, orgas) {
    state.orgas = orgas
  },
  [SET_ORGA] (state, orga) {
    if ('id' in orga) {
      DataHelper.updateById(state.orgas, orga)
    }
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
