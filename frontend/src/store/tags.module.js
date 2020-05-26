import createCrud from "@/common/storeCrudHelper";
import ApiService from "@/common/api.service";
import Vue from "vue";

const tags_extra = {
  actions: {
    destroyUnused({ commit }) {
      return ApiService.delete("tags/delete_unused").then(({ data }) => {
        commit(
          "destroyUnusedSuccess",
          data.map(item => item.toString())
        );
        return data;
      });
    }
  },
  mutations: {
    destroyUnusedSuccess(state, tag_ids) {
      var i = state.list.length;
      while (i--) {
        if (tag_ids.includes(state.list[i])) {
          Vue.delete(state.entities, state.list[i].toString());
          state.list.splice(i, 1);
        }
      }
    }
  }
};
const tags = createCrud("tags", tags_extra);
export default tags;
