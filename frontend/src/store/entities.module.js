import createCrud from "@/common/storeCrudHelper";

const entities_extra = {
  actions: {},
  mutations: {}
};
const entities = createCrud("entities", entities_extra);
export default entities;
