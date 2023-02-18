import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";

export default function useLoanRouting(loansStore, authUser) {
  const route = useRoute();
  const router = useRouter();

  const isAuthLoan = computed(() => {
    return (
      (loansStore.loanOrigin != null &&
        loansStore.loanOrigin.name == "authloans") ||
      (loansStore.loanOrigin == null &&
        loansStore.currentLoan &&
        loansStore.currentLoan.user == authUser.value.id)
    );
  });

  function initOrigin() {
    if (!loansStore.loanOrigin) {
      loansStore.loanOrigin = isAuthLoan.value
        ? { name: "authloans" }
        : {
            name: "entityloans",
            params: { entityid: loansStore.currentLoan.entity },
          };
    }
  }
  function toLoan(id) {
    loansStore.loanOrigin = { name: route.name, params: route.params };
    router.push({ name: "loan", params: { loanid: id } });
  }

  function goBack() {
    if (isAuthLoan.value) router.push({ name: "authloans" });
    router.push(loansStore.loanOrigin);
  }

  function goBackToLoan() {
    router.push({
      name: "loan",
      params: { loanid: loansStore.currentLoan.id },
    });
  }

  return {
    toLoan,
    initOrigin,
    isAuthLoan,
    goBack,
    goBackToLoan,
  };
}
