let getters = {
    equipments: state => {
        return state.equipments
    },
    isManager: state => {
        return state.authUser.manager;
    },
   
    userAuth: state => {
        return state.authUser;

    }

 }

export default getters