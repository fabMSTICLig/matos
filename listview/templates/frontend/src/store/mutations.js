let mutations = {
  CREATE_EQUIPMENT(state, equipment) {
    state.equipments.unshift(equipment);
  },
  FETCH_EQUIPMENTS(state, equipments) {
    return (state.equipments = equipments);
  },
  GET_EQUIPMENT(state, equipment) {
    let index = state.equipments.findIndex(item => item.id == equipment.id);

    state.equipments[index] == equipment;
    return (state.equipments[index] = equipment);
  },
  DELETE_EQUIPMENT(state, equipment) {
    let index = state.equipments.findIndex(item => item.id == equipment.id);

    state.equipments.splice(index, 1);
  },
  UPDATE_EQUIPMENT(state, equipment) {
    let index = state.equipments.findIndex(item => item.id == equipment.id);

    state[index] == equipment;
  },
  GET_CATEGORY(state, category) {
    return (state.category = category);
  },
  GET_CATEGORIES(state, categories) {
    return (state.categories = categories);
  },

  GET_ORGANIZATIONS(state, organizations) {
    return (state.organizations = organizations);
  },

  GET_ORGANIZATION_TYPES(state, organizationTypes) {
    return (state.organizationTypes = organizationTypes);
  }
};

export default mutations;
