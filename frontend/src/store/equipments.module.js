import ApiService from '@/common/api.service'
import { DataHelper } from '../common/helpers'

import {
  FETCH_EQUIPMENTS,
  GET_EQUIPMENT,
  CREATE_EQUIPMENT,
  UPDATE_EQUIPMENT
} from './actions.type'

import { SET_EQUIPMENTS, SET_EQUIPMENT } from './mutations.type'

export const state = {
  equipments: []
}
const getters = {
  equipments (state) {
    return state.equipments
  }
}

export const actions = {
  [FETCH_EQUIPMENTS] (context, force = false) {
    // eslint-disable-next-line eqeqeq
    if (context.state.equipments.length == 0 || force) {
      return ApiService.get('api/equipments')
        .then(({ data }) => {
          console.log('equipements')
          console.log(data)
          context.commit(SET_EQUIPMENTS, data)
          return data.data
        })
    } else {
      return Promise.resolve(context.state.orgas)
    }
  },
  [GET_EQUIPMENT] (context, index) {
    return ApiService.get('/equipment/', index).then(({ data }) => {
      context.commit(SET_EQUIPMENT, data)
      return data
    })
  },
  [UPDATE_EQUIPMENT] (context, { id, data }) {
    return ApiService.update('/equipment/', id, data).then(({ data }) => {
      context.commit(SET_EQUIPMENT, data)
      return data
    })
  },
  [CREATE_EQUIPMENT] (context, { data }) {
    return ApiService.post('/equipments', data).then(({ data }) => {
      context.commit(SET_EQUIPMENT, data)
      return data
    })
  }

}

/* eslint no-param-reassign: ['error', { 'props': false }] */
export const mutations = {
  [SET_EQUIPMENTS] (state, equipments) {
    state.orgas = equipments
  },
  [SET_EQUIPMENT] (state, equipment) {
    if ('id' in equipment) {
      DataHelper.updateById(state.equipments, equipment)
    }
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
