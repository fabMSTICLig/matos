import createCrud from "@/common/storeCrudHelper";

const users_extra = {
  actions: {},
  mutations: {}
};
const users = createCrud("users", users_extra);
export default users;
