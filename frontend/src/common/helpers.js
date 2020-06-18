export const DataHelper = {
  updateById: function(items, item) {
    var index = items.findIndex(i => {
      return i.id == item.id;
    });
    if (index != -1) {
      items.splice(index, 1, item);
    } else {
      items.push(item);
    }
  }
};
