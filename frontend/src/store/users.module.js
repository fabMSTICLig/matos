import ApiService from '@/common/api.service'
import { DataHelper } from '../common/helpers'

import {
  FETCH_USERS,
  UPDATE_USER,
  GET_USER,
  CREATE_USER
} from './actions.type'

import { SET_USERS, SET_USER } from './mutations.type'

export const state = {
  users: []
}
const getters = {
  users (state) {
    return state.users
  }
}

export const actions = {
  [FETCH_USERS] (context, force = false) {
    // eslint-disable-next-line eqeqeq
    if (context.state.users.length == 0 || force) {
      return ApiService.get('/users')
        .then(({ data }) => {
          context.commit(SET_USERS, data)
          return data
        })
    } else {
      return Promise.resolve(context.state.families)
    }
  },
  [GET_USER] (context, index) {
    return ApiService.get('/users', index).then(({ data }) => {
      context.commit(SET_USER, data)
      return data
    })
  },
  [UPDATE_USER] (context, { id, data }) {
    return ApiService.update('/users', id, data).then(({ data }) => {
      context.commit(SET_USER, data)
      return data
    })
  },
  [CREATE_USER] (context, { data }) {
    return ApiService.post('/users', data).then(({ data }) => {
      context.commit(SET_USER, data)
      return data
    })
  }

}

/* eslint no-param-reassign: ["error", { "props": false }] */
export const mutations = {
  [SET_USERS] (state, users) {
    state.users = users
  },
  [SET_USER] (state, user) {
    if ('id' in user) {
      DataHelper.updateById(state.users, user)
    }
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
