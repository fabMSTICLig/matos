import createCrud from "@/common/storeCrudHelper";

const instances_extra = {};
const instances = createCrud("instances", instances_extra);

const specific_extra = {
  modules: {
    instances: instances
  }
};
export const specificmaterials = createCrud(
  "specificmaterials",
  specific_extra
);

const generic_extra = {};
export const genericmaterials = createCrud("genericmaterials", generic_extra);
