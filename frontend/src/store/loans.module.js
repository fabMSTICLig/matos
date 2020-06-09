import createCrud from "@/common/storeCrudHelper";
import ApiService from "@/common/api.service";

const loans_extra = {
  state: {
    pending_loan: null,
    status : {}
  },
  getters: {
    pending_loan(state) {
      return state.pending_loan;
    },
    status(state){
        return state.status;
    }
  },
  actions: {
      fetchStatus({ commit }) {
      return ApiService.query("loans/status", {}).then(({ data }) => {
        commit("setStatus", data);
        return data;
      });
    }
  },
  mutations: {
    setStatus(state, status) {
      state.status = status;
    },
    onLoad(state){
      if(localStorage.getItem("pending_loan")!=null)
      {
          var loan = JSON.parse(localStorage.getItem("pending_loan"))
          state.pending_loan = loan
      }
      else
      {
          state.pending_loan={
              entity:null,
              status:1,
              user:null,
              due_date:null,
              return_date:null,
              checkout_date:null,
              comments:null,
              specificmaterials:[],
              models:[],
              genericmaterials:[],
          }
          localStorage.setItem('pending_loan', JSON.stringify(state.pending_loan));
      }
    },
    resetPending(state) {
      state.pending_loan={
          entity:null,
          status:1,
          user:null,
          due_date:null,
          return_date:null,
          checkout_date:null,
          comments:null,
          specificmaterials:[],
          models:[],
          genericmaterials:[],
      }
      localStorage.setItem('pending_loan', JSON.stringify(state.pending_loan));
    },
    addMaterial(state,item){
        if(state.pending_loan.entity == null)
        {
            state.pending_loan.entity=item.entity
        }
        if("quantity" in item && state.pending_loan.genericmaterials.indexOf(item.id) == -1 ){
            state.pending_loan.genericmaterials.push({ 'material' : item.id, 'quantity' : 1})
        }
        else if(state.pending_loan.models.indexOf(item.id) == -1) {
            state.pending_loan.models.push(item)
        }
        localStorage.setItem('pending_loan', JSON.stringify(state.pending_loan));
    },
    cleanMaterials(state){
        state.pending_loan.entity = null;
        state.pending_loan.genericmaterials=[]
        state.pending_loan.specificmaterials=[]
        state.pending_loan.models=[]
        localStorage.setItem('pending_loan', JSON.stringify(state.pending_loan));
    }
  }
};
const loans = createCrud("loans", loans_extra);
export default loans;
