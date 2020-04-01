export const DataHelper = {
  updateById: function (items, item) {
    var index = items.findIndex((i) => {
      // eslint-disable-next-line eqeqeq
      return i.id == item.id
    })
    // eslint-disable-next-line eqeqeq
    if (index != -1) {
      items.splice(index, 1, item)
    } else {
      items.push(item)
    }
  },
  removeById: function (items, item) {
    var index = items.findIndex((i) => {
      // eslint-disable-next-line eqeqeq
      return i.id == item.id
    })
    // eslint-disable-next-line eqeqeq
    if (index != -1) {
      items.splice(index, 1)
    }
  }
}
