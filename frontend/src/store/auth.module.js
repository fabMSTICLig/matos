import ApiService from '@/common/api.service'

import {
  CHECK_AUTH,
  UPDATE_AUTHUSER,
  UPDATE_PASSWORD
} from './actions.type'
import { SET_AUTHUSER, PURGE_AUTH, SET_ERROR, SET_AUTHUSER_MANAGER } from './mutations.type'

const state = {
  errors: null,
  authUser: {}
}

const getters = {
  authUser (state) {
    return state.authUser
  },
  isAuthenticated (state) {
    if (state.authUser) {
      return !!state.authUser.username
    } else {
      return false
    }
  },
  isAdmin (state) {
    if (state.authUser) {
      return state.authUser.is_staff || false
    } else {
      return false
    }
  },
  isManager (state) {
    if (state.authUser) {
      return state.authUser.is_manager || false
    } else {
      return false
    }
  }
}

const actions = {
  [CHECK_AUTH] (context) {
    return new Promise((resolve, reject) => {
      ApiService.query('self', { withCredentials: true })
        .then(({ data }) => {
          context.commit(SET_AUTHUSER, data.user)
          context.commit(SET_AUTHUSER_MANAGER, data.manager)
          resolve()
        })
        .catch((e) => {
          context.commit(PURGE_AUTH)
          // eslint-disable-next-line prefer-promise-reject-errors
          reject()
        })
    })
  },
  [UPDATE_AUTHUSER] (context, user) {
    return ApiService.update('users', user.id, user).then(({ data }) => {
      context.commit(SET_AUTHUSER, data)
      return data
    })
  },
  [UPDATE_PASSWORD] (context, passwords) {
    return ApiService.put(`users/${state.authUser.id}/set_password/`, passwords).then(({ data }) => {
      return 'Password changed'
    })
  }

}

const mutations = {
  [SET_ERROR] (state, error) {
    state.errors = error
  },
  [SET_AUTHUSER] (state, user) {
    state.authUser = user
    state.errors = {}
  },
  [PURGE_AUTH] (state) {
    state.authUser = {}
    state.errors = {}
  },
  [SET_AUTHUSER_MANAGER] (state, manager) {
    state.authUser.is_manager = manager
    state.errors = {}
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
