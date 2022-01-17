<template>
  <div class="row">
    <div class="col-12">
      <div v-if="material" class="card">
        <div class="card-header">
          <h3 class="float-start" v-text="material.name" />
          <div class="float-end">
            <div class="btn-group" role="group">
              <button
                class="btn btn-primary"
                type="button"
                @click="addMaterial()"
                :class="{
                  disabled:
                    pendingLoan.entity && pendingLoan.entity != material.entity,
                }"
              >
                Ajouter
              </button>
              <router-link
                v-if="isManager"
                class="btn btn-primary"
                role="button"
                :to="editRoute"
              >
                Modifier
              </router-link>
              <div
                v-if="isManager && managedEntities.length"
                ref="dropcopy"
                class="btn-group"
                style="margin-right: 10px"
                @focusout="hideDropdown"
              >
                <button
                  id="dropdownMenuButton"
                  class="btn btn-primary dropdown-toggle"
                  @click="toggleDropdown"
                >
                  Copier
                </button>
                <ul
                  :class="showDropdown ? 'dropdown-menu show' : 'dropdown-menu'"
                  aria-labelledby="dropdownMenuButton"
                  :style="dropdownStyle"
                >
                  <li v-for="item in managedEntities" :key="item.id">
                    <button
                      class="dropdown-item"
                      type="button"
                      @click="copyMaterial(item)"
                    >
                      {{ item.name }}
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-12 col-md-6">
              <markdown
                :description="material.description"
              />
            </div>
            <div  class="col-12 col-md-6">
            <table class="table">
              <tr>
                <th scope="row">Appartient à</th>
                <td>
                  <router-link
                    :to="{
                      name: 'entityinfos',
                      params: { entityid: material.entity },
                    }"
                    >{{ materialEntity.name }}</router-link
                  >
                </td>
              </tr>
              <tr>
                <th scope="row">Ref interne</th>
                <td>{{ material.ref_int }}</td>
              </tr>
              <tr>
                <th scope="row">Ref fabricant</th>
                <td>{{ material.ref_man }}</td>
              </tr>
            </table>
            
            <p class="col-12 col-md-6">
              <span><strong>Tags :&nbsp;</strong></span>
              <DisplayIdList :items="materialTags" />
            </p>
          </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, onBeforeMount, inject } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";

import Markdown from "@/components/ui/Markdown.vue";
import DisplayIdList from "@/components/ui/DisplayIdList.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const material = ref(null);

const materialTags = ref([]);
const materialEntity = ref([]);

const entityName = computed(() => {
  let entity = store.getters["entities/byId"](material.value.entity);
  if (entity) {
    return entity.name;
  } else return "";
});

onBeforeMount(async () => {
  let typeMat = "";
  if (route.name == "specificmaterialitem") {
    typeMat = "fetchSingleSpecificMaterial";
  }
  if (route.name == "genericmaterialitem") {
    typeMat = "fetchSingleGenericMaterial";
  }

  material.value = Object.assign(
    {},
    await store.dispatch("materials/" + typeMat, {
      id: route.params[route.meta.routeparam],
    })
  );
  if (material.value.tags) {
    materialTags.value = [
      ...(await store.dispatch("tags/fetchList", {
        params: { ids: material.value.tags.join(",") },
      })),
    ];
  }
  //Récupération de l'entité avant de flush mémoire avec entité user
  materialEntity.value = await store.dispatch("entities/fetchSingle", {
    id: material.value.entity,
  });

  let ids = authUser.value.entities.filter((e) => e != material.entity);
  if (ids)
    managedEntities.value = await store.dispatch("entities/fetchList", {
      params: { ids: ids.join(",") },
    });
  else managedEntities.value = [];
});

const authUser = computed(() => store.getters.authUser);
const isManager = computed(() => {
  return authUser.value.entities.length || authUser.value.is_staff;
});
const pendingLoan = computed(() => store.getters["loans/pendingLoan"]);
const editRoute = computed(() => {
  let name = "specificmaterial";
  if ("quantity" in material.value) {
    name = "genericmaterial";
  }
  return {
    name: name,
    params: { matid: material.value.id, entityid: material.value.entity },
  };
});

function addMaterial() {
  store.dispatch("loans/addMaterial", material.value);
}

const managedEntities = ref([]);
const showDropdown = ref(false);
const dropdownStyle = computed(() => {
  if (showDropdown.value)
    return "position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate(0px, 40px);";
  else return "";
});
const dropcopy = ref();
function toggleDropdown() {
  showDropdown.value = !showDropdown.value;
}
function hideDropdown(e) {
  console.log(e);
  if (!dropcopy.value.contains(e.relatedTarget)) {
    showDropdown.value = false;
  }
}
async function copyMaterial(entity) {
  /*
        Copie du matériel dans une entité gérée
      */
  let ressource = "";
  let routeName = "";
  if (route.name == "genericmaterialitem") {
    ressource = "genericmaterials";
    routeName = "genericmaterial";
  } else if (route.name == "specificmaterialitem") {
    ressource = "specificmaterials";
    routeName = "specificmaterial";
  }
  var prefix = "entities/" + entity.id + "/";

  try {
    const mat = await store.dispatch(ressource + "/create", {
      data: material.value,
      prefix: prefix,
    });
    router.push({
      name: routeName,
      params: { matid: mat.id, entityid: entity.id },
    });
  } catch (error) {
    if (error.response.data.non_field_errors) {
      const showModal = inject("show");
      showModal({
        content: "La copie a échouée, vous avez déjà un matériel avec ce nom.",
      });
    }
  }
}
</script>
