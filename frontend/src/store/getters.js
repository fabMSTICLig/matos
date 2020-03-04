let getters = {
    equipments: state => {
        return state.equipments
    },
    isAdmin: state => {
        return true;
    },
    userAuth: state => {
        return state.authUser;

    }

 }

export default getters