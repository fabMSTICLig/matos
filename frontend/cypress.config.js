const { defineConfig } = require("cypress");
const { rmdir } = require('fs');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8000',
    setupNodeEvents(on, config) {
      on('task', {
        deleteFolder(folderName) {
          console.log('deleting folder %s', folderName)
    
          return new Promise((resolve, reject) => {
            rmdir(folderName, { maxRetries: 3, recursive: true }, (err) => {
              if (err) {
                console.error(err)
                return reject(err)
              }
              resolve(null)
            })
          })
        },
      })
    },
  },
});
