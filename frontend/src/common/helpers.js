export const DataHelper = {
  updateById: function (items, item) {
    var index = items.findIndex((i) => {
      return i.id == item.id;
    });
    if (index != -1) {
      items.splice(index, 1, item);
    } else {
      items.push(item);
    }
  },
  copy: function (object) {
    let objectCopy = {}; // objectCopy will store a copy of the mainObject
    let key;
    for (key in object) {
      objectCopy[key] = object[key]; // copies each property to the objectCopy object
    }
    return objectCopy;
  },
};

export const JSONRenderer = {
  download: function (content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([JSON.stringify(content, null, 2)], {
      type: contentType,
    });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  },
};
