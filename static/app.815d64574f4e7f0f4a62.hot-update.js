webpackHotUpdate("app",{

/***/ "./src/store/actions.js":
/*!******************************!*\
  !*** ./src/store/actions.js ***!
  \******************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! axios */ \"./node_modules/axios/index.js\");\n/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _common_api_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @/common/api.service */ \"./src/common/api.service.js\");\n\n\nvar actions = {\n  createEquipment: function createEquipment(_ref, equipment) {\n    var commit = _ref.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].post(\"api/equipments\", equipment, {\n      withCredentials: true\n    }).then(function (res) {\n      commit('CREATE_EQUIPMENT', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  fetchEquipments: function fetchEquipments(_ref2) {\n    var commit = _ref2.commit;\n    // Vue.use(VueAxios, axios);\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].get(\"api/equipments\", {\n      headers: {}\n    }).then(function (res) {\n      commit('FETCH_EQUIPMENTS', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  getEquipment: function getEquipment(_ref3, index) {\n    var commit = _ref3.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].get(\"api/equipments/\".concat(index), {\n      headers: {}\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('GET_EQUIPMENT', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  getCategory: function getCategory(_ref4, index) {\n    var commit = _ref4.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].get(\"api/families/\".concat(index), {\n      headers: {}\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('GET_CATEGORY', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  getCategories: function getCategories(_ref5, index) {\n    var commit = _ref5.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].get(\"api/families/\", {\n      headers: {}\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('GET_CATEGORIES', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  getOrganizations: function getOrganizations(_ref6, index) {\n    var commit = _ref6.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].get(\"api/organizations/\", {\n      headers: {}\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('GET_ORGANIZATIONS', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  getUsers: function getUsers(_ref7, index) {\n    var commit = _ref7.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].get(\"api/users/\", {\n      headers: {}\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('GET_USERS', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  getUserInstance: function getUserInstance(_ref8, index) {\n    var commit = _ref8.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].get(\"api/self\", {\n      headers: {}\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('AUTH_USER', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  },\n  updateEquipment: function updateEquipment(_ref9, equipment) {\n    var commit = _ref9.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].put(\"api/equipments/\".concat(equipment.id, \"/\"), equipment, {\n      withCredentials: true\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('GET_EQUIPMENT', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n    console.log(axios__WEBPACK_IMPORTED_MODULE_0___default.a.defaults.headers);\n  },\n  updateEntity: function updateEntity(_ref10, entity) {\n    var commit = _ref10.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].put(\"api/organizations/\".concat(entity.id, \"/\"), entity, {\n      withCredentials: true\n    }).then(function (res) {\n      console.log('Data', JSON.stringify(res, null, 4));\n      commit('SET_ORGA', res.data);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n    console.log(axios__WEBPACK_IMPORTED_MODULE_0___default.a.defaults.headers);\n  },\n  deleteEquipment: function deleteEquipment(_ref11, equipment) {\n    var commit = _ref11.commit;\n    _common_api_service__WEBPACK_IMPORTED_MODULE_1__[\"default\"].delete(\"api/equipments/\".concat(equipment.id)).then(function (res) {\n      if (res.data === 'ok') commit('DELETE_EQUIPMENT', equipment);\n    }).catch(function (err) {\n      // eslint-disable-next-line no-console\n      console.log(err);\n    });\n  }\n};\n/* harmony default export */ __webpack_exports__[\"default\"] = (actions);//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvc3RvcmUvYWN0aW9ucy5qcy5qcyIsInNvdXJjZXMiOlsid2VicGFjazovLy8uL3NyYy9zdG9yZS9hY3Rpb25zLmpzPzYzZTAiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IGF4aW9zIGZyb20gJ2F4aW9zJ1xuaW1wb3J0IEFwaVNlcnZpY2UgZnJvbSAnQC9jb21tb24vYXBpLnNlcnZpY2UnXG5cbmxldCBhY3Rpb25zID0ge1xuICBjcmVhdGVFcXVpcG1lbnQgKHsgY29tbWl0IH0sIGVxdWlwbWVudCkge1xuICAgIEFwaVNlcnZpY2VcbiAgICAgIC5wb3N0KGBhcGkvZXF1aXBtZW50c2AsIGVxdWlwbWVudCwgeyB3aXRoQ3JlZGVudGlhbHM6IHRydWUgfSlcbiAgICAgIC50aGVuKHJlcyA9PiB7XG4gICAgICAgIGNvbW1pdCgnQ1JFQVRFX0VRVUlQTUVOVCcsIHJlcy5kYXRhKVxuICAgICAgfSlcbiAgICAgIC5jYXRjaChlcnIgPT4ge1xuICAgICAgICAvLyBlc2xpbnQtZGlzYWJsZS1uZXh0LWxpbmUgbm8tY29uc29sZVxuICAgICAgICBjb25zb2xlLmxvZyhlcnIpXG4gICAgICB9KVxuICB9LFxuXG4gIGZldGNoRXF1aXBtZW50cyAoeyBjb21taXQgfSkge1xuICAgIC8vIFZ1ZS51c2UoVnVlQXhpb3MsIGF4aW9zKTtcblxuICAgIEFwaVNlcnZpY2VcbiAgICAgIC5nZXQoYGFwaS9lcXVpcG1lbnRzYCwgeyBoZWFkZXJzOiB7fSB9KVxuICAgICAgLnRoZW4ocmVzID0+IHtcbiAgICAgICAgY29tbWl0KCdGRVRDSF9FUVVJUE1FTlRTJywgcmVzLmRhdGEpXG4gICAgICB9KVxuICAgICAgLmNhdGNoKGVyciA9PiB7XG4gICAgICAgIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1jb25zb2xlXG4gICAgICAgIGNvbnNvbGUubG9nKGVycilcbiAgICAgIH0pXG4gIH0sXG5cbiAgZ2V0RXF1aXBtZW50ICh7IGNvbW1pdCB9LCBpbmRleCkge1xuICAgIEFwaVNlcnZpY2VcbiAgICAgIC5nZXQoYGFwaS9lcXVpcG1lbnRzLyR7aW5kZXh9YCwgeyBoZWFkZXJzOiB7fSB9KVxuICAgICAgLnRoZW4ocmVzID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coJ0RhdGEnLCBKU09OLnN0cmluZ2lmeShyZXMsIG51bGwsIDQpKVxuICAgICAgICBjb21taXQoJ0dFVF9FUVVJUE1FTlQnLCByZXMuZGF0YSlcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgICAgICAgY29uc29sZS5sb2coZXJyKVxuICAgICAgfSlcbiAgfSxcblxuICBnZXRDYXRlZ29yeSAoeyBjb21taXQgfSwgaW5kZXgpIHtcbiAgICBBcGlTZXJ2aWNlXG4gICAgICAuZ2V0KGBhcGkvZmFtaWxpZXMvJHtpbmRleH1gLCB7IGhlYWRlcnM6IHt9IH0pXG4gICAgICAudGhlbihyZXMgPT4ge1xuICAgICAgICBjb25zb2xlLmxvZygnRGF0YScsIEpTT04uc3RyaW5naWZ5KHJlcywgbnVsbCwgNCkpXG4gICAgICAgIGNvbW1pdCgnR0VUX0NBVEVHT1JZJywgcmVzLmRhdGEpXG4gICAgICB9KVxuICAgICAgLmNhdGNoKGVyciA9PiB7XG4gICAgICAgIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1jb25zb2xlXG4gICAgICAgIGNvbnNvbGUubG9nKGVycilcbiAgICAgIH0pXG4gIH0sXG5cbiAgZ2V0Q2F0ZWdvcmllcyAoeyBjb21taXQgfSwgaW5kZXgpIHtcbiAgICBBcGlTZXJ2aWNlXG4gICAgICAuZ2V0KGBhcGkvZmFtaWxpZXMvYCwgeyBoZWFkZXJzOiB7fSB9KVxuICAgICAgLnRoZW4ocmVzID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coJ0RhdGEnLCBKU09OLnN0cmluZ2lmeShyZXMsIG51bGwsIDQpKVxuICAgICAgICBjb21taXQoJ0dFVF9DQVRFR09SSUVTJywgcmVzLmRhdGEpXG4gICAgICB9KVxuICAgICAgLmNhdGNoKGVyciA9PiB7XG4gICAgICAgIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1jb25zb2xlXG4gICAgICAgIGNvbnNvbGUubG9nKGVycilcbiAgICAgIH0pXG4gIH0sXG5cbiAgZ2V0T3JnYW5pemF0aW9ucyAoeyBjb21taXQgfSwgaW5kZXgpIHtcbiAgICBBcGlTZXJ2aWNlXG4gICAgICAuZ2V0KGBhcGkvb3JnYW5pemF0aW9ucy9gLCB7IGhlYWRlcnM6IHt9IH0pXG4gICAgICAudGhlbihyZXMgPT4ge1xuICAgICAgICBjb25zb2xlLmxvZygnRGF0YScsIEpTT04uc3RyaW5naWZ5KHJlcywgbnVsbCwgNCkpXG4gICAgICAgIGNvbW1pdCgnR0VUX09SR0FOSVpBVElPTlMnLCByZXMuZGF0YSlcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgICAgICAgY29uc29sZS5sb2coZXJyKVxuICAgICAgfSlcbiAgfSxcbiAgZ2V0VXNlcnMgKHsgY29tbWl0IH0sIGluZGV4KSB7XG4gICAgQXBpU2VydmljZVxuICAgICAgLmdldChgYXBpL3VzZXJzL2AsIHsgaGVhZGVyczoge30gfSlcbiAgICAgIC50aGVuKHJlcyA9PiB7XG4gICAgICAgIGNvbnNvbGUubG9nKCdEYXRhJywgSlNPTi5zdHJpbmdpZnkocmVzLCBudWxsLCA0KSlcbiAgICAgICAgY29tbWl0KCdHRVRfVVNFUlMnLCByZXMuZGF0YSlcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgICAgICAgY29uc29sZS5sb2coZXJyKVxuICAgICAgfSlcbiAgfSxcblxuICBnZXRVc2VySW5zdGFuY2UgKHsgY29tbWl0IH0sIGluZGV4KSB7XG4gICAgQXBpU2VydmljZVxuICAgICAgLmdldChgYXBpL3NlbGZgLCB7IGhlYWRlcnM6IHt9IH0pXG4gICAgICAudGhlbihyZXMgPT4ge1xuICAgICAgICBjb25zb2xlLmxvZygnRGF0YScsIEpTT04uc3RyaW5naWZ5KHJlcywgbnVsbCwgNCkpXG4gICAgICAgIGNvbW1pdCgnQVVUSF9VU0VSJywgcmVzLmRhdGEpXG4gICAgICB9KVxuICAgICAgLmNhdGNoKGVyciA9PiB7XG4gICAgICAgIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1jb25zb2xlXG4gICAgICAgIGNvbnNvbGUubG9nKGVycilcbiAgICAgIH0pXG4gIH0sXG4gIFxuICB1cGRhdGVFcXVpcG1lbnQgKHsgY29tbWl0IH0sIGVxdWlwbWVudCkge1xuICAgIEFwaVNlcnZpY2VcbiAgICAgIC5wdXQoYGFwaS9lcXVpcG1lbnRzLyR7ZXF1aXBtZW50LmlkfS9gLCBlcXVpcG1lbnQsIHtcbiAgICAgICAgd2l0aENyZWRlbnRpYWxzOiB0cnVlXG4gICAgICB9KVxuICAgICAgLnRoZW4ocmVzID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coJ0RhdGEnLCBKU09OLnN0cmluZ2lmeShyZXMsIG51bGwsIDQpKVxuICAgICAgICBjb21taXQoJ0dFVF9FUVVJUE1FTlQnLCByZXMuZGF0YSlcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgICAgICAgY29uc29sZS5sb2coZXJyKVxuICAgICAgfSlcblxuICAgIGNvbnNvbGUubG9nKGF4aW9zLmRlZmF1bHRzLmhlYWRlcnMpXG4gIH0sXG5cbiAgdXBkYXRlRW50aXR5KCB7Y29tbWl0fSwgZW50aXR5KSB7XG4gICAgQXBpU2VydmljZVxuICAgICAgLnB1dChgYXBpL29yZ2FuaXphdGlvbnMvJHtlbnRpdHkuaWR9L2AsIGVudGl0eSwge1xuICAgICAgICB3aXRoQ3JlZGVudGlhbHM6IHRydWVcbiAgICAgIH0pXG4gICAgICAudGhlbihyZXMgPT4ge1xuICAgICAgICBjb25zb2xlLmxvZygnRGF0YScsIEpTT04uc3RyaW5naWZ5KHJlcywgbnVsbCwgNCkpXG4gICAgICAgIGNvbW1pdCgnU0VUX09SR0EnLCByZXMuZGF0YSlcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgICAgICAgY29uc29sZS5sb2coZXJyKVxuICAgICAgfSlcblxuICAgIGNvbnNvbGUubG9nKGF4aW9zLmRlZmF1bHRzLmhlYWRlcnMpXG4gIH0sXG5cbiAgZGVsZXRlRXF1aXBtZW50ICh7IGNvbW1pdCB9LCBlcXVpcG1lbnQpIHtcbiAgIFxuICAgIEFwaVNlcnZpY2VcbiAgICAgIC5kZWxldGUoYGFwaS9lcXVpcG1lbnRzLyR7ZXF1aXBtZW50LmlkfWApXG4gICAgICAudGhlbihyZXMgPT4ge1xuICAgICAgICBpZiAocmVzLmRhdGEgPT09ICdvaycpIGNvbW1pdCgnREVMRVRFX0VRVUlQTUVOVCcsIGVxdWlwbWVudClcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLWNvbnNvbGVcbiAgICAgICAgY29uc29sZS5sb2coZXJyKVxuICAgICAgfSlcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBhY3Rpb25zXG4iXSwibWFwcGluZ3MiOiJBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFDQTtBQUVBO0FBQ0E7QUFBQTtBQUNBO0FBQ0E7QUFBQTtBQUVBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQUE7QUFDQTtBQUVBO0FBQ0E7QUFBQTtBQUVBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQUE7QUFDQTtBQUNBO0FBQUE7QUFFQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQUE7QUFDQTtBQUNBO0FBQUE7QUFFQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQUE7QUFDQTtBQUNBO0FBQUE7QUFFQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQUE7QUFDQTtBQUNBO0FBQUE7QUFFQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQUE7QUFDQTtBQUNBO0FBQUE7QUFFQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQUE7QUFDQTtBQUNBO0FBQUE7QUFFQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQUE7QUFDQTtBQUVBO0FBREE7QUFJQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBRUE7QUFBQTtBQUNBO0FBRUE7QUFEQTtBQUlBO0FBQ0E7QUFDQTtBQUVBO0FBQ0E7QUFDQTtBQUVBO0FBQ0E7QUFFQTtBQUFBO0FBRUE7QUFHQTtBQUNBO0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFySkE7QUF3SkEiLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./src/store/actions.js\n");

/***/ })

})