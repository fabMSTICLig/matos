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
import { ref, computed, inject } from "vue";
import { useRouter, useRoute, onBeforeRouteUpdate } from "vue-router";

export default function useEditor(
  store,
  emptyObject,
  listRoute,
  {
    prefix = "",
  } = {}
) {
  const object = ref(null);
  const editorForm = ref(null);

  const route = useRoute();

  const isNew = computed(() => route.params[route.meta.routeparam] == "new");

  const confirmModal = inject("confirm");

  async function initObject(route) {
    if (route.params[route.meta.routeparam] == "new") {
      object.value = Object.assign({}, emptyObject);
    } else if (parseInt(route.params[route.meta.routeparam], -1) != -1) {
      const data = await store.fetchSingle(
        route.params[route.meta.routeparam],
        prefix
      );
      object.value = Object.assign({}, data);
    }
    return object.value;
  }

  const router = useRouter();
  async function create(push=true) {
    if (editorForm.value.checkValidity()) {
      try{
      const data = await store.create(
          object.value,
          prefix
        )
          if(push)router.push(listRoute);
          return data
      }catch(error){
          console.log(error)
          console.log(JSON.stringify(error));
      }
    } else {
      editorForm.value.reportValidity();
    }
  }
  async function update(push=true) {
    if (editorForm.value.checkValidity()) {
      store
        .update(
          object.value.id,
          object.value,
          prefix
        )
        .then(() => {
          if(push)router.push(listRoute);
        });
    } else {
      editorForm.value.reportValidity();
    }
  }
  async function destroy(push=true) {
    const isConfirmed = await confirmModal({
      content: 'Voulez vous vraiment supprimer '+object.value.name+' ?',
    });
    if (isConfirmed) {
      await store.destroy(
        object.value.id,
        prefix
      );
      if(push)router.push(listRoute);
    }
  }
  async function cancel(){
      router.push(listRoute);
  }

  onBeforeRouteUpdate(async (to, from, next) => {
    await initObject(to);
    next();
  });

  return {
    editorForm,
    object,
    isNew,
    initObject,
    create,
    update,
    destroy,
    cancel,
  };
}
