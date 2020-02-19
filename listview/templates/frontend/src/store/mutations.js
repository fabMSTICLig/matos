let mutations = {
    CREATE_EQUIPMENT(state, equipment)  {
            state.equipments.unshift(equipment)
    },
    FETCH_EQUIPMENTS(state, equipments) {
        return state.equipments = equipments
    },
    DELETE_EQUIPMENT(state, equipment) {
        let index = state.equipments.findIndex( item =>
            item.id == equipment.id)
        
        state.equipments.splice(index, 1)
    }

}

export default mutations