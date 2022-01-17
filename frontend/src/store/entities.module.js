import createCrud from "./crud.factory";

const entities_extra = {};
const entities = createCrud("entities", entities_extra);
export default entities;
