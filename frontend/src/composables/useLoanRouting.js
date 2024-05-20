/*
 * Copyright (C) 2020-2024 LIG Université Grenoble Alpes
 *
 *
 * This file is part of Matos.
 *
 * FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * Matos is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>
 *
 * @author Germain Lemasson
 * @author Clément Lesaulnier
 * @author Robin Courault
*/
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
