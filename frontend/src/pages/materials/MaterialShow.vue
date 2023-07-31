<template>
  <div class="row">
    <div class="col-12">
      <div v-if="material" class="card">
        <div class="card-header">
          <h3 class="float-start" v-text="material.name" />
          <div class="float-end">
            <div class="btn-group" role="group">
              <router-link
                v-if="isManagerOf"
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
                  :class="{ show: showDropdown }"
                  class="dropdown-menu"
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
              <markdown :description="material.description" />
            </div>
            <div class="col-12 col-md-6">
              <table class="table">
                <tr>
                  <th scope="row">Appartient à</th>
                  <td>
                    <router-link
                      :to="{
                        name: 'entityinfos',
                        params: { entityid: material.entity },
                      }"
                    >
                      {{ materialEntity.name }}
                    </router-link>
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
import { ref, computed, onBeforeMount, inject } from "vue";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {
  useMaterialsStore,
  useSpecificMaterialsStore,
  useGenericMaterialsStore,
} from "@/stores/materials";
import { useEntitiesStore } from "@/stores/entities";
import { useTagsStore } from "@/stores/tags";

import Markdown from "@/components/ui/MarkdownComponent.vue";
import DisplayIdList from "@/components/ui/DisplayIdList.vue";

const store = useMaterialsStore();

const authStore = useAuthStore();
const { authUser, isManager } = storeToRefs(authStore);

const isManagerOf = computed(
  () =>
    material.value &&
    authUser.value.entities.indexOf(material.value.entity) > -1
);

const tagsStore = useTagsStore();
const entitiesStore = useEntitiesStore();

const route = useRoute();
const router = useRouter();

const material = ref(null);

const materialTags = ref([]);
const materialEntity = ref([]);

onBeforeMount(async () => {
  let typeMat = "";
  if (route.name == "specificmaterialitem") {
    typeMat = "fetchSingleSpecificMaterial";
  }
  if (route.name == "genericmaterialitem") {
    typeMat = "fetchSingleGenericMaterial";
  }

  material.value = Object.assign({}, await store[typeMat](route.params.matid));
  if (material.value.tags) {
    materialTags.value = [
      ...(await tagsStore.fetchList({ ids: material.value.tags.join(",") })),
    ];
  }
  //Récupération de l'entité avant de flush mémoire avec entité user
  materialEntity.value = await entitiesStore.fetchSingle(material.value.entity);

  let ids = authUser.value.entities.filter((e) => e != material.value.entity);
  if (ids)
    managedEntities.value = await entitiesStore.fetchList({
      ids: ids.join(","),
    });
  else managedEntities.value = [];
});

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

const managedEntities = ref([]);
///Visual dropdown
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
  if (dropcopy.value && !dropcopy.value.contains(e.relatedTarget)) {
    showDropdown.value = false;
  }
}
///////

const speMatS = useSpecificMaterialsStore();
const genMatS = useGenericMaterialsStore();

async function copyMaterial(entity) {
  /*
        Copie du matériel dans une entité gérée
      */
  let storeMat = "";
  let routeName = "";
  if (route.name == "genericmaterialitem") {
    storeMat = genMatS;
    routeName = "genericmaterial";
  } else if (route.name == "specificmaterialitem") {
    storeMat = speMatS;
    routeName = "specificmaterial";
  }
  var prefix = "entities/" + entity.id + "/";

  try {
    const mat = await storeMat.create(material.value, prefix);
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
