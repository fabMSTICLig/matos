import ApiService from "@/common/api.service"


export default  {

    query(params) {
        return ApiService.query("equipments", {
            params: params
        });
    },
    getEquipments(slug) {
        return ApiService.get("equipments/", slug);
    },
    update(slug, user) {
        return ApiService.update("equipments", slug, user);
    },
    create(data) {
        return ApiService.post("equipments/", data);
    }
}