import createCrud from "@/common/storeCrudHelper";

const users_extra = {
  getters: {
    users(state) {
      return state.users;
    }
  },
  mutations: {}
};
const users = createCrud("users", users_extra);
export default users;
