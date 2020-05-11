import createCrud from "@/common/storeCrudHelper"

import ApiService from "@/common/api.service";

const users_extra = {
    actions:{
        fetchTypes({commit}) {

            return ApiService.query("users/types", {})
                .then(({
                    data
                }) => {
                    commit('setTypes', data);
                    return data;
                });
        },
    },
    mutations:{
        setTypes(state, user_types) {
            state.types = user_types;
        },
    }
};
const users = createCrud('users',users_extra);
export default users;
