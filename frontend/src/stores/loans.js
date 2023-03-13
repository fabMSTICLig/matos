import { ref, watch } from "vue";
import { defineStore } from "pinia";
import { useAuthStore } from "@/stores/auth";
import ApiService from "@/helpers/api.service";
import useCRUDStore from "./useCRUDStore";

export const useLoansStore = defineStore("loans", () => {
  const {
    objects,
    count,
    list,
    getById,
    fetchList,
    fetchSingle,
    create,
    update,
    destroy,
  } = useCRUDStore("loans");

  const authStore = useAuthStore();

  const status = ref({});
  async function fetchStatus() {
    const { data } = await ApiService.query("loans/status");
    status.value = data;
    return data;
  }

  async function askExtension(id, date) {
    const { message } = await ApiService.post(
      "loans/" + id + "/ask_extension",
      { ext_date: date }
    );
    return message;
  }

  const basket = ref({});
  const currentLoan = ref(null);
  const loanOrigin = ref(null);

  function initBasket() {
    if (sessionStorage.getItem("basket") != null) {
      basket.value = JSON.parse(sessionStorage.getItem("basket"));
    } else {
      resetBasket();
    }
  }

  function resetBasket() {
    basket.value = {
      entity: null,
      checkout_date: new Date().toISOString().substring(0, 10),
      due_date: null,
      return_date: null,
      user: authStore.authUser.id,
      affiliation:
        authStore.authUser.affiliations.length > 0
          ? authStore.authUser.affiliations[0]
          : null,
      status: 2,
      commentary: "",
      generic_materials: [],
      specific_materials: {},
    };
  }

  watch(
    basket,
    () => {
      sessionStorage.setItem("basket", JSON.stringify(basket.value));
    },
    { deep: true }
  );

  async function setCurrent(id) {
    if (id) {
      if (currentLoan.value == null || currentLoan.value.id != id)
        currentLoan.value = JSON.parse(JSON.stringify(await fetchSingle(id)));
    } else currentLoan.value = null;
  }

  async function updateCurrent(hist = false) {
    currentLoan.value = await update(
      currentLoan.value.id,
      currentLoan.value,
      "",
      { hist }
    );
  }

  async function cancelCurrent(){
    currentLoan.value.status=1;
    await updateCurrent();
  }

  const originalLoan = ref(null);
  const historyChange = ref(false);

  watch(
    currentLoan,
    (v, p) => {
      if (v != null)
        if (p == null || (p != null && p.id != v.id)) {
          originalLoan.value = JSON.parse(JSON.stringify(v));
          historyChange.value = false;
        } else {
          let nowstring = new Date().toISOString().substring(0, 10);
          if (
            originalLoan.value.due_date > nowstring &&
            v.due_date > nowstring &&
            !originalLoan.value.child &&
            v.status == 3 &&
            !v.return_date
          )
            if (v.user != originalLoan.value.user) historyChange.value = true;
            else {
              let equal =
                v.generic_materials.length ==
                  originalLoan.value.generic_materials.length &&
                JSON.stringify(
                  v.generic_materials.sort((a, b) => a.material - b.material)
                ) ===
                  JSON.stringify(
                    originalLoan.value.generic_materials.sort(
                      (a, b) => a.material - b.material
                    )
                  );
              if (equal) {
                equal =
                  JSON.stringify(Object.keys(v.specific_materials).sort()) ===
                  JSON.stringify(
                    Object.keys(originalLoan.value.specific_materials).sort()
                  );
                if (equal) {
                  let smiv = [];
                  let smio = [];
                  Object.keys(v.specific_materials).forEach((key) => {
                    smiv = smiv.concat(v.specific_materials[key]);
                    smio = smio.concat(
                      originalLoan.value.specific_materials[key]
                    );
                  });
                  equal =
                    JSON.stringify(smiv.sort()) === JSON.stringify(smio.sort());
                }
              }
              historyChange.value = !equal;
            }
          else historyChange.value = false;
        }
      else {
        originalLoan.value = null;
        historyChange.value = false;
      }
    },
    { deep: true }
  );

  function _setLoan(loan, toBasket) {
    if (!toBasket) currentLoan.value = loan;
    else {
      basket.value = loan;
    }
  }
  function addMaterial(mat, toBasket = true) {
    let loan = Object.assign({}, !toBasket ? currentLoan.value : basket.value);
    if (loan.entity == null) {
      loan.entity = mat.entity;
    }
    if (loan.entity && loan.entity == mat.entity) {
      if ("quantity" in mat) {
        let gen_mat_items = loan.generic_materials;
        let gen_mat_included = gen_mat_items.find((item) => {
          return item.material == mat.id;
        });

        if (gen_mat_included) {
          gen_mat_included.quantity = gen_mat_included.quantity + 1;
        } else {
          loan.generic_materials.push({
            material: mat.id,
            quantity: 1,
          });
        }
      } else if (!(mat.id in loan.specific_materials)) {
        loan.specific_materials[mat.id] = [];
      }
    }
    _setLoan(loan, toBasket);
  }
  function removeMaterial(mat, toBasket = true) {
    let loan = Object.assign({}, !toBasket ? currentLoan.value : basket.value);
    if ("quantity" in mat) {
      loan.generic_materials = loan.generic_materials.filter(
        (item) => item.material != mat.id
      );
    } else if (mat.id in loan.specific_materials) {
      delete loan.specific_materials[mat.id];
    }
    if (
      toBasket &&
      Object.keys(loan.specific_materials).length == 0 &&
      loan.generic_materials.length == 0
    ) {
      loan.entity = null;
    }
    _setLoan(loan, toBasket);
  }
  function cleanMaterials(toBasket = true) {
    let loan = Object.assign({}, !toBasket ? currentLoan.value : basket.value);
    loan.generic_materials = [];
    loan.specific_materials = {};
    if (loan.status == null) {
      loan.entity = null;
    }
    _setLoan(loan, toBasket);
  }

  return {
    objects,
    count,
    list,
    getById,
    fetchList,
    fetchSingle,
    create,
    update,
    destroy,
    status,
    fetchStatus,
    basket,
    initBasket,
    resetBasket,
    currentLoan,
    setCurrent,
    updateCurrent,
    cancelCurrent,
    askExtension,
    addMaterial,
    removeMaterial,
    cleanMaterials,
    historyChange,
    loanOrigin, 
  };
});
