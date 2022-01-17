import createCrud from "./crud.factory";
import ApiService from "../common/api.service";

const tags_extra = {
  actions: {
    async destroyUnused({ commit }) {
      const { data } = await ApiService.delete("tags/delete_unused");
      commit(
        "destroyUnusedSuccess",
        data.map((item) => item.toString())
      );
      return data;
    },
  },
  mutations: {
    destroyUnusedSuccess(state, tag_ids) {
      var i = state.list.length;
      while (i--) {
        if (tag_ids.includes(state.list[i])) {
          delete state.entities[state.list[i].toString()];
          state.list.splice(i, 1);
        }
      }
    },
  },
};
const tags = createCrud("tags", tags_extra);
export default tags;
