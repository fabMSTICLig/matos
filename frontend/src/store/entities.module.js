import createCrud from "@/common/storeCrudHelper";

const instances_extra = {};
const instances = createCrud("instances", instances_extra);

const specific_extra = {
  modules: {
    instances: instances
  }
};
const specific = createCrud("specificmaterials", specific_extra);

const generic_extra = {};
const generic = createCrud("genericmaterials", generic_extra);
const entities_extra = {
  modules: {
    genericMaterials: generic,
    specificMaterials: specific
  }
};
const entities = createCrud("entities", entities_extra);
export default entities;
