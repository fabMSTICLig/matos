import createCrud from "./crud.factory";

const users_extra = {};
const users = createCrud("users", users_extra);
export default users;
