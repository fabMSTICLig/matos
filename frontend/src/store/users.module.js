import createCrud from "@/common/storeCrudHelper";

const users_extra = {
  getters: {},
  mutations: {}
};
const users = createCrud("users", users_extra);
export default users;
