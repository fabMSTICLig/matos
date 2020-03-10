import { SET_AUTHUSER } from "./mutations.type";

/* eslint-disable eqeqeq */
let mutations = {
  CREATE_EQUIPMENT (state, equipment) {
    state.equipments.unshift(equipment)
  },
  FETCH_EQUIPMENTS (state, equipments) {
    return (state.equipments = equipments)
  },
  GET_EQUIPMENT (state, equipment) {
    let index = state.equipments.findIndex(item => item.id == equipment.id);

    // eslint-disable-next-line no-unused-expressions
    state.equipments[index] == equipment
    return (state.equipments[index] = equipment)
  },
  DELETE_EQUIPMENT (state, equipment) {
    let index = state.equipments.findIndex(item => item.id == equipment.id);

    state.equipments.splice(index, 1)
  },
  UPDATE_EQUIPMENT (state, equipment) {
    //let index = state.equipments.findIndex(item => item.id == equipment.id);
    console.log("equipment update")
  },
  GET_CATEGORY (state, category) {
    return (state.category = category)
  },
  GET_CATEGORIES (state, categories) {
    return (state.categories = categories)
  },

  GET_ORGANIZATIONS (state, organizations) {
    return (state.organizations = organizations)
  },

  GET_ORGANIZATION_TYPES (state, organizationTypes) {
    return (state.organizationTypes = organizationTypes)
  },
  GET_USERS (state, users) {
    return (state.users = users)
  },
  AUTH_USER (state, user) {
    return (state.authUser = user)
  },
  SET_ORGA (state,user) {
    console.log("orga update")
  },
  SET_AUTHUSER (state,user) {
    return (state.authUser = user)
  }
}

export default mutations
